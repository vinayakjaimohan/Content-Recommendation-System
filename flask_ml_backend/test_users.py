#!/usr/bin/env python3
"""
User Testing Script for Movie Recommendation API
Tests different users and compares their recommendations
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_user(user_id):
    """Test a specific user"""
    print(f"\n{'='*60}")
    print(f"TESTING USER {user_id}")
    print(f"{'='*60}")
    
    # Get user stats
    try:
        response = requests.get(f"{BASE_URL}/user/{user_id}/stats")
        if response.status_code == 200:
            stats = response.json()
            user_stats = stats['stats']
            print(f"📊 USER STATISTICS:")
            print(f"   Total Ratings: {user_stats['total_ratings']}")
            print(f"   Average Rating: {user_stats['average_rating']:.2f}")
            print(f"   High Ratings (≥4.0): {user_stats['high_ratings']}")
            print(f"   Favorite Genres: {', '.join(user_stats['favorite_genres'])}")
        else:
            print(f"❌ Failed to get user stats: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting user stats: {e}")
        return False
    
    # Get recommendations
    try:
        response = requests.post(f"{BASE_URL}/recommend", 
                               json={"userId": user_id, "numRecommendations": 5})
        if response.status_code == 200:
            data = response.json()
            print(f"\n🎬 RECOMMENDATIONS:")
            print(f"   Found {len(data['recommendations'])} recommendations")
            
            for i, rec in enumerate(data['recommendations'], 1):
                similarity = rec.get('similarity_score', 0)
                print(f"   {i}. {rec['title']}")
                print(f"      Genre: {rec['genre']}")
                print(f"      Similarity: {similarity:.3f}")
        else:
            print(f"❌ Failed to get recommendations: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting recommendations: {e}")
        return False
    
    return True

def compare_users(user_ids):
    """Compare multiple users"""
    print(f"\n{'='*80}")
    print(f"COMPARING {len(user_ids)} USERS")
    print(f"{'='*80}")
    
    results = {}
    
    for user_id in user_ids:
        try:
            # Get user stats
            stats_response = requests.get(f"{BASE_URL}/user/{user_id}/stats")
            if stats_response.status_code == 200:
                stats = stats_response.json()['stats']
                
                # Get recommendations
                rec_response = requests.post(f"{BASE_URL}/recommend", 
                                          json={"userId": user_id, "numRecommendations": 3})
                if rec_response.status_code == 200:
                    recommendations = rec_response.json()['recommendations']
                    
                    results[user_id] = {
                        'total_ratings': stats['total_ratings'],
                        'avg_rating': stats['average_rating'],
                        'high_ratings': stats['high_ratings'],
                        'favorite_genres': stats['favorite_genres'],
                        'recommendations': [rec['title'] for rec in recommendations]
                    }
        except Exception as e:
            print(f"❌ Error testing user {user_id}: {e}")
    
    # Display comparison
    print(f"\n{'User ID':<8} {'Ratings':<8} {'Avg':<6} {'High':<6} {'Top Genres':<30} {'Sample Recommendations'}")
    print("-" * 100)
    
    for user_id, data in results.items():
        genres_str = ', '.join(data['favorite_genres'][:3])
        recs_str = ', '.join(data['recommendations'][:2])
        print(f"{user_id:<8} {data['total_ratings']:<8} {data['avg_rating']:<6.2f} {data['high_ratings']:<6} {genres_str:<30} {recs_str}")

def find_active_users(limit=10):
    """Find users with the most ratings"""
    print(f"\n{'='*60}")
    print(f"FINDING MOST ACTIVE USERS")
    print(f"{'='*60}")
    
    active_users = []
    
    # Test a range of user IDs
    for user_id in range(1, 51):  # Test first 50 users
        try:
            response = requests.get(f"{BASE_URL}/user/{user_id}/stats")
            if response.status_code == 200:
                stats = response.json()['stats']
                if stats['total_ratings'] > 0:
                    active_users.append({
                        'user_id': user_id,
                        'total_ratings': stats['total_ratings'],
                        'avg_rating': stats['average_rating'],
                        'high_ratings': stats['high_ratings']
                    })
        except:
            continue
    
    # Sort by total ratings
    active_users.sort(key=lambda x: x['total_ratings'], reverse=True)
    
    print(f"{'User ID':<8} {'Total Ratings':<15} {'Avg Rating':<12} {'High Ratings':<12}")
    print("-" * 50)
    
    for user in active_users[:limit]:
        print(f"{user['user_id']:<8} {user['total_ratings']:<15} {user['avg_rating']:<12.2f} {user['high_ratings']:<12}")
    
    return [user['user_id'] for user in active_users[:limit]]

def main():
    print("🎬 MOVIE RECOMMENDATION API - USER TESTING")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test individual users
    test_users = [1, 2, 10, 100]
    
    for user_id in test_users:
        test_user(user_id)
    
    # Find and compare active users
    active_users = find_active_users(5)
    
    if active_users:
        print(f"\nComparing top {len(active_users)} active users...")
        compare_users(active_users)
    
    print(f"\n{'='*60}")
    print("USER TESTING COMPLETE!")
    print(f"{'='*60}")

if __name__ == "__main__":
    main() 