#!/usr/bin/env python3
"""
Launcher script for the meditation course demo bot
"""
import subprocess
import sys
import os
import time
import threading
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import aiogram
        import fastapi
        import uvicorn
        import jinja2
        import aiofiles
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has BOT_TOKEN"""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found!")
        print("Please create .env file with:")
        print("BOT_TOKEN=your_telegram_bot_token_here")
        print("WEBAPP_URL=http://localhost:8080")
        return False
    
    with open(env_path, 'r') as f:
        content = f.read()
        if 'BOT_TOKEN=' not in content or 'BOT_TOKEN=""' in content or 'BOT_TOKEN=your_telegram_bot_token_here' in content:
            print("❌ BOT_TOKEN not set in .env file!")
            print("Please add your Telegram bot token to .env file:")
            print("BOT_TOKEN=your_real_bot_token_here")
            return False
    
    print("✅ .env file configured")
    return True

def start_webapp():
    """Start the FastAPI webapp"""
    print("🚀 Starting FastAPI webapp on port 8000...")
    try:
        os.chdir(Path(__file__).parent)
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "webapp.app:app", 
            "--host", "0.0.0.0", 
            "--port", "8000",
            "--reload"
        ], check=False)
    except KeyboardInterrupt:
        print("📱 Webapp stopped")

def start_nginx():
    """Start nginx (if available)"""
    print("🌐 Starting nginx proxy on port 8080...")
    try:
        # Check if nginx is available
        result = subprocess.run(["nginx", "-v"], capture_output=True, text=True)
        if result.returncode == 0:
            subprocess.run([
                "nginx", 
                "-c", str(Path(__file__).parent / "nginx.conf"),
                "-g", "daemon off;"
            ], check=False)
        else:
            print("⚠️ nginx not available, webapp will be accessible directly on port 8000")
            print("📱 Webapp URL: http://localhost:8000")
    except FileNotFoundError:
        print("⚠️ nginx not found, webapp will be accessible directly on port 8000") 
        print("📱 Webapp URL: http://localhost:8000")
    except KeyboardInterrupt:
        print("🌐 Nginx stopped")

def start_bot():
    """Start the Telegram bot"""
    print("🤖 Starting Telegram bot...")
    try:
        os.chdir(Path(__file__).parent)
        subprocess.run([sys.executable, "main.py"], check=False)
    except KeyboardInterrupt:
        print("🤖 Bot stopped")

def main():
    """Main launcher function"""
    print("🧘‍♀️ Meditation Course Demo Bot Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check env file
    if not check_env_file():
        return

    print("\n🚀 Starting all services...")

    # Start webapp in background thread
    webapp_thread = threading.Thread(target=start_webapp, daemon=True)
    webapp_thread.start()

    # Start nginx in background thread
    nginx_thread = threading.Thread(target=start_nginx, daemon=True)
    nginx_thread.start()

    # Wait a bit for services to start
    time.sleep(3)
    print("✅ Services started!")
    print("📱 Webapp: http://localhost:8080")
    print("🤖 Starting bot...")

    start_bot()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 All services stopped. Goodbye!")
        sys.exit(0)