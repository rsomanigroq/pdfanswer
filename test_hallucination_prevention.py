#!/usr/bin/env python3
"""
Test script to verify hallucination prevention features
"""

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    print("❌ GROQ_API_KEY not found in environment variables")
    exit(1)

client = Groq(api_key=groq_api_key)

def test_confidence_scoring():
    """Test confidence scoring function"""
    print("🧪 Testing Confidence Scoring...")
    
    # Import the function from app.py
    import sys
    sys.path.append('.')
    
    # Mock context and question
    context = "The document discusses climate change. The main findings show that global temperatures have increased by 1.1°C since pre-industrial times."
    question = "What is the main topic of this document?"
    
    try:
        # Import and test the function
        from app import ask_groq_with_confidence
        
        result = ask_groq_with_confidence(context, question)
        
        print(f"✅ Answer: {result['answer']}")
        print(f"✅ Confidence: {result['confidence']}")
        print(f"✅ Reasoning: {result['reasoning']}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing confidence scoring: {e}")
        return False

def test_source_citations():
    """Test source citation function"""
    print("\n🧪 Testing Source Citations...")
    
    # Mock context and question
    context = "The document discusses climate change. The main findings show that global temperatures have increased by 1.1°C since pre-industrial times."
    question = "What is the main topic of this document?"
    
    try:
        # Import and test the function
        from app import ask_groq_with_sources
        
        result = ask_groq_with_sources(context, question)
        
        print(f"✅ Answer: {result['answer']}")
        print(f"✅ Sources: {result['sources']}")
        print(f"✅ Confidence: {result['confidence']}")
        
        return True
    except Exception as e:
        print(f"❌ Error testing source citations: {e}")
        return False

def test_hallucination_detection():
    """Test hallucination detection with non-existent information"""
    print("\n🧪 Testing Hallucination Detection...")
    
    # Mock context and question about non-existent information
    context = "The document discusses climate change. The main findings show that global temperatures have increased by 1.1°C since pre-industrial times."
    question = "What is the author's phone number?"
    
    try:
        from app import ask_groq_with_confidence
        
        result = ask_groq_with_confidence(context, question)
        
        print(f"✅ Answer: {result['answer']}")
        print(f"✅ Confidence: {result['confidence']}")
        print(f"✅ Reasoning: {result['reasoning']}")
        
        # Check if it properly detected no information
        if "cannot find" in result['answer'].lower() or result['confidence'] == "LOW":
            print("✅ Hallucination detection working correctly")
            return True
        else:
            print("⚠️ Hallucination detection may need improvement")
            return False
            
    except Exception as e:
        print(f"❌ Error testing hallucination detection: {e}")
        return False

def main():
    print("🛡️ Testing Hallucination Prevention Features")
    print("=" * 50)
    
    # Test confidence scoring
    confidence_ok = test_confidence_scoring()
    
    # Test source citations
    sources_ok = test_source_citations()
    
    # Test hallucination detection
    hallucination_ok = test_hallucination_detection()
    
    print("\n" + "=" * 50)
    if confidence_ok and sources_ok and hallucination_ok:
        print("🎉 All hallucination prevention tests passed!")
        print("\nTo run the enhanced app:")
        print("   streamlit run app.py")
    else:
        print("❌ Some tests failed. Please check the implementation.")
    
    return confidence_ok and sources_ok and hallucination_ok

if __name__ == "__main__":
    main() 