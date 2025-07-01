#!/usr/bin/env python3
"""
Launcher script for Snowflake Cortex Analyst Streamlit App

This script provides an easy way to launch either the demo or production version.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path(".env")
    
    if not env_path.exists():
        return False
    
    required_vars = ['SNOWFLAKE_ACCOUNT', 'SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD']
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
            for var in required_vars:
                if f"{var}=" not in content:
                    return False
                # Check if variable has a real value (not template placeholder)
                for line in content.split('\n'):
                    if line.startswith(f"{var}=") and not line.endswith('='):
                        value = line.split('=', 1)[1].strip()
                        if value and not value.startswith('your_'):
                            continue
                        else:
                            return False
        return True
    except Exception:
        return False

def launch_demo(port=12000):
    """Launch the demo version."""
    print("🎯 Launching Snowflake Cortex Analyst Demo...")
    print(f"📱 Demo will be available at: http://localhost:{port}")
    print("💡 This version uses mock data and doesn't require Snowflake credentials")
    print("-" * 60)
    
    cmd = [
        sys.executable, "-m", "streamlit", "run", "demo_app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching demo: {e}")

def launch_production(port=12001):
    """Launch the production version."""
    print("🚀 Launching Snowflake Cortex Analyst (Production)...")
    print(f"📱 App will be available at: http://localhost:{port}")
    print("🔐 This version requires valid Snowflake credentials in .env file")
    print("-" * 60)
    
    cmd = [
        sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
        "--server.port", str(port),
        "--server.address", "0.0.0.0",
        "--server.headless", "true"
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching application: {e}")

def setup_environment():
    """Set up the environment and install dependencies."""
    print("📦 Setting up environment...")
    
    # Install requirements
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    
    # Check/create .env file
    if not Path(".env").exists():
        if Path(".env.template").exists():
            import shutil
            shutil.copy(".env.template", ".env")
            print("✅ Created .env file from template")
        else:
            print("❌ No .env.template found")
            return False
    
    return True

def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(description="Launch Snowflake Cortex Analyst Streamlit App")
    parser.add_argument("--mode", choices=["demo", "production", "auto"], default="auto",
                       help="Launch mode: demo (mock data), production (real Snowflake), or auto (detect)")
    parser.add_argument("--port", type=int, default=None,
                       help="Port to run the application on")
    parser.add_argument("--setup", action="store_true",
                       help="Set up environment and install dependencies")
    
    args = parser.parse_args()
    
    # Setup if requested
    if args.setup:
        if not setup_environment():
            sys.exit(1)
        print("🎉 Setup completed successfully!")
        return
    
    # Determine mode
    if args.mode == "auto":
        if check_env_file():
            mode = "production"
            default_port = 12001
        else:
            mode = "demo"
            default_port = 12000
    else:
        mode = args.mode
        default_port = 12001 if mode == "production" else 12000
    
    port = args.port or default_port
    
    # Validate production mode requirements
    if mode == "production" and not check_env_file():
        print("❌ Production mode requires valid Snowflake credentials in .env file")
        print("💡 Options:")
        print("   1. Run with --mode demo to use mock data")
        print("   2. Configure your .env file with Snowflake credentials")
        print("   3. Run with --setup to initialize the environment")
        sys.exit(1)
    
    # Launch appropriate version
    print("❄️ Snowflake Cortex Analyst Launcher")
    print("=" * 50)
    
    if mode == "demo":
        launch_demo(port)
    else:
        launch_production(port)

if __name__ == "__main__":
    main()