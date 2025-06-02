#!/usr/bin/env python3
"""
This is a simple test script to verify OpenAI API connection
Run this in your project directory with python3 test_openai.py
"""

import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

def test_openai_connection():
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        print("Please check your .env file")
        return False
    
    if not api_key.startswith('sk-'):
        print("❌ API key doesn't look valid (should start with 'sk-')")
        return False
    
    print(f"✅ Found API key: {api_key[:10]}...")
    
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # Test with a simple request
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say 'API test successful'"}],
            max_tokens=10
        )
        
        print("✅ OpenAI API connection successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except openai.AuthenticationError:
        print("❌ Authentication failed - invalid API key")
        return False
    except openai.RateLimitError:
        print("❌ Rate limit exceeded - please wait and try again")
        return False
    except openai.APIConnectionError:
        print("❌ Network connection error")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing OpenAI API connection...")
    test_openai_connection()
