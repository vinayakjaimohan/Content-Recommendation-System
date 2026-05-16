import requests
import json

# Your Gemini API key
API_KEY = "AIzaSyBVi71_yWahv3k7c5uI2dqyAM-c-WEa8Zo"

# Gemini API endpoint
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

# Build the prompt like the backend does
contentType = "movies"
genre = "Sci-Fi"
preferences = "I love mind-bending plots and complex characters"
watchHistory = []

prompt = f"""You are a content recommendation expert. Based on the following information, provide 5 personalized recommendations in JSON format.

Content Type: {contentType}
Preferred Genre: {genre}
User Preferences: {preferences}

Please provide recommendations in this exact JSON format:
[
  {{
    "id": "unique_id",
    "title": "Title of the content",
    "type": "Genre",
    "description": "Brief description of why this is recommended",
    "year": "Year of release (if applicable)",
    "rating": "Average rating if known"
  }}
]

Make sure the recommendations are diverse, high-quality, and match the user's preferences and history. Only return valid JSON, no additional text."""

# Prepare the request body
data = {
    "contents": [
        {
            "parts": [
                {
                    "text": prompt
                }
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.7,
        "topK": 40,
        "topP": 0.95,
        "maxOutputTokens": 2048
    }
}

headers = {
    "Content-Type": "application/json"
}

try:
    print("Testing Gemini API with backend-style prompt...")
    print(f"URL: {url}")
    print(f"Prompt: {prompt}")
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
            
            # Try to extract JSON
            start = text.find('[')
            end = text.rfind(']')
            if start != -1 and end != -1 and end > start:
                json_text = text[start:end + 1]
                print(f"Extracted JSON: {json_text}")
                try:
                    parsed = json.loads(json_text)
                    print(f"Parsed recommendations: {json.dumps(parsed, indent=2)}")
                except json.JSONDecodeError as e:
                    print(f"JSON parsing error: {e}")
            else:
                print("No JSON found in response")
    else:
        print("❌ Gemini API failed!")
        print(f"Error: {response.text}")
        
except Exception as e:
    print(f"❌ Error testing Gemini API: {e}") 