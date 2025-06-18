#!/usr/bin/env python3
"""
Test script to verify setup for PDF Question Answering with Groq
"""

import sys
import os

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import streamlit
        print("✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Streamlit: {e}")
        return False
    
    try:
        import groq
        print("✅ Groq imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Groq: {e}")
        return False
    
    try:
        import PyPDF2
        print("✅ PyPDF2 imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import PyPDF2: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    return True

def test_groq_api():
    """Test if Groq API key is set and working"""
    print("\n🔍 Testing Groq API...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        return False
    
    print("✅ GROQ_API_KEY found")
    
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        # Test with a simple completion
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": "Hello, this is a test."}],
            model="llama3-8b-8192",
            max_tokens=10
        )
        
        print("✅ Groq API connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Groq API test failed: {e}")
        return False

def test_pdf_processing():
    """Test PDF processing capabilities"""
    print("\n🔍 Testing PDF processing...")
    
    try:
        from PyPDF2 import PdfReader
        print("✅ PyPDF2 can be used for PDF processing")
        return True
    except Exception as e:
        print(f"❌ PDF processing test failed: {e}")
        return False

def main():
    print("🧪 Testing PDF Question Answering Setup")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed. Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False
    
    # Test Groq API
    if not test_groq_api():
        print("\n❌ Groq API test failed. Please check your API key.")
        return False
    
    # Test PDF processing
    if not test_pdf_processing():
        print("\n❌ PDF processing test failed.")
        return False
    
    print("\n🎉 All tests passed! Your setup is ready.")
    print("\nTo run the application:")
    print("   streamlit run app.py")
    
    return True

if __name__ == "__main__":
    main() 