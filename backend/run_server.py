#!/usr/bin/env python3
"""
Startup script for StyleGenius Backend
This script handles common startup issues and provides better error messages
"""

import sys
import os
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'fastapi', 'uvicorn', 'pandas', 'numpy', 
        'scikit-learn', 'pydantic'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install " + " ".join(missing_packages))
        return False
    
    print("✅ All required packages are installed")
    return True

def check_data_file():
    """Check if the dataset file exists"""
    data_file = Path("data/fashion_with_embeddings.pkl")
    if not data_file.exists():
        print(f"❌ Dataset file not found: {data_file}")
        print("Make sure the data file is in the correct location")
        return False
    
    print("✅ Dataset file found")
    return True

def start_server():
    """Start the FastAPI server"""
    try:
        print("🚀 Starting StyleGenius Backend Server...")
        print("📡 Server will be available at: http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🛑 Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start uvicorn server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main startup function"""
    print("🎨 StyleGenius Backend Startup")
    print("=" * 40)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Run checks
    if not check_dependencies():
        sys.exit(1)
    
    if not check_data_file():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
