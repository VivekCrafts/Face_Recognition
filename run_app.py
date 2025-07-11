#!/usr/bin/env python3
"""
Sports Personality Classifier - Startup Script
This script helps you run both the Flask backend and Streamlit frontend.
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'flask', 'flask_cors', 'streamlit', 'opencv-python', 
        'numpy', 'scikit-learn', 'joblib', 'Pillow', 'requests', 'plotly'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them using:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies are installed!")
    return True

def check_model_files():
    """Check if model files exist"""
    required_files = [
        'server/artifact/class_dictionary.json',
        'server/artifact/saved_model.pkl',
        'server/haarcascades/haarcascade_frontalface_default.xml',
        'server/haarcascades/haarcascade_eye.xml'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing model files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        print("\n📁 Make sure to extract all zip files:")
        print("   - server.zip")
        print("   - haarcascades.zip")
        return False
    
    print("✅ All model files are present!")
    return True

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting Flask backend server...")
    
    # Change to server directory
    os.chdir('server')
    
    try:
        # Start Flask server
        process = subprocess.Popen([
            sys.executable, 'server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server is running
        if process.poll() is None:
            print("✅ Flask backend is running on http://127.0.0.1:5000")
            return process
        else:
            stdout, stderr = process.communicate()
            print("❌ Failed to start Flask backend:")
            print(stderr.decode())
            return None
            
    except Exception as e:
        print(f"❌ Error starting Flask backend: {e}")
        return None

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎨 Starting Streamlit frontend...")
    
    try:
        # Start Streamlit
        process = subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
            '--server.port', '8501',
            '--server.address', '127.0.0.1'
        ])
        
        # Wait a moment for server to start
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Streamlit frontend is running on http://127.0.0.1:8501")
            return process
        else:
            print("❌ Failed to start Streamlit frontend")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Streamlit frontend: {e}")
        return None

def main():
    """Main function to start the application"""
    print("🏆 Sports Personality Classifier")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check model files
    if not check_model_files():
        return
    
    print("\n🔄 Starting application...")
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        return
    
    # Start frontend
    frontend_process = start_frontend()
    if not frontend_process:
        backend_process.terminate()
        return
    
    print("\n🎉 Application is ready!")
    print("📱 Open your browser and go to: http://127.0.0.1:8501")
    print("🔧 Backend API: http://127.0.0.1:5000")
    print("\n⏹️  Press Ctrl+C to stop both servers")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped")

if __name__ == "__main__":
    main()