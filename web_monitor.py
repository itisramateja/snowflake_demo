#!/usr/bin/env python3
"""
Web-based Patients Table Monitor

This script provides a web interface for monitoring the patients table.
Access via browser at http://localhost:12000
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify
import threading
import time

app = Flask(__name__)

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

def read_log_file():
    """Read and parse the log file."""
    log_file = '/workspace/snowflake_demo/patients_monitor.log'
    
    if not os.path.exists(log_file):
        return []
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
        return [line.strip() for line in lines if line.strip()][-50:]  # Last 50 lines
    except Exception as e:
        return [f"Error reading log file: {str(e)}"]

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

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🏥 Patients Table Monitor</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        .status-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
        }
        .status-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            border-left: 5px solid #4CAF50;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .status-card.warning {
            border-left-color: #ff9800;
        }
        .status-card.error {
            border-left-color: #f44336;
        }
        .status-card h3 {
            margin: 0 0 10px 0;
            color: #333;
            font-size: 1.2em;
        }
        .status-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #4CAF50;
        }
        .status-card.warning .status-value {
            color: #ff9800;
        }
        .status-card.error .status-value {
            color: #f44336;
        }
        .logs-section {
            margin: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            overflow: hidden;
        }
        .logs-header {
            background: #343a40;
            color: white;
            padding: 15px 20px;
            font-weight: bold;
        }
        .logs-content {
            max-height: 400px;
            overflow-y: auto;
            padding: 20px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            line-height: 1.4;
        }
        .log-line {
            margin: 5px 0;
            padding: 5px;
            border-radius: 3px;
        }
        .log-line.alert {
            background: #ffebee;
            border-left: 3px solid #f44336;
        }
        .log-line.info {
            background: #e3f2fd;
            border-left: 3px solid #2196f3;
        }
        .controls {
            padding: 20px 30px;
            background: #f8f9fa;
            border-top: 1px solid #dee2e6;
            text-align: center;
        }
        .btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 0 10px;
            font-size: 1em;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #45a049;
        }
        .btn.secondary {
            background: #6c757d;
        }
        .btn.secondary:hover {
            background: #5a6268;
        }
        .auto-refresh {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 10px 15px;
            border-radius: 20px;
            font-size: 0.9em;
        }
        .timestamp {
            color: #666;
            font-size: 0.9em;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .pulse {
            animation: pulse 2s infinite;
        }
    </style>
</head>
<body>
    <div class="auto-refresh">
        🔄 Auto-refresh: <span id="countdown">30</span>s
    </div>
    
    <div class="container">
        <div class="header">
            <h1>🏥 Patients Table Monitor</h1>
            <p class="timestamp">Last Updated: <span id="last-updated">{{ last_updated }}</span></p>
        </div>
        
        <div class="status-grid">
            <div class="status-card {{ 'error' if not is_running else '' }}">
                <h3>🔄 Monitoring Status</h3>
                <div class="status-value">
                    {{ '✅ RUNNING' if is_running else '🔴 STOPPED' }}
                </div>
                {% if pids %}
                <small>PID: {{ ', '.join(pids) }}</small>
                {% endif %}
            </div>
            
            <div class="status-card">
                <h3>📊 Current Records</h3>
                <div class="status-value">{{ record_count if record_count is not none else 'Unknown' }}</div>
                <small>Total records in patients table</small>
            </div>
            
            <div class="status-card">
                <h3>🆔 Max ID</h3>
                <div class="status-value">{{ max_id if max_id is not none else 'Unknown' }}</div>
                <small>Highest patient ID</small>
            </div>
            
            <div class="status-card">
                <h3>🕐 Last Check</h3>
                <div class="status-value">{{ last_check if last_check else 'Never' }}</div>
                <small>Most recent monitoring check</small>
            </div>
            
            <div class="status-card">
                <h3>⏰ Next Check</h3>
                <div class="status-value">{{ next_check if next_check else 'Unknown' }}</div>
                <small>Scheduled next check</small>
            </div>
            
            <div class="status-card {{ 'warning' if time_until_next and time_until_next < 5 else '' }}">
                <h3>⏳ Time Until Next</h3>
                <div class="status-value">
                    {% if time_until_next is not none %}
                        {% if time_until_next > 0 %}
                            {{ time_until_next }} min
                        {% else %}
                            Overdue
                        {% endif %}
                    {% else %}
                        Unknown
                    {% endif %}
                </div>
                <small>Minutes until next check</small>
            </div>
        </div>
        
        <div class="logs-section">
            <div class="logs-header">
                📋 Recent Log Entries
            </div>
            <div class="logs-content" id="logs-content">
                {% for log in logs %}
                <div class="log-line {{ 'alert' if 'ALERT' in log or 'NEW RECORDS' in log or 'DELETED' in log else 'info' }}">
                    {{ log }}
                </div>
                {% endfor %}
            </div>
        </div>
        
        <div class="controls">
            <button class="btn" onclick="refreshData()">🔄 Refresh Now</button>
            <button class="btn secondary" onclick="runTestCheck()">🔍 Run Test Check</button>
            <button class="btn secondary" onclick="toggleAutoRefresh()">
                <span id="auto-refresh-btn">⏸️ Pause Auto-refresh</span>
            </button>
        </div>
    </div>

    <script>
        let autoRefresh = true;
        let countdown = 30;
        let countdownInterval;

        function updateCountdown() {
            document.getElementById('countdown').textContent = countdown;
            countdown--;
            
            if (countdown < 0) {
                if (autoRefresh) {
                    refreshData();
                }
                countdown = 30;
            }
        }

        function startCountdown() {
            countdownInterval = setInterval(updateCountdown, 1000);
        }

        function refreshData() {
            fetch('/api/status')
                .then(response => response.json())
                .then(data => {
                    location.reload(); // Simple refresh for now
                })
                .catch(error => {
                    console.error('Error refreshing data:', error);
                });
        }

        function runTestCheck() {
            document.querySelector('.controls').innerHTML += '<div class="pulse">🔍 Running test check...</div>';
            
            fetch('/api/test-check', { method: 'POST' })
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        refreshData();
                    }, 3000);
                })
                .catch(error => {
                    console.error('Error running test check:', error);
                });
        }

        function toggleAutoRefresh() {
            autoRefresh = !autoRefresh;
            const btn = document.getElementById('auto-refresh-btn');
            btn.textContent = autoRefresh ? '⏸️ Pause Auto-refresh' : '▶️ Resume Auto-refresh';
        }

        // Start countdown on page load
        startCountdown();

        // Auto-scroll logs to bottom
        const logsContent = document.getElementById('logs-content');
        logsContent.scrollTop = logsContent.scrollHeight;
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard page."""
    # Get monitoring status
    is_running, pids = check_process_status()
    
    # Get current state
    state = read_state_file()
    
    # Get logs
    logs = read_log_file()
    
    # Prepare data for template
    data = {
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'is_running': is_running,
        'pids': pids,
        'record_count': None,
        'max_id': None,
        'last_check': None,
        'next_check': None,
        'time_until_next': None,
        'logs': logs
    }
    
    if state:
        data['record_count'] = state['record_count']
        data['max_id'] = state['max_id']
        
        last_check = datetime.fromisoformat(state['timestamp'])
        data['last_check'] = last_check.strftime('%H:%M:%S')
        
        next_check = last_check + timedelta(hours=1)
        data['next_check'] = next_check.strftime('%H:%M:%S')
        
        time_until_next = next_check - datetime.now()
        if time_until_next.total_seconds() > 0:
            data['time_until_next'] = int(time_until_next.total_seconds() / 60)
        else:
            data['time_until_next'] = 0
    
    return render_template_string(HTML_TEMPLATE, **data)

@app.route('/api/status')
def api_status():
    """API endpoint for status data."""
    is_running, pids = check_process_status()
    state = read_state_file()
    
    return jsonify({
        'is_running': is_running,
        'pids': pids,
        'state': state,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/test-check', methods=['POST'])
def api_test_check():
    """API endpoint to run a test check."""
    try:
        result = subprocess.run([
            'python', '/workspace/snowflake_demo/patients_monitor.py', '--check-once'
        ], capture_output=True, text=True, cwd='/workspace/snowflake_demo')
        
        return jsonify({
            'success': True,
            'output': result.stdout,
            'error': result.stderr
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    print("🌐 Starting Web Monitor...")
    print("📱 Access the dashboard at: https://work-1-jltqpidwmduqrdev.prod-runtime.all-hands.dev")
    print("🔄 The dashboard will auto-refresh every 30 seconds")
    print("💡 Use Ctrl+C to stop the web server")
    
    app.run(host='0.0.0.0', port=12000, debug=False)