#!/usr/bin/env python3
"""
Setup script for Snowflake Cortex Analyst Streamlit App

This script helps set up the environment and dependencies.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages."""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_path = Path(".env")
    
    if not env_path.exists():
        print("⚠️  .env file not found. Creating from template...")
        template_path = Path(".env.template")
        if template_path.exists():
            import shutil
            shutil.copy(template_path, env_path)
            print("✅ .env file created from template.")
        else:
            print("❌ .env.template not found!")
            return False
    
    # Check if required variables are set
    required_vars = ['SNOWFLAKE_ACCOUNT', 'SNOWFLAKE_USER', 'SNOWFLAKE_PASSWORD']
    missing_vars = []
    
    with open(env_path, 'r') as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=" not in content or f"{var}=your_" in content or f"{var}=" in content.split('\n'):
                missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Please update the following variables in .env file: {', '.join(missing_vars)}")
        return False
    
    print("✅ .env file configured correctly!")
    return True

def test_connection():
    """Test Snowflake connection."""
    print("🔗 Testing Snowflake connection...")
    try:
        from cortex_analyst import CortexAnalyst
        analyst = CortexAnalyst()
        if analyst.connect():
            print("✅ Snowflake connection successful!")
            analyst.close()
            return True
        else:
            print("❌ Snowflake connection failed!")
            return False
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Snowflake Cortex Analyst Streamlit App")
    print("=" * 50)
    
    # Step 1: Install requirements
    if not install_requirements():
        print("❌ Setup failed at requirements installation.")
        return False
    
    # Step 2: Check .env file
    if not check_env_file():
        print("❌ Setup failed at .env configuration.")
        print("📝 Please edit the .env file with your Snowflake credentials and run setup again.")
        return False
    
    # Step 3: Test connection
    if not test_connection():
        print("❌ Setup failed at connection test.")
        print("📝 Please verify your Snowflake credentials in the .env file.")
        return False
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the Streamlit app: streamlit run streamlit_app.py")
    print("2. Open your browser and navigate to the provided URL")
    print("3. Start asking questions in natural language!")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)