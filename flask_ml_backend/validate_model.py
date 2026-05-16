import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os

# --- Paths to your dataset files ---
TFIDF_VECTORIZER_PATH = 'tfidf_vectorizer.pkl'
PROCESSED_MOVIES_PATH = 'processed_movies.csv'
RATINGS_DATA_PATH = 'rating.csv'

# --- Global variables for loaded data and model components ---
tfidf_vectorizer = None
movies_df = None
ratings_df = None
content_tfidf_matrix = None

# --- Model Loading Function (to be called once at startup) ---
def load_model_artifacts():
    global tfidf_vectorizer, movies_df, ratings_df, content_tfidf_matrix
    # Check if already loaded (for multiple calls in same session)
    if tfidf_vectorizer is not None and movies_df is not None and ratings_df is not None:
        return True
    try:
        tfidf_vectorizer = joblib.load(TFIDF_VECTORIZER_PATH)
        movies_df = pd.read_csv(PROCESSED_MOVIES_PATH)
        ratings_df = pd.read_csv(RATINGS_DATA_PATH)

        # Ensure movieId in ratings_df is int for merging
        ratings_df['movieId'] = ratings_df['movieId'].astype(int)
        movies_df['movieId'] = movies_df['movieId'].astype(int)

        # Re-generate the content TF-IDF matrix from the loaded movies_df
        content_tfidf_matrix = tfidf_vectorizer.transform(movies_df['combined_features'])

        print("Model artifacts and data loaded successfully.")
        print(f"Loaded movies_df shape: {movies_df.shape}")
        print(f"Loaded ratings_df shape: {ratings_df.shape}")
        print(f"Re-generated content_tfidf_matrix shape: {content_tfidf_matrix.shape}")
        return True
    except FileNotFoundError as e:
        print(f"Error loading model artifacts: {e.filename}. Make sure they are in the correct directory.")
        print("Please ensure 'tfidf_vectorizer.pkl', 'processed_movies.csv', and 'ratings.csv' are present.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred during model loading: {e}")
        return False

# --- User Profile Representation Function ---
def get_user_profile_vector(user_id, min_rating_threshold=4.0):
    if ratings_df is None or movies_df is None or tfidf_vectorizer is None:
        print("Error: Data or vectorizer not loaded for user profile generation.")
        return None

    user_highly_rated_movies = ratings_df[
        (ratings_df['userId'] == user_id) &
        (ratings_df['rating'] >= min_rating_threshold)
    ]

    if user_highly_rated_movies.empty:
        # print(f"User {user_id} has no movies rated {min_rating_threshold} or higher.")
        return None

    highly_rated_movie_ids = user_highly_rated_movies['movieId'].tolist()
    liked_movies_data = movies_df[movies_df['movieId'].isin(highly_rated_movie_ids)]

    if liked_movies_data.empty:
        print(f"No content data found for highly-rated movies of user {user_id}.")
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

# --- Recommendation Generation Function ---
# ... (previous code) ...

# --- Recommendation Generation Function ---
def get_recommendations_ml(user_id, category_filter=None, num_recommendations=5):
    user_profile_vector = get_user_profile_vector(user_id)

    if user_profile_vector is None:
        print(f"No specific profile for user {user_id} (no high ratings), returning a random sample of movies.")
        random_sample_df = movies_df.sample(n=num_recommendations)
        formatted_sample = []
        for idx, item in random_sample_df.iterrows():
            formatted_sample.append({
                'id': str(item['movieId']),
                'title': item['title'],
                'category': 'Movies',
                'genre': item['genres'].replace('|', ', '),
                'description': f"Genres: {item['genres'].replace('|', ', ')}"
            })
        return formatted_sample

    # --- CRITICAL FIX: Convert user_profile_vector to numpy array ---
    # The user_profile_vector might be a sparse matrix or a numpy.matrix
    # cosine_similarity expects a numpy.ndarray
    user_profile_vector_np = user_profile_vector.toarray() if hasattr(user_profile_vector, 'toarray') else np.asarray(user_profile_vector)


    similarity_scores = cosine_similarity(user_profile_vector_np, content_tfidf_matrix).flatten() # Use the converted vector
    sorted_indices = similarity_scores.argsort()[::-1]

    recommended_items = []
    seen_movie_ids = set()
    user_rated_movie_ids = set(ratings_df[ratings_df['userId'] == user_id]['movieId'].tolist())

    for idx in sorted_indices:
        movie_id = movies_df.iloc[idx]['movieId']

        if movie_id in seen_movie_ids or movie_id in user_rated_movie_ids:
            continue

        item = movies_df.iloc[idx].to_dict()

        item_category = 'Movies'
        if category_filter and item_category != category_filter:
            continue

        recommended_items.append({
            'id': str(item['movieId']),
            'title': item['title'],
            'category': item_category,
            'genre': item['genres'].replace('|', ', '),
            'description': f"Genres: {item['genres'].replace('|', ', ')}"
        })
        seen_movie_ids.add(movie_id)

        if len(recommended_items) >= num_recommendations:
            break

    return recommended_items

# ... (rest of the code) ...

# --- Main execution block for validation ---
if __name__ == '__main__':
    print("--- Starting Model Validation ---")
    if not load_model_artifacts(): # Call the setup function
        print("Cannot proceed with validation as model artifacts failed to load.")
        exit()

    # --- Scenario 1: Recommendations for User ID 1 (based on their high ratings) ---
    test_user_id_1 = 1
    print(f"\n--- Scenario 1: Recommendations for User ID {test_user_id_1} (based on their high ratings) ---")
    recommendations_1 = get_recommendations_ml(test_user_id_1, category_filter="Movies", num_recommendations=5)
    if recommendations_1:
        for i, rec in enumerate(recommendations_1):
            print(f"{i+1}. Title: {rec['title']}, Genres: {rec['genre']}")
    else:
        print(f"No recommendations found for User ID {test_user_id_1}. Check if they have high ratings.")
        user_ratings_sample = ratings_df[ratings_df['userId'] == test_user_id_1].head(10)
        if not user_ratings_sample.empty:
            print(f"Sample ratings for User {test_user_id_1}:\n{user_ratings_sample}")
        else:
            print(f"User {test_user_id_1} has no ratings in the dataset.")


    # --- Scenario 2: Recommendations for a hypothetical new user (or user with no high ratings) ---
    test_user_id_2 = 9999999 # A user ID that likely doesn't exist in ratings.csv
    print(f"\n--- Scenario 2: Recommendations for User ID {test_user_id_2} (new user/no high ratings) ---")
    recommendations_2 = get_recommendations_ml(test_user_id_2, category_filter="Movies", num_recommendations=5)
    if recommendations_2:
        for i, rec in enumerate(recommendations_2):
            print(f"{i+1}. Title: {rec['title']}, Genres: {rec['genre']}")
    else:
        print("No recommendations found for this user.")

    print("\n--- Model Validation Complete ---")