#!/usr/bin/env python3
"""
Setup script for PDF Question Answering with Groq
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up PDF Question Answering with Groq")
    print("=" * 50)
    
    # Check if virtual environment exists
    if not os.path.exists("venv"):
        print("❌ Virtual environment not found. Please create it first:")
        print("   python -m venv venv")
        return False
    
    # Activate virtual environment and install dependencies
    if sys.platform == "win32":
        activate_cmd = "venv\\Scripts\\activate"
        pip_cmd = "venv\\Scripts\\pip"
    else:
        activate_cmd = "source venv/bin/activate"
        pip_cmd = "venv/bin/pip"
    
    # Install requirements
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Check for API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("\n⚠️  GROQ_API_KEY not found in environment variables")
        print("Please set your API key:")
        print("   export GROQ_API_KEY='your_api_key_here'")
        print("\nOr create a .env file:")
        print("   cp env_example.txt .env")
        print("   # Edit .env and add your API key")
    else:
        print("✅ GROQ_API_KEY found in environment")
    
    print("\n🎉 Setup completed!")
    print("\nTo run the application:")
    print("   streamlit run app.py")
    
    return True

if __name__ == "__main__":
    main() 