#!/usr/bin/env python3
"""
Start Patients Table Monitoring

This script starts the patients table monitoring in the background.
"""

import subprocess
import sys
import os
from datetime import datetime

def start_monitoring():
    """Start the monitoring process in the background."""
    print("🚀 Starting Patients Table Monitoring...")
    print("=" * 60)
    
    # Check if monitoring is already running
    try:
        result = subprocess.run(['pgrep', '-f', 'patients_monitor.py'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            print("⚠️  Monitoring appears to already be running!")
            print(f"Process ID(s): {result.stdout.strip()}")
            response = input("Do you want to start another instance? (y/N): ")
            if response.lower() != 'y':
                print("❌ Monitoring start cancelled")
                return False
    except:
        pass  # pgrep might not be available on all systems
    
    # Start monitoring in background
    log_file = '/workspace/snowflake_demo/patients_monitor.log'
    
    print(f"📝 Log file: {log_file}")
    print(f"⏰ Check interval: Every hour")
    print(f"📊 Monitoring table: development.patients.patients")
    print()
    
    try:
        # Start the monitoring process
        process = subprocess.Popen([
            sys.executable, 
            '/workspace/snowflake_demo/patients_monitor.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print(f"✅ Monitoring started successfully!")
        print(f"🆔 Process ID: {process.pid}")
        print()
        print("📋 Available commands:")
        print("  • Check status: python start_monitoring.py --status")
        print("  • Stop monitoring: python start_monitoring.py --stop")
        print("  • View logs: tail -f patients_monitor.log")
        print("  • Run single check: python patients_monitor.py --check-once")
        print()
        print("🔍 The monitor will check for new records every hour and log any changes.")
        print("💡 Use Ctrl+C to stop this script (monitoring will continue in background)")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to start monitoring: {str(e)}")
        return False

def check_status():
    """Check the monitoring status."""
    try:
        result = subprocess.run([
            sys.executable, 
            '/workspace/snowflake_demo/patients_monitor.py', 
            '--status'
        ], capture_output=True, text=True)
        
        print(result.stdout)
        
        # Check if process is running
        try:
            pgrep_result = subprocess.run(['pgrep', '-f', 'patients_monitor.py'], 
                                        capture_output=True, text=True)
            if pgrep_result.stdout.strip():
                print(f"🟢 Monitoring process is running (PID: {pgrep_result.stdout.strip()})")
            else:
                print("🔴 No monitoring process found running")
        except:
            print("❓ Could not check if monitoring process is running")
            
    except Exception as e:
        print(f"❌ Error checking status: {str(e)}")

def stop_monitoring():
    """Stop the monitoring process."""
    try:
        result = subprocess.run(['pgrep', '-f', 'patients_monitor.py'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            pids = result.stdout.strip().split('\n')
            print(f"🛑 Stopping monitoring process(es): {', '.join(pids)}")
            
            for pid in pids:
                try:
                    subprocess.run(['kill', pid], check=True)
                    print(f"✅ Stopped process {pid}")
                except:
                    print(f"❌ Failed to stop process {pid}")
        else:
            print("ℹ️  No monitoring processes found running")
            
    except Exception as e:
        print(f"❌ Error stopping monitoring: {str(e)}")

def show_logs():
    """Show recent log entries."""
    log_file = '/workspace/snowflake_demo/patients_monitor.log'
    
    if os.path.exists(log_file):
        print("📋 Recent log entries (last 20 lines):")
        print("=" * 60)
        try:
            result = subprocess.run(['tail', '-20', log_file], 
                                  capture_output=True, text=True)
            print(result.stdout)
        except:
            # Fallback to Python implementation
            with open(log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-20:]:
                    print(line.rstrip())
    else:
        print("📝 No log file found yet. Monitoring may not have started.")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage patients table monitoring')
    parser.add_argument('--status', action='store_true', help='Check monitoring status')
    parser.add_argument('--stop', action='store_true', help='Stop monitoring')
    parser.add_argument('--logs', action='store_true', help='Show recent log entries')
    
    args = parser.parse_args()
    
    if args.status:
        check_status()
    elif args.stop:
        stop_monitoring()
    elif args.logs:
        show_logs()
    else:
        start_monitoring()

if __name__ == "__main__":
    main()