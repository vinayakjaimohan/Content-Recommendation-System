import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import logging
import warnings
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

# Suppress scikit-learn version compatibility warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")

# --- Configure logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('recommendation_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Paths to your dataset files ---
TFIDF_VECTORIZER_PATH = 'tfidf_vectorizer.pkl'
PROCESSED_MOVIES_PATH = 'processed_movies.csv'
RATINGS_DATA_PATH = 'rating.csv'

# --- Global variables for loaded data and model components ---
tfidf_vectorizer = None
movies_df = None
ratings_df = None
content_tfidf_matrix = None

# --- Content type mappings ---
CONTENT_TYPES = {
    'movies': 'Movies',
    'tv_shows': 'TV Shows', 
    'podcasts': 'Podcasts',
    'books': 'Books'
}

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

# --- Model Loading Function (to be called once at startup) ---
def load_model_artifacts():
    global tfidf_vectorizer, movies_df, ratings_df, content_tfidf_matrix
    if tfidf_vectorizer is not None and movies_df is not None and ratings_df is not None:
        # Already loaded
        return True
    try:
        logger.info("Loading model artifacts...")
        tfidf_vectorizer = joblib.load(TFIDF_VECTORIZER_PATH)
        movies_df = pd.read_csv(PROCESSED_MOVIES_PATH)
        ratings_df = pd.read_csv(RATINGS_DATA_PATH)

        # Ensure movieId in ratings_df is int for merging
        ratings_df['movieId'] = ratings_df['movieId'].astype(int)
        movies_df['movieId'] = movies_df['movieId'].astype(int)

        # Re-generate the content TF-IDF matrix from the loaded movies_df
        content_tfidf_matrix = tfidf_vectorizer.transform(movies_df['combined_features'])

        logger.info("Model artifacts and data loaded successfully.")
        logger.info(f"Loaded movies_df shape: {movies_df.shape}")
        logger.info(f"Loaded ratings_df shape: {ratings_df.shape}")
        logger.info(f"Re-generated content_tfidf_matrix shape: {content_tfidf_matrix.shape}")
        return True
    except FileNotFoundError as e:
        logger.error(f"Error loading model artifacts: {e.filename}. Make sure they are in the correct directory.")
        logger.error("Please ensure 'tfidf_vectorizer.pkl', 'processed_movies.csv', and 'ratings.csv' are present.")
        return False
    except Exception as e:
        logger.error(f"An unexpected error occurred during model loading: {e}")
        return False

# --- User Profile Representation Function ---
def get_user_profile_vector(user_id, min_rating_threshold=4.0):
    if ratings_df is None or movies_df is None or tfidf_vectorizer is None:
        logger.error("Error: Data or vectorizer not loaded for user profile generation.")
        return None

    user_highly_rated_movies = ratings_df[
        (ratings_df['userId'] == user_id) &
        (ratings_df['rating'] >= min_rating_threshold)
    ]

    if user_highly_rated_movies.empty:
        logger.info(f"User {user_id} has no movies rated {min_rating_threshold} or higher.")
        return None

    highly_rated_movie_ids = user_highly_rated_movies['movieId'].tolist()
    liked_movies_data = movies_df[movies_df['movieId'].isin(highly_rated_movie_ids)]

    if liked_movies_data.empty:
        logger.warning(f"No content data found for highly-rated movies of user {user_id}.")
        return None

    liked_movie_indices = liked_movies_data.index.tolist()
    liked_content_vectors = content_tfidf_matrix[liked_movie_indices]

    ratings_map = user_highly_rated_movies.set_index('movieId')['rating'].to_dict()
    weights = np.array([ratings_map[mid] for mid in liked_movies_data['movieId']])

    if weights.sum() > 0:
        weights = weights / weights.sum()
    else:
        weights = np.ones_like(weights) / len(weights)

    weighted_vectors = liked_content_vectors.multiply(weights[:, np.newaxis])
    user_profile_vector = weighted_vectors.sum(axis=0)
    return user_profile_vector

# --- Enhanced Recommendation Generation Function ---
def get_recommendations_ml(user_id, content_type=None, category_filter=None, num_recommendations=5):
    user_profile_vector = get_user_profile_vector(user_id)

    if user_profile_vector is None:
        logger.info(f"No specific profile for user {user_id} (no high ratings), returning a random sample of content.")
        random_sample_df = movies_df.sample(n=num_recommendations)
        formatted_sample = []
        for idx, item in random_sample_df.iterrows():
            formatted_sample.append({
                'id': str(item['movieId']),
                'title': item['title'],
                'category': 'Movies',
                'content_type': 'movies',
                'genre': item['genres'].replace('|', ', '),
                'description': f"Genres: {item['genres'].replace('|', ', ')}",
                'similarity_score': 0.0
            })
        return formatted_sample

    # --- CRITICAL FIX: Convert user_profile_vector to numpy array ---
    user_profile_vector_np = user_profile_vector.toarray() if hasattr(user_profile_vector, 'toarray') else np.asarray(user_profile_vector)

    similarity_scores = cosine_similarity(user_profile_vector_np, content_tfidf_matrix).flatten()
    sorted_indices = similarity_scores.argsort()[::-1]

    recommended_items = []
    seen_movie_ids = set()
    user_rated_movie_ids = set(ratings_df[ratings_df['userId'] == user_id]['movieId'].tolist())

    for idx in sorted_indices:
        movie_id = movies_df.iloc[idx]['movieId']

        if movie_id in seen_movie_ids or movie_id in user_rated_movie_ids:
            continue

        item = movies_df.iloc[idx].to_dict()

        # Determine content type based on genre or other criteria
        item_content_type = determine_content_type(item['genres'])
        
        # Apply content type filter if specified
        if content_type and item_content_type != content_type:
            continue

        # Apply category filter if specified
        item_category = 'Movies'  # Default for now
        if category_filter and item_category != category_filter:
            continue

        recommended_items.append({
            'id': str(item['movieId']),
            'title': item['title'],
            'category': item_category,
            'content_type': item_content_type,
            'genre': item['genres'].replace('|', ', '),
            'description': f"Genres: {item['genres'].replace('|', ', ')}",
            'similarity_score': float(similarity_scores[idx])
        })
        seen_movie_ids.add(movie_id)

        if len(recommended_items) >= num_recommendations:
            break

    return recommended_items

# --- Content Type Determination Function ---
def determine_content_type(genres):
    """Determine content type based on genres or other criteria"""
    genres_lower = genres.lower()
    
    # This is a simple heuristic - in a real system, you'd have separate datasets
    if any(genre in genres_lower for genre in ['documentary', 'reality-tv']):
        return 'tv_shows'
    elif any(genre in genres_lower for genre in ['news', 'talk-show']):
        return 'podcasts'
    elif any(genre in genres_lower for genre in ['biography', 'history']):
        return 'books'
    else:
        return 'movies'  # Default to movies

# --- Get user statistics with content type breakdown ---
def get_user_stats(user_id):
    if ratings_df is None:
        return None
    
    user_ratings = ratings_df[ratings_df['userId'] == user_id]
    if user_ratings.empty:
        return {
            'total_ratings': 0,
            'average_rating': 0,
            'high_ratings': 0,
            'favorite_genres': [],
            'content_type_breakdown': {
                'movies': 0,
                'tv_shows': 0,
                'podcasts': 0,
                'books': 0
            }
        }
    
    total_ratings = len(user_ratings)
    average_rating = user_ratings['rating'].mean()
    high_ratings = len(user_ratings[user_ratings['rating'] >= 4.0])
    
    # Get favorite genres
    highly_rated_movies = user_ratings[user_ratings['rating'] >= 4.0]['movieId'].tolist()
    if highly_rated_movies:
        liked_movies = movies_df[movies_df['movieId'].isin(highly_rated_movies)]
        if not liked_movies.empty:
            all_genres = []
            content_type_counts = {'movies': 0, 'tv_shows': 0, 'podcasts': 0, 'books': 0}
            
            for idx, movie in liked_movies.iterrows():
                all_genres.extend(movie['genres'].split('|'))
                content_type = determine_content_type(movie['genres'])
                content_type_counts[content_type] += 1
            
            genre_counts = pd.Series(all_genres).value_counts()
            favorite_genres = genre_counts.head(5).index.tolist()
        else:
            favorite_genres = []
            content_type_counts = {'movies': 0, 'tv_shows': 0, 'podcasts': 0, 'books': 0}
    else:
        favorite_genres = []
        content_type_counts = {'movies': 0, 'tv_shows': 0, 'podcasts': 0, 'books': 0}
    
    return {
        'total_ratings': int(total_ratings),
        'average_rating': float(average_rating),
        'high_ratings': int(high_ratings),
        'favorite_genres': favorite_genres,
        'content_type_breakdown': content_type_counts
    }

# --- Flask API Endpoints ---

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": tfidf_vectorizer is not None and movies_df is not None,
        "supported_content_types": list(CONTENT_TYPES.keys())
    })

@app.route('/recommend', methods=['POST'])
def recommend():
    """Main recommendation endpoint with content type support"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user_id = data.get('userId')
        content_type = data.get('contentType', None)  # New parameter
        category_filter = data.get('categoryFilter', None)
        num_recommendations = data.get('numRecommendations', 5)

        if user_id is None:
            return jsonify({"error": "userId is required"}), 400

        # Validate content type if provided
        if content_type and content_type not in CONTENT_TYPES:
            return jsonify({"error": f"Invalid content type. Supported types: {list(CONTENT_TYPES.keys())}"}), 400

        # Validate user_id is an integer
        try:
            user_id = int(user_id)
        except (ValueError, TypeError):
            return jsonify({"error": "userId must be a valid integer"}), 400

        if not load_model_artifacts():
            return jsonify({"error": "Model not loaded. Server might be initializing."}), 500

        logger.info(f"Generating recommendations for user {user_id}, content type: {content_type}")
        recommendations = get_recommendations_ml(user_id, content_type, category_filter, num_recommendations)
        
        return jsonify({
            "recommendations": recommendations,
            "user_id": user_id,
            "content_type": content_type,
            "count": len(recommendations)
        })
    
    except Exception as e:
        logger.error(f"Error in recommend endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/user/<int:user_id>/stats', methods=['GET'])
def user_stats(user_id):
    """Get user statistics with content type breakdown"""
    try:
        if not load_model_artifacts():
            return jsonify({"error": "Model not loaded"}), 500
        
        stats = get_user_stats(user_id)
        if stats is None:
            return jsonify({"error": "Unable to get user stats"}), 500
        
        return jsonify({
            "user_id": user_id,
            "stats": stats
        })
    
    except Exception as e:
        logger.error(f"Error in user_stats endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/content/types', methods=['GET'])
def get_content_types():
    """Get supported content types"""
    return jsonify({
        "content_types": CONTENT_TYPES,
        "description": "Supported content types for recommendations"
    })

@app.route('/content/search', methods=['GET'])
def search_content():
    """Search content by title across all types"""
    try:
        query = request.args.get('q', '').lower()
        content_type = request.args.get('type', None)  # Optional content type filter
        limit = int(request.args.get('limit', 10))
        
        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400
        
        if not load_model_artifacts():
            return jsonify({"error": "Model not loaded"}), 500
        
        # Search in movies data (extend this for other content types)
        matching_content = movies_df[movies_df['title'].str.lower().str.contains(query, na=False)]
        
        results = []
        for idx, item in matching_content.head(limit).iterrows():
            content_type_detected = determine_content_type(item['genres'])
            
            # Apply content type filter if specified
            if content_type and content_type_detected != content_type:
                continue
            
            results.append({
                'id': str(item['movieId']),
                'title': item['title'],
                'content_type': content_type_detected,
                'genre': item['genres'].replace('|', ', '),
                'description': f"Genres: {item['genres'].replace('|', ', ')}"
            })
        
        return jsonify({
            "query": query,
            "content_type_filter": content_type,
            "results": results,
            "count": len(results)
        })
    
    except Exception as e:
        logger.error(f"Error in search_content endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/content/popular', methods=['GET'])
def get_popular_content():
    """Get popular content with content type filtering"""
    try:
        content_type = request.args.get('type', None)
        limit = int(request.args.get('limit', 10))
        
        if not load_model_artifacts():
            return jsonify({"error": "Model not loaded"}), 500
        
        # Calculate average rating and count for each item
        content_stats = ratings_df.groupby('movieId').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        content_stats.columns = ['movieId', 'avg_rating', 'rating_count']
        
        # Filter content with minimum ratings and sort by average rating
        popular_content = content_stats[content_stats['rating_count'] >= 10].sort_values('avg_rating', ascending=False)
        
        # Get content details
        popular_content_ids = popular_content.head(limit)['movieId'].tolist()
        popular_content_data = movies_df[movies_df['movieId'].isin(popular_content_ids)]
        
        results = []
        for content_id in popular_content_ids:
            content_data = popular_content_data[popular_content_data['movieId'] == content_id]
            if not content_data.empty:
                content_row = content_data.iloc[0]
                stats_row = popular_content[popular_content['movieId'] == content_id].iloc[0]
                
                content_type_detected = determine_content_type(content_row['genres'])
                
                # Apply content type filter if specified
                if content_type and content_type_detected != content_type:
                    continue
                
                results.append({
                    'id': str(content_row['movieId']),
                    'title': content_row['title'],
                    'content_type': content_type_detected,
                    'genre': content_row['genres'].replace('|', ', '),
                    'avg_rating': float(stats_row['avg_rating']),
                    'rating_count': int(stats_row['rating_count'])
                })
        
        return jsonify({
            "content_type_filter": content_type,
            "popular_content": results,
            "count": len(results)
        })
    
    except Exception as e:
        logger.error(f"Error in get_popular_content endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# --- Server Initialization ---
if __name__ == '__main__':
    logger.info("Loading model components...")
    if load_model_artifacts():
        logger.info("Model components loaded successfully. Starting Flask app...")
        app.run(debug=True, port=5000, host='0.0.0.0')
    else:
        logger.error("Failed to load model components. Flask app will not start.")