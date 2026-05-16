import requests
import json

# Your Gemini API key
API_KEY = "AIzaSyBVi71_yWahv3k7c5uI2dqyAM-c-WEa8Zo"

# First, let's check available models
models_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

print("Checking available models...")
try:
    models_response = requests.get(models_url)
    print(f"Models Status Code: {models_response.status_code}")
    print(f"Available models: {models_response.text}")
except Exception as e:
    print(f"Error checking models: {e}")

# Gemini API endpoint - try different model names
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# Test prompt
data = {
    "contents": [
        {
            "parts": [
                {
                    "text": "Hello! Can you give me a simple movie recommendation?"
                }
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.7,
        "topK": 40,
        "topP": 0.95,
        "maxOutputTokens": 1024
    }
}

headers = {
    "Content-Type": "application/json"
}

try:
    print("Testing Gemini API...")
    print(f"URL: {url}")
    print(f"Request data: {json.dumps(data, indent=2)}")
    
    response = requests.post(url, headers=headers, json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Gemini API is working!")
        if "candidates" in result and len(result["candidates"]) > 0:
            text = result["candidates"][0]["content"]["parts"][0]["text"]
            print(f"Response text: {text}")
    else:
        print("❌ Gemini API failed!")
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"❌ Error testing Gemini API: {e}") 