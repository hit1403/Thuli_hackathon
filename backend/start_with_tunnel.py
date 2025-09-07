#!/usr/bin/env python3
"""
Simple script to start the FastAPI backend with public tunnel access
This allows mobile devices to connect to the backend from anywhere
"""

import subprocess
import sys
import time
import threading
import requests

def start_backend():
    """Start the FastAPI backend server"""
    print("🚀 Starting FastAPI backend server...")
    subprocess.run([
        sys.executable, "-m", "uvicorn", 
        "main:app", 
        "--reload", 
        "--host", "0.0.0.0", 
        "--port", "8001"
    ])

def start_ngrok():
    """Start ngrok tunnel for the backend"""
    print("🌐 Starting ngrok tunnel...")
    subprocess.run(["ngrok", "http", "8001"])

if __name__ == "__main__":
    print("=" * 50)
    print("StyleGenius Backend with Tunnel")
    print("=" * 50)
    
    # Check if ngrok is installed
    try:
        subprocess.run(["ngrok", "version"], capture_output=True, check=True)
        print("✅ ngrok is available")
        
        # Start backend in a separate thread
        backend_thread = threading.Thread(target=start_backend)
        backend_thread.daemon = True
        backend_thread.start()
        
        # Wait a moment for backend to start
        time.sleep(3)
        
        # Start ngrok tunnel
        print("\n🌐 Starting public tunnel...")
        print("📱 Your mobile device will be able to connect via the ngrok URL")
        start_ngrok()
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ ngrok not found. Installing ngrok...")
        print("\nPlease install ngrok:")
        print("1. Download from: https://ngrok.com/download")
        print("2. Extract and add to PATH")
        print("3. Run: ngrok authtoken YOUR_TOKEN")
        print("\nAlternatively, just start the backend normally:")
        start_backend()
