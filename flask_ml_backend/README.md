# Flask ML Backend - Multi-Content Recommendation System

A sophisticated content recommendation system that provides personalized recommendations for **movies**, **TV shows**, **podcasts**, and **books** using content-based filtering with TF-IDF vectorization.

## 🎯 **Features**

### **Multi-Content Support**
- ✅ **Movies** - Feature films and documentaries
- ✅ **TV Shows** - Series, reality TV, and episodic content  
- ✅ **Podcasts** - Audio content and talk shows
- ✅ **Books** - Literature, biographies, and educational content

### **Advanced ML Features**
- **Content-based filtering** using TF-IDF vectorization
- **User profile generation** from rating history
- **Cosine similarity** for content recommendations
- **Genre-based analysis** for user preferences
- **Content type classification** based on genres and metadata

### **Comprehensive API**
- **Health monitoring** with content type support
- **Personalized recommendations** with content type filtering
- **User statistics** with content breakdown
- **Content search** across all types
- **Popular content** discovery
- **Error handling** and validation

## 🚀 **Quick Start**

### **1. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **2. Start the Server**
```bash
python start_server.py
```

### **3. Test the API**
```bash
python test_multi_content.py
```

## 📊 **API Endpoints**

### **Core Endpoints**

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check and supported content types |
| `/recommend` | POST | Get personalized recommendations with content type filtering |
| `/user/{id}/stats` | GET | Get user statistics with content type breakdown |
| `/content/types` | GET | Get supported content types |
| `/content/search` | GET | Search content across all types |
| `/content/popular` | GET | Get popular content with type filtering |

### **Example Usage**

#### **Get Movie Recommendations**
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"userId": 1, "contentType": "movies", "numRecommendations": 5}'
```

#### **Get TV Show Recommendations**
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"userId": 1, "contentType": "tv_shows", "numRecommendations": 3}'
```

#### **Get Podcast Recommendations**
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"userId": 1, "contentType": "podcasts", "numRecommendations": 3}'
```

#### **Get Book Recommendations**
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"userId": 1, "contentType": "books", "numRecommendations": 3}'
```

#### **Search Content by Type**
```bash
curl "http://localhost:5000/content/search?q=star&type=movies&limit=5"
```

#### **Get Popular Content by Type**
```bash
curl "http://localhost:5000/content/popular?type=tv_shows&limit=5"
```

## 🧠 **ML Model Architecture**

### **Content Type Classification**
The system automatically classifies content based on genres:
- **Movies**: Action, Comedy, Drama, Horror, etc.
- **TV Shows**: Documentary, Reality-TV, Talk-Show
- **Podcasts**: News, Talk-Show, Educational
- **Books**: Biography, History, Educational

### **Recommendation Process**
1. **User Profile Generation**: Analyzes highly-rated content (rating ≥ 4.0)
2. **Content Type Filtering**: Filters by requested content type
3. **Similarity Calculation**: Uses cosine similarity between user profile and content
4. **Recommendation Ranking**: Returns top similar content with similarity scores

## 🧪 **Testing**

### **Comprehensive Testing**
```bash
# Test all multi-content features
python test_multi_content.py

# Test basic API functionality
python test_api.py

# Test user-specific features
python test_users.py
```

### **Interactive Testing**
```bash
# Run interactive demo
python example_client.py

# Run interactive mode
python example_client.py interactive
```

## 📈 **Response Examples**

### **Health Check Response**
```json
{
  "status": "healthy",
  "timestamp": "2025-07-31T20:33:51.831693",
  "model_loaded": true,
  "supported_content_types": ["movies", "tv_shows", "podcasts", "books"]
}
```

### **Recommendation Response**
```json
{
  "recommendations": [
    {
      "id": "123",
      "title": "The Shawshank Redemption",
      "content_type": "movies",
      "category": "Movies",
      "genre": "Drama",
      "description": "Genres: Drama",
      "similarity_score": 0.85
    }
  ],
  "user_id": 1,
  "content_type": "movies",
  "count": 1
}
```

### **User Stats Response**
```json
{
  "user_id": 1,
  "stats": {
    "total_ratings": 175,
    "average_rating": 3.74,
    "high_ratings": 88,
    "favorite_genres": ["Adventure", "Fantasy", "Action"],
    "content_type_breakdown": {
      "movies": 120,
      "tv_shows": 25,
      "podcasts": 15,
      "books": 15
    }
  }
}
```

## 🔧 **Configuration**

### **Content Type Mappings**
```python
CONTENT_TYPES = {
    'movies': 'Movies',
    'tv_shows': 'TV Shows', 
    'podcasts': 'Podcasts',
    'books': 'Books'
}
```

### **Content Classification Rules**
```python
def determine_content_type(genres):
    genres_lower = genres.lower()
    
    if any(genre in genres_lower for genre in ['documentary', 'reality-tv']):
        return 'tv_shows'
    elif any(genre in genres_lower for genre in ['news', 'talk-show']):
        return 'podcasts'
    elif any(genre in genres_lower for genre in ['biography', 'history']):
        return 'books'
    else:
        return 'movies'
```

## 🚀 **Deployment**

### **Production Setup**
```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python app.py
```

### **Docker Deployment (Optional)**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📚 **Documentation**

- **API Testing**: See `test_multi_content.py`
- **Interactive Client**: See `example_client.py`
- **Troubleshooting**: See `TROUBLESHOOTING.md`
- **User Testing**: See `test_users.py`

## 🎯 **Key Benefits**

### **Multi-Content Support**
- **Unified API** for all content types
- **Content type filtering** for targeted recommendations
- **Cross-content search** capabilities
- **Content type breakdown** in user statistics

### **Advanced Features**
- **Content classification** based on genres
- **Similarity scoring** for all recommendations
- **Comprehensive error handling**
- **Production-ready logging**

### **Developer Friendly**
- **Comprehensive testing** suite
- **Interactive client** for API exploration
- **Detailed documentation**
- **Easy deployment** options

---

**Built with ❤️ using Flask, scikit-learn, and modern ML techniques for multi-content recommendations** 