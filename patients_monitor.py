#!/usr/bin/env python3
"""
Patients Table Monitor

This script monitors the patients table every hour and alerts when new records are inserted.
It tracks the record count and identifies new records by comparing with the last known state.
"""

import os
import time
import json
import logging
from datetime import datetime, timedelta
import snowflake.connector
from dotenv import load_dotenv
import signal
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/workspace/snowflake_demo/patients_monitor.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class PatientsMonitor:
    def __init__(self):
        """Initialize the patients monitor."""
        load_dotenv()
        
        self.connection_params = {
            'account': os.getenv('SNOWFLAKE_ACCOUNT'),
            'user': os.getenv('SNOWFLAKE_USER'),
            'password': os.getenv('SNOWFLAKE_PASSWORD'),
            'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE'),
            'database': os.getenv('SNOWFLAKE_DATABASE', 'development'),
            'role': os.getenv('SNOWFLAKE_ROLE')
        }
        
        self.state_file = '/workspace/snowflake_demo/monitor_state.json'
        self.monitoring = True
        self.check_interval = 3600  # 1 hour in seconds
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully."""
        logger.info(f"Received signal {signum}. Shutting down gracefully...")
        self.monitoring = False
    
    def connect_to_snowflake(self):
        """Connect to Snowflake."""
        try:
            connection = snowflake.connector.connect(**self.connection_params)
            return connection
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {str(e)}")
            return None
    
    def get_current_state(self):
        """Get current state of the patients table."""
        connection = self.connect_to_snowflake()
        if not connection:
            return None
        
        try:
            cursor = connection.cursor()
            cursor.execute("USE DATABASE development")
            
            # Get current record count
            cursor.execute("SELECT COUNT(*) FROM development.patients.patients")
            record_count = cursor.fetchone()[0]
            
            # Get all current records with their IDs
            cursor.execute("SELECT id, name FROM development.patients.patients ORDER BY id")
            current_records = cursor.fetchall()
            
            # Get the maximum ID (assuming ID is auto-incrementing or sequential)
            cursor.execute("SELECT MAX(id) FROM development.patients.patients")
            max_id = cursor.fetchone()[0]
            
            state = {
                'timestamp': datetime.now().isoformat(),
                'record_count': record_count,
                'max_id': max_id,
                'records': [{'id': record[0], 'name': record[1]} for record in current_records]
            }
            
            cursor.close()
            connection.close()
            
            return state
            
        except Exception as e:
            logger.error(f"Error getting current state: {str(e)}")
            if connection:
                connection.close()
            return None
    
    def load_previous_state(self):
        """Load the previous state from file."""
        try:
            if os.path.exists(self.state_file):
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Error loading previous state: {str(e)}")
            return None
    
    def save_state(self, state):
        """Save the current state to file."""
        try:
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving state: {str(e)}")
    
    def compare_states(self, previous_state, current_state):
        """Compare previous and current states to detect changes."""
        if not previous_state:
            return {
                'new_records_detected': True,
                'new_records': current_state['records'],
                'message': f"Initial scan: Found {current_state['record_count']} existing records"
            }
        
        prev_count = previous_state['record_count']
        curr_count = current_state['record_count']
        
        if curr_count > prev_count:
            # New records detected
            prev_ids = {record['id'] for record in previous_state['records']}
            new_records = [record for record in current_state['records'] if record['id'] not in prev_ids]
            
            return {
                'new_records_detected': True,
                'new_records': new_records,
                'previous_count': prev_count,
                'current_count': curr_count,
                'records_added': curr_count - prev_count,
                'message': f"🚨 NEW RECORDS DETECTED! {curr_count - prev_count} new record(s) added"
            }
        elif curr_count < prev_count:
            # Records deleted
            return {
                'new_records_detected': False,
                'records_deleted': prev_count - curr_count,
                'previous_count': prev_count,
                'current_count': curr_count,
                'message': f"⚠️  RECORDS DELETED! {prev_count - curr_count} record(s) removed"
            }
        else:
            # No change in count, but check if records were modified
            prev_records = {record['id']: record['name'] for record in previous_state['records']}
            curr_records = {record['id']: record['name'] for record in current_state['records']}
            
            if prev_records != curr_records:
                return {
                    'new_records_detected': False,
                    'records_modified': True,
                    'message': "📝 Records modified (same count but different data)"
                }
            else:
                return {
                    'new_records_detected': False,
                    'message': f"✅ No changes detected. Current count: {curr_count}"
                }
    
    def send_alert(self, comparison_result, current_state):
        """Send alert about changes (currently logs, but can be extended to email/slack/etc)."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info("=" * 80)
        logger.info(f"PATIENTS TABLE MONITORING ALERT - {timestamp}")
        logger.info("=" * 80)
        logger.info(comparison_result['message'])
        
        if comparison_result.get('new_records_detected'):
            if 'new_records' in comparison_result:
                logger.info(f"\n📋 New Records Details:")
                for i, record in enumerate(comparison_result['new_records'], 1):
                    logger.info(f"   {i}. ID: {record['id']}, Name: {record['name']}")
        
        if 'previous_count' in comparison_result:
            logger.info(f"\n📊 Count Summary:")
            logger.info(f"   Previous Count: {comparison_result['previous_count']}")
            logger.info(f"   Current Count: {comparison_result['current_count']}")
            if 'records_added' in comparison_result:
                logger.info(f"   Records Added: {comparison_result['records_added']}")
        
        logger.info(f"\n🕐 Next check scheduled for: {(datetime.now() + timedelta(seconds=self.check_interval)).strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info("=" * 80)
        
        # Here you could add additional alert mechanisms:
        # - Send email
        # - Post to Slack
        # - Send SMS
        # - Write to a webhook
        # - etc.
    
    def run_single_check(self):
        """Run a single monitoring check."""
        logger.info("🔍 Starting patients table check...")
        
        # Get current state
        current_state = self.get_current_state()
        if not current_state:
            logger.error("❌ Failed to get current state. Skipping this check.")
            return False
        
        # Load previous state
        previous_state = self.load_previous_state()
        
        # Compare states
        comparison_result = self.compare_states(previous_state, current_state)
        
        # Send alert if changes detected
        if comparison_result.get('new_records_detected') or comparison_result.get('records_deleted') or comparison_result.get('records_modified'):
            self.send_alert(comparison_result, current_state)
        else:
            logger.info(comparison_result['message'])
        
        # Save current state
        self.save_state(current_state)
        
        return True
    
    def start_monitoring(self):
        """Start the monitoring loop."""
        logger.info("🚀 Starting Patients Table Monitor")
        logger.info(f"📊 Monitoring: development.patients.patients")
        logger.info(f"⏰ Check interval: {self.check_interval} seconds (1 hour)")
        logger.info(f"📝 Log file: /workspace/snowflake_demo/patients_monitor.log")
        logger.info(f"💾 State file: {self.state_file}")
        logger.info("=" * 80)
        
        # Run initial check
        self.run_single_check()
        
        # Start monitoring loop
        while self.monitoring:
            try:
                # Wait for next check
                for i in range(self.check_interval):
                    if not self.monitoring:
                        break
                    time.sleep(1)
                
                if self.monitoring:
                    self.run_single_check()
                    
            except Exception as e:
                logger.error(f"❌ Error in monitoring loop: {str(e)}")
                logger.info("⏳ Waiting 60 seconds before retrying...")
                time.sleep(60)
        
        logger.info("🛑 Monitoring stopped")
    
    def get_status(self):
        """Get current monitoring status."""
        previous_state = self.load_previous_state()
        if previous_state:
            last_check = datetime.fromisoformat(previous_state['timestamp'])
            next_check = last_check + timedelta(seconds=self.check_interval)
            
            return {
                'monitoring_active': self.monitoring,
                'last_check': last_check.strftime('%Y-%m-%d %H:%M:%S'),
                'next_check': next_check.strftime('%Y-%m-%d %H:%M:%S'),
                'current_record_count': previous_state['record_count'],
                'max_id': previous_state['max_id']
            }
        else:
            return {
                'monitoring_active': self.monitoring,
                'last_check': 'Never',
                'next_check': 'On next run',
                'current_record_count': 'Unknown',
                'max_id': 'Unknown'
            }

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Monitor patients table for new records')
    parser.add_argument('--check-once', action='store_true', help='Run a single check and exit')
    parser.add_argument('--status', action='store_true', help='Show monitoring status')
    parser.add_argument('--interval', type=int, default=3600, help='Check interval in seconds (default: 3600 = 1 hour)')
    
    args = parser.parse_args()
    
    monitor = PatientsMonitor()
    monitor.check_interval = args.interval
    
    if args.status:
        status = monitor.get_status()
        print("\n📊 PATIENTS TABLE MONITORING STATUS")
        print("=" * 50)
        print(f"Monitoring Active: {status['monitoring_active']}")
        print(f"Last Check: {status['last_check']}")
        print(f"Next Check: {status['next_check']}")
        print(f"Current Record Count: {status['current_record_count']}")
        print(f"Max ID: {status['max_id']}")
        print("=" * 50)
    elif args.check_once:
        print("🔍 Running single check...")
        monitor.run_single_check()
        print("✅ Check completed")
    else:
        monitor.start_monitoring()

if __name__ == "__main__":
    main()