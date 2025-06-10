#!/usr/bin/env python3
"""
Patients Table Monitoring Dashboard

This script provides a simple dashboard to view monitoring results and alerts.
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
import time

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def read_log_file():
    """Read and parse the log file."""
    log_file = '/workspace/snowflake_demo/patients_monitor.log'
    
    if not os.path.exists(log_file):
        return []
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()]
    except Exception as e:
        return [f"Error reading log file: {str(e)}"]

def read_state_file():
    """Read the current state file."""
    state_file = '/workspace/snowflake_demo/monitor_state.json'
    
    if not os.path.exists(state_file):
        return None
    
    try:
        with open(state_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        return None

def check_process_status():
    """Check if monitoring process is running."""
    try:
        result = subprocess.run(['pgrep', '-f', 'patients_monitor.py'], 
                              capture_output=True, text=True)
        if result.stdout.strip():
            return True, result.stdout.strip().split('\n')
        return False, []
    except:
        return None, []

def format_timestamp(timestamp_str):
    """Format timestamp for display."""
    try:
        dt = datetime.fromisoformat(timestamp_str)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except:
        return timestamp_str

def display_dashboard():
    """Display the monitoring dashboard."""
    clear_screen()
    
    print("🏥 PATIENTS TABLE MONITORING DASHBOARD")
    print("=" * 80)
    print(f"Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check process status
    is_running, pids = check_process_status()
    
    print("🔄 MONITORING STATUS")
    print("-" * 40)
    if is_running:
        print(f"✅ Status: RUNNING (PID: {', '.join(pids)})")
    elif is_running is None:
        print("❓ Status: UNKNOWN (cannot check process)")
    else:
        print("🔴 Status: NOT RUNNING")
    
    # Read current state
    state = read_state_file()
    if state:
        print(f"📊 Current Record Count: {state['record_count']}")
        print(f"🆔 Max ID: {state['max_id']}")
        print(f"🕐 Last Check: {format_timestamp(state['timestamp'])}")
        
        # Calculate next check time
        last_check = datetime.fromisoformat(state['timestamp'])
        next_check = last_check + timedelta(hours=1)
        print(f"⏰ Next Check: {next_check.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Time until next check
        time_until_next = next_check - datetime.now()
        if time_until_next.total_seconds() > 0:
            minutes_left = int(time_until_next.total_seconds() / 60)
            print(f"⏳ Time Until Next Check: {minutes_left} minutes")
        else:
            print("⏳ Next check is overdue")
    else:
        print("📊 No state information available")
    
    print()
    
    # Show recent alerts/changes
    log_lines = read_log_file()
    alert_lines = [line for line in log_lines if any(keyword in line for keyword in 
                   ['NEW RECORDS DETECTED', 'RECORDS DELETED', 'Records modified', 'ALERT'])]
    
    print("🚨 RECENT ALERTS")
    print("-" * 40)
    if alert_lines:
        # Show last 5 alerts
        for line in alert_lines[-5:]:
            print(f"  {line}")
    else:
        print("  No alerts found")
    
    print()
    
    # Show recent log entries
    print("📋 RECENT LOG ENTRIES (Last 10)")
    print("-" * 40)
    recent_logs = log_lines[-10:] if log_lines else ["No log entries found"]
    for line in recent_logs:
        # Truncate long lines
        if len(line) > 75:
            line = line[:72] + "..."
        print(f"  {line}")
    
    print()
    print("🎛️  CONTROLS")
    print("-" * 40)
    print("  r - Refresh dashboard")
    print("  s - Show full status")
    print("  l - Show full logs")
    print("  t - Run test check")
    print("  q - Quit dashboard")

def show_full_status():
    """Show full monitoring status."""
    clear_screen()
    print("📊 FULL MONITORING STATUS")
    print("=" * 60)
    
    try:
        result = subprocess.run([
            'python', '/workspace/snowflake_demo/patients_monitor.py', '--status'
        ], capture_output=True, text=True, cwd='/workspace/snowflake_demo')
        print(result.stdout)
    except Exception as e:
        print(f"Error getting status: {str(e)}")
    
    input("\nPress Enter to return to dashboard...")

def show_full_logs():
    """Show full log file."""
    clear_screen()
    print("📋 FULL LOG FILE")
    print("=" * 60)
    
    log_lines = read_log_file()
    if log_lines:
        for line in log_lines:
            print(line)
    else:
        print("No log entries found")
    
    input("\nPress Enter to return to dashboard...")

def run_test_check():
    """Run a single test check."""
    clear_screen()
    print("🔍 RUNNING TEST CHECK")
    print("=" * 60)
    
    try:
        result = subprocess.run([
            'python', '/workspace/snowflake_demo/patients_monitor.py', '--check-once'
        ], capture_output=True, text=True, cwd='/workspace/snowflake_demo')
        print(result.stdout)
        if result.stderr:
            print("Errors:")
            print(result.stderr)
    except Exception as e:
        print(f"Error running test check: {str(e)}")
    
    input("\nPress Enter to return to dashboard...")

def main():
    """Main dashboard loop."""
    print("🏥 Starting Patients Table Monitoring Dashboard...")
    time.sleep(1)
    
    while True:
        try:
            display_dashboard()
            
            print("\nEnter command (r/s/l/t/q): ", end="", flush=True)
            choice = input().strip().lower()
            
            if choice == 'q':
                clear_screen()
                print("👋 Dashboard closed")
                break
            elif choice == 'r':
                continue  # Refresh dashboard
            elif choice == 's':
                show_full_status()
            elif choice == 'l':
                show_full_logs()
            elif choice == 't':
                run_test_check()
            else:
                print("Invalid choice. Press Enter to continue...")
                input()
                
        except KeyboardInterrupt:
            clear_screen()
            print("\n👋 Dashboard closed")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()