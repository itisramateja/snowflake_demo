# 🏥 Patients Table Monitoring System

This monitoring system continuously scans the `development.patients.patients` table every hour and alerts you when new records are inserted, deleted, or modified.

## 🚀 Quick Start

### Start Monitoring
```bash
python start_monitoring.py
```

### View Dashboard
```bash
python monitoring_dashboard.py
```

### Check Status
```bash
python start_monitoring.py --status
```

### Stop Monitoring
```bash
python start_monitoring.py --stop
```

## 📋 Available Scripts

### 1. `patients_monitor.py` - Core Monitoring Engine
The main monitoring script that runs continuously and checks for changes.

**Usage:**
```bash
# Start continuous monitoring (runs every hour)
python patients_monitor.py

# Run a single check and exit
python patients_monitor.py --check-once

# Show current status
python patients_monitor.py --status

# Custom check interval (in seconds)
python patients_monitor.py --interval 1800  # Check every 30 minutes
```

### 2. `start_monitoring.py` - Management Script
Easy-to-use script for starting, stopping, and managing the monitoring process.

**Usage:**
```bash
# Start monitoring in background
python start_monitoring.py

# Check if monitoring is running
python start_monitoring.py --status

# Stop all monitoring processes
python start_monitoring.py --stop

# View recent log entries
python start_monitoring.py --logs
```

### 3. `monitoring_dashboard.py` - Interactive Dashboard
Real-time dashboard showing monitoring status, alerts, and recent activity.

**Features:**
- Live monitoring status
- Recent alerts and changes
- Current record count and statistics
- Interactive controls for testing and management

**Dashboard Controls:**
- `r` - Refresh dashboard
- `s` - Show full status
- `l` - Show full logs
- `t` - Run test check
- `q` - Quit dashboard

## 🔍 What Gets Monitored

The system tracks:
- **Record Count Changes**: Detects when records are added or deleted
- **New Records**: Identifies specific new records by ID
- **Record Modifications**: Detects changes to existing record data
- **Table State**: Maintains complete state history

## 📊 Monitoring Details

### Check Frequency
- **Default**: Every 1 hour (3600 seconds)
- **Customizable**: Use `--interval` parameter to change frequency

### Detection Logic
1. **New Records**: Compares current record count with previous count
2. **Deleted Records**: Detects when record count decreases
3. **Modified Records**: Compares record content even when count is same
4. **State Tracking**: Maintains JSON state file with complete record history

### Alert Types
- 🚨 **NEW RECORDS DETECTED**: When new records are added
- ⚠️ **RECORDS DELETED**: When records are removed
- 📝 **Records Modified**: When existing records are changed
- ✅ **No Changes**: When no changes are detected

## 📁 Files Created

### Log Files
- `patients_monitor.log` - Detailed monitoring logs with timestamps
- `monitor_state.json` - Current state tracking file

### State Information
The state file contains:
```json
{
  "timestamp": "2025-06-10T15:49:35.900000",
  "record_count": 6,
  "max_id": 6,
  "records": [
    {"id": 1, "name": "ram"},
    {"id": 2, "name": "ramw"},
    ...
  ]
}
```

## 🔧 Configuration

### Environment Variables
The monitoring system uses the same Snowflake credentials from your `.env` file:
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_ROLE`

### Customization Options
- **Check Interval**: Modify the `check_interval` parameter
- **Alert Methods**: Extend the `send_alert()` method to add email, Slack, SMS, etc.
- **Monitored Tables**: Modify queries to monitor different tables
- **Log Level**: Adjust logging configuration for more/less detail

## 📈 Example Monitoring Session

```bash
# Start monitoring
$ python start_monitoring.py
🚀 Starting Patients Table Monitoring...
✅ Monitoring started successfully!
🆔 Process ID: 12345

# Check status
$ python start_monitoring.py --status
📊 PATIENTS TABLE MONITORING STATUS
==================================================
Monitoring Active: True
Last Check: 2025-06-10 15:49:35
Next Check: 2025-06-10 16:49:35
Current Record Count: 6
Max ID: 6

# View dashboard
$ python monitoring_dashboard.py
🏥 PATIENTS TABLE MONITORING DASHBOARD
================================================================================
Last Updated: 2025-06-10 15:50:00

🔄 MONITORING STATUS
----------------------------------------
✅ Status: RUNNING (PID: 12345)
📊 Current Record Count: 6
🆔 Max ID: 6
🕐 Last Check: 2025-06-10 15:49:35
⏰ Next Check: 2025-06-10 16:49:35
⏳ Time Until Next Check: 59 minutes
```

## 🚨 Alert Examples

### New Records Detected
```
================================================================================
PATIENTS TABLE MONITORING ALERT - 2025-06-10 16:49:35
================================================================================
🚨 NEW RECORDS DETECTED! 2 new record(s) added

📋 New Records Details:
   1. ID: 7, Name: john
   2. ID: 8, Name: jane

📊 Count Summary:
   Previous Count: 6
   Current Count: 8
   Records Added: 2
```

### Records Deleted
```
================================================================================
PATIENTS TABLE MONITORING ALERT - 2025-06-10 17:49:35
================================================================================
⚠️ RECORDS DELETED! 1 record(s) removed

📊 Count Summary:
   Previous Count: 8
   Current Count: 7
```

## 🛠️ Troubleshooting

### Common Issues

1. **Connection Errors**
   - Check `.env` file credentials
   - Verify Snowflake account access
   - Ensure warehouse is running

2. **Permission Errors**
   - Verify user has SELECT permissions on patients table
   - Check role permissions

3. **Process Not Running**
   - Use `python start_monitoring.py --status` to check
   - Check log file for error messages
   - Restart with `python start_monitoring.py`

### Log Analysis
```bash
# View recent logs
tail -f patients_monitor.log

# Search for errors
grep -i error patients_monitor.log

# View alerts only
grep -i alert patients_monitor.log
```

## 🔒 Security Notes

- Credentials are stored securely in `.env` file
- No sensitive data is logged
- State file contains only record IDs and names
- All connections use encrypted HTTPS

## 📞 Support

If you encounter issues:
1. Check the log file: `patients_monitor.log`
2. Run a test check: `python patients_monitor.py --check-once`
3. Verify Snowflake connectivity with existing scripts
4. Check process status: `python start_monitoring.py --status`

---

**Happy Monitoring! 🏥📊**