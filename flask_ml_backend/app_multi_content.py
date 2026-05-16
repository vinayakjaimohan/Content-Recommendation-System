#!/usr/bin/env python3
"""
Enhanced Multi-Content Recommendation System
Handles real datasets for movies, TV shows, podcasts, and books
"""

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
        logging.FileHandler('multi_content_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Paths to dataset files ---
TFIDF_VECTORIZER_PATH = 'tfidf_vectorizer.pkl'
MOVIES_PATH = 'processed_movies.csv'
TV_SHOWS_PATH = 'tv_shows.csv'
PODCASTS_PATH = 'podcasts.csv'
BOOKS_PATH = 'books.csv'
COMBINED_CONTENT_PATH = 'combined_content.csv'
MULTI_CONTENT_RATINGS_PATH = 'multi_content_ratings.csv'

# --- Global variables for loaded data and model components ---
tfidf_vectorizer = None
content_dfs = {}  # Dictionary to store different content type dataframes
ratings_df = None
content_tfidf_matrices = {}  # Dictionary to store TF-IDF matrices for each content type

# --- Content type mappings ---
CONTENT_TYPES = {
    'movies': 'Movies',
    'tv_shows': 'TV Shows', 
    'podcasts': 'Podcasts',
    'books': 'Books'
}

app = Flask(__name__)
CORS(app)

# --- Model Loading Function ---
def load_multi_content_artifacts():
    """Load all multi-content datasets and models"""
    global tfidf_vectorizer, content_dfs, ratings_df, content_tfidf_matrices
    
    try:
        logger.info("Loading multi-content model artifacts...")
        
        # Load TF-IDF vectorizer
        if os.path.exists(TFIDF_VECTORIZER_PATH):
            tfidf_vectorizer = joblib.load(TFIDF_VECTORIZER_PATH)
        else:
            logger.warning("TF-IDF vectorizer not found, will create new one")
            tfidf_vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
        
        # Load content datasets
        content_dfs = {}
        
        # Load movies (existing dataset)
        if os.path.exists(MOVIES_PATH):
            movies_df = pd.read_csv(MOVIES_PATH)
            movies_df['content_type'] = 'movies'
            content_dfs['movies'] = movies_df
            logger.info(f"Loaded movies: {len(movies_df)} items")
        
        # Load TV shows
        if os.path.exists(TV_SHOWS_PATH):
            tv_shows_df = pd.read_csv(TV_SHOWS_PATH)
            tv_shows_df['content_type'] = 'tv_shows'
            content_dfs['tv_shows'] = tv_shows_df
            logger.info(f"Loaded TV shows: {len(tv_shows_df)} items")
        
        # Load podcasts
        if os.path.exists(PODCASTS_PATH):
            podcasts_df = pd.read_csv(PODCASTS_PATH)
            podcasts_df['content_type'] = 'podcasts'
            content_dfs['podcasts'] = podcasts_df
            logger.info(f"Loaded podcasts: {len(podcasts_df)} items")
        
        # Load books
        if os.path.exists(BOOKS_PATH):
            books_df = pd.read_csv(BOOKS_PATH)
            books_df['content_type'] = 'books'
            content_dfs['books'] = books_df
            logger.info(f"Loaded books: {len(books_df)} items")
        
        # Load ratings
        if os.path.exists(MULTI_CONTENT_RATINGS_PATH):
            ratings_df = pd.read_csv(MULTI_CONTENT_RATINGS_PATH)
            logger.info(f"Loaded ratings: {len(ratings_df)} ratings")
        elif os.path.exists('rating.csv'):
            # Fallback to original ratings
            ratings_df = pd.read_csv('rating.csv')
            ratings_df['contentType'] = 'movies'  # Default to movies
            logger.info(f"Loaded original ratings: {len(ratings_df)} ratings")
        
        # Create TF-IDF matrices for each content type
        content_tfidf_matrices = {}
        for content_type, df in content_dfs.items():
            if 'combined_features' in df.columns:
                if tfidf_vectorizer is not None:
                    content_tfidf_matrices[content_type] = tfidf_vectorizer.transform(df['combined_features'])
                    logger.info(f"Created TF-IDF matrix for {content_type}: {content_tfidf_matrices[content_type].shape}")
        
        logger.info("Multi-content model artifacts loaded successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error loading multi-content artifacts: {e}")
        return False

# --- User Profile Generation for Multi-Content ---
def get_user_profile_vector_multi_content(user_id, content_type=None, min_rating_threshold=4.0):
    """Generate user profile vector for specific content type or all content"""
    if ratings_df is None or not content_dfs:
        logger.error("Error: Data not loaded for user profile generation.")
        return None
    
    # Filter ratings by content type if specified
    if content_type:
        user_ratings = ratings_df[
            (ratings_df['userId'] == user_id) &
            (ratings_df['contentType'] == content_type) &
            (ratings_df['rating'] >= min_rating_threshold)
        ]
    else:
        user_ratings = ratings_df[
            (ratings_df['userId'] == user_id) &
            (ratings_df['rating'] >= min_rating_threshold)
        ]
    
    if user_ratings.empty:
        logger.info(f"User {user_id} has no {content_type or 'any'} content rated {min_rating_threshold} or higher.")
        return None
    
    # Get content data for the rated items
    rated_content = []
    for _, rating in user_ratings.iterrows():
        content_id = rating['contentId']
        content_type_rated = rating['contentType']
        
        if content_type_rated in content_dfs:
            content_data = content_dfs[content_type_rated][content_dfs[content_type_rated]['id'] == content_id]
            if not content_data.empty:
                rated_content.append({
                    'content_type': content_type_rated,
                    'content_data': content_data.iloc[0],
                    'rating': rating['rating']
                })
    
    if not rated_content:
        logger.warning(f"No content data found for highly-rated items of user {user_id}.")
        return None
    
    # Create weighted average of content vectors
    all_vectors = []
    weights = []
    
    for item in rated_content:
        content_type = item['content_type']
        if content_type in content_tfidf_matrices:
            content_idx = content_dfs[content_type][content_dfs[content_type]['id'] == item['content_data']['id']].index[0]
            vector = content_tfidf_matrices[content_type][content_idx]
            all_vectors.append(vector)
            weights.append(item['rating'])
    
    if not all_vectors:
        return None
    
    # Calculate weighted average
    weights = np.array(weights)
    weights = weights / weights.sum()
    
    weighted_vectors = [vec * weight for vec, weight in zip(all_vectors, weights)]
    user_profile_vector = sum(weighted_vectors)
    
    return user_profile_vector

# --- Enhanced Recommendation Generation ---
def get_recommendations_multi_content(user_id, content_type=None, num_recommendations=5):
    """Get recommendations from multi-content system"""
    user_profile_vector = get_user_profile_vector_multi_content(user_id, content_type)
    
    if user_profile_vector is None:
        logger.info(f"No specific profile for user {user_id}, returning random content.")
        # Return random content from specified type or all types
        if content_type and content_type in content_dfs:
            random_sample = content_dfs[content_type].sample(n=min(num_recommendations, len(content_dfs[content_type])))
        else:
            # Combine all content types
            all_content = pd.concat(content_dfs.values(), ignore_index=True)
            random_sample = all_content.sample(n=min(num_recommendations, len(all_content)))
        
        recommendations = []
        for _, item in random_sample.iterrows():
            recommendations.append({
                'id': str(item['id']),
                'title': item['title'],
                'content_type': item['content_type'],
                'genre': item.get('genres', '').replace('|', ', '),
                'description': item.get('description', ''),
                'similarity_score': 0.0
            })
        return recommendations
    
    # Get recommendations using similarity
    recommendations = []
    user_rated_content = set()
    
    # Get user's rated content IDs
    user_ratings = ratings_df[ratings_df['userId'] == user_id]
    for _, rating in user_ratings.iterrows():
        user_rated_content.add((rating['contentType'], rating['contentId']))
    
    # Calculate similarities for each content type
    for content_type, df in content_dfs.items():
        if content_type in content_tfidf_matrices:
            # Convert user profile to numpy array
            user_profile_np = user_profile_vector.toarray() if hasattr(user_profile_vector, 'toarray') else np.asarray(user_profile_vector)
            
            # Calculate similarities
            similarities = cosine_similarity(user_profile_np, content_tfidf_matrices[content_type]).flatten()
            
            # Get top similar items
            sorted_indices = similarities.argsort()[::-1]
            
            for idx in sorted_indices:
                content_id = df.iloc[idx]['id']
                
                # Skip if user already rated this content
                if (content_type, content_id) in user_rated_content:
                    continue
                
                item = df.iloc[idx]
                recommendations.append({
                    'id': str(item['id']),
                    'title': item['title'],
                    'content_type': item['content_type'],
                    'genre': item.get('genres', '').replace('|', ', '),
                    'description': item.get('description', ''),
                    'similarity_score': float(similarities[idx])
                })
                
                if len(recommendations) >= num_recommendations:
                    break
            
            if len(recommendations) >= num_recommendations:
                break
    
    # Sort by similarity score and return top recommendations
    recommendations.sort(key=lambda x: x['similarity_score'], reverse=True)
    return recommendations[:num_recommendations]

# --- User Statistics with Multi-Content Breakdown ---
def get_user_stats_multi_content(user_id):
    """Get comprehensive user statistics with content type breakdown"""
    if ratings_df is None:
        return None
    
    user_ratings = ratings_df[ratings_df['userId'] == user_id]
    if user_ratings.empty:
        return {
            'total_ratings': 0,
            'average_rating': 0,
            'high_ratings': 0,
            'favorite_genres': [],
            'content_type_breakdown': {content_type: 0 for content_type in CONTENT_TYPES.keys()}
        }
    
    total_ratings = len(user_ratings)
    average_rating = user_ratings['rating'].mean()
    high_ratings = len(user_ratings[user_ratings['rating'] >= 4.0])
    
    # Content type breakdown
    content_breakdown = user_ratings['contentType'].value_counts().to_dict()
    
    # Get favorite genres from highly-rated content
    highly_rated = user_ratings[user_ratings['rating'] >= 4.0]
    all_genres = []
    
    for _, rating in highly_rated.iterrows():
        content_id = rating['contentId']
        content_type = rating['contentType']
        
        if content_type in content_dfs:
            content_data = content_dfs[content_type][content_dfs[content_type]['id'] == content_id]
            if not content_data.empty:
                genres = content_data.iloc[0].get('genres', '')
                if genres:
                    all_genres.extend(genres.split('|'))
    
    favorite_genres = pd.Series(all_genres).value_counts().head(5).index.tolist()
    
    return {
        'total_ratings': int(total_ratings),
        'average_rating': float(average_rating),
        'high_ratings': int(high_ratings),
        'favorite_genres': favorite_genres,
        'content_type_breakdown': content_breakdown
    }

# --- Flask API Endpoints ---

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "model_loaded": tfidf_vectorizer is not None and bool(content_dfs),
        "supported_content_types": list(CONTENT_TYPES.keys()),
        "loaded_content_types": list(content_dfs.keys()),
        "total_content_items": sum(len(df) for df in content_dfs.values())
    })

@app.route('/recommend', methods=['POST'])
def recommend():
    """Multi-content recommendation endpoint"""
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user_id = data.get('userId')
        content_type = data.get('contentType', None)
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

        if not load_multi_content_artifacts():
            return jsonify({"error": "Model not loaded. Server might be initializing."}), 500

        logger.info(f"Generating multi-content recommendations for user {user_id}, content type: {content_type}")
        recommendations = get_recommendations_multi_content(user_id, content_type, num_recommendations)
        
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
    """Get user statistics with multi-content breakdown"""
    try:
        if not load_multi_content_artifacts():
            return jsonify({"error": "Model not loaded"}), 500
        
        stats = get_user_stats_multi_content(user_id)
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
        "loaded_content_types": list(content_dfs.keys()),
        "description": "Supported content types for recommendations"
    })

@app.route('/content/search', methods=['GET'])
def search_content():
    """Search content across all types"""
    try:
        query = request.args.get('q', '').lower()
        content_type = request.args.get('type', None)
        limit = int(request.args.get('limit', 10))
        
        if not query:
            return jsonify({"error": "Query parameter 'q' is required"}), 400
        
        if not load_multi_content_artifacts():
            return jsonify({"error": "Model not loaded"}), 500
        
        results = []
        
        # Search in all content types
        for content_type_name, df in content_dfs.items():
            if content_type and content_type_name != content_type:
                continue
            
            matching_content = df[df['title'].str.lower().str.contains(query, na=False)]
            
            for _, item in matching_content.head(limit).iterrows():
                results.append({
                    'id': str(item['id']),
                    'title': item['title'],
                    'content_type': item['content_type'],
                    'genre': item.get('genres', '').replace('|', ', '),
                    'description': item.get('description', '')
                })
        
        return jsonify({
            "query": query,
            "content_type_filter": content_type,
            "results": results[:limit],
            "count": len(results)
        })
    
    except Exception as e:
        logger.error(f"Error in search_content endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/content/popular', methods=['GET'])
def get_popular_content():
    """Get popular content with type filtering"""
    try:
        content_type = request.args.get('type', None)
        limit = int(request.args.get('limit', 10))
        
        if not load_multi_content_artifacts():
            return jsonify({"error": "Model not loaded"}), 500
        
        # Calculate popularity for each content type
        results = []
        
        for content_type_name in content_dfs.keys():
            if content_type and content_type_name != content_type:
                continue
            
            # Get ratings for this content type
            type_ratings = ratings_df[ratings_df['contentType'] == content_type_name]
            
            if not type_ratings.empty:
                # Calculate average rating and count
                content_stats = type_ratings.groupby('contentId').agg({
                    'rating': ['mean', 'count']
                }).reset_index()
                content_stats.columns = ['contentId', 'avg_rating', 'rating_count']
                
                # Filter by minimum ratings and sort
                popular_content = content_stats[content_stats['rating_count'] >= 5].sort_values('avg_rating', ascending=False)
                
                # Get content details
                for _, stats_row in popular_content.head(limit).iterrows():
                    content_id = stats_row['contentId']
                    content_data = content_dfs[content_type_name][content_dfs[content_type_name]['id'] == content_id]
                    
                    if not content_data.empty:
                        content_row = content_data.iloc[0]
                        results.append({
                            'id': str(content_row['id']),
                            'title': content_row['title'],
                            'content_type': content_row['content_type'],
                            'genre': content_row.get('genres', '').replace('|', ', '),
                            'avg_rating': float(stats_row['avg_rating']),
                            'rating_count': int(stats_row['rating_count'])
                        })
        
        return jsonify({
            "content_type_filter": content_type,
            "popular_content": results[:limit],
            "count": len(results)
        })
    
    except Exception as e:
        logger.error(f"Error in get_popular_content endpoint: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

# --- Server Initialization ---
if __name__ == '__main__':
    logger.info("Loading multi-content model components...")
    if load_multi_content_artifacts():
        logger.info("Multi-content model components loaded successfully. Starting Flask app...")
        app.run(debug=True, port=5000, host='0.0.0.0')
    else:
        logger.error("Failed to load multi-content model components. Flask app will not start.") 