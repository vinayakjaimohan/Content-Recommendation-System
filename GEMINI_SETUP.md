# Gemini API Integration Setup

## Overview
The content recommendation system now includes Gemini AI integration for personalized recommendations. The system will use Gemini to generate intelligent content recommendations based on user preferences and watch history.

## Setup Instructions

### 1. Get a Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key
4. Copy the API key

### 2. Configure the Backend
1. Set the environment variable for your Gemini API key:
   ```bash
   # Windows (PowerShell)
   $env:GEMINI_API_KEY="your-actual-gemini-api-key-here"
   
   # Windows (Command Prompt)
   set GEMINI_API_KEY=your-actual-gemini-api-key-here
   
   # Linux/Mac
   export GEMINI_API_KEY="your-actual-gemini-api-key-here"
   ```

2. Or update the `backend/src/main/resources/application.properties` file:
   ```properties
   gemini.api.key=your-actual-gemini-api-key-here
   ```

### 3. Start the Services
1. Start the backend:
   ```bash
   cd backend
   mvn spring-boot:run
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

### 4. Test the Integration
1. Open the application in your browser
2. Register or login
3. Go to the Dashboard
4. Select a content type (movies, books, tv, podcast)
5. Optionally select a genre
6. Add your preferences
7. Click "Get Recommendations"

## How It Works

### Frontend
- The frontend collects user preferences and watch history
- Sends this data to the backend via POST request to `/api/recommendations/gemini`
- Displays the AI-generated recommendations

### Backend
- `GeminiRecommendationService` handles the Gemini API integration
- Builds a detailed prompt based on user data
- Calls the Gemini API with the prompt
- Parses the JSON response and returns structured recommendations
- Falls back to curated recommendations if the API fails

### Gemini API
- Receives a structured prompt with user preferences and history
- Generates personalized content recommendations
- Returns results in JSON format

## API Endpoint

**POST** `/api/recommendations/gemini`

**Request Body:**
```json
{
  "type": "movies",
  "genre": "Sci-Fi",
  "preferences": "I love mind-bending plots and complex characters",
  "watchHistory": [
    {
      "title": "Inception",
      "type": "movies",
      "genre": "Sci-Fi",
      "rating": "5"
    }
  ]
}
```

**Response:**
```json
[
  {
    "id": "1",
    "title": "Interstellar",
    "type": "Sci-Fi",
    "description": "Space exploration epic with complex time concepts",
    "year": "2014",
    "rating": "4.7"
  }
]
```

## Troubleshooting

### Common Issues

1. **403 Forbidden Error**
   - Make sure the backend is running
   - Check that the security configuration allows the recommendations endpoint

2. **Gemini API Errors**
   - Verify your API key is correct
   - Check that you have sufficient API quota
   - Ensure the API key has access to Gemini Pro

3. **No Recommendations**
   - The system will fall back to curated recommendations if Gemini fails
   - Check the backend logs for error messages

### Debugging
- Check the browser console for frontend errors
- Check the backend logs for API call errors
- Verify the Gemini API key is properly set

## Fallback System
If the Gemini API is unavailable or fails, the system will automatically fall back to curated recommendations based on the selected content type and genre. This ensures users always get recommendations even if the AI service is down. 