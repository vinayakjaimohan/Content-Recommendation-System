#!/usr/bin/env python3
"""
Test script for the Flask ML Backend API
"""

import requests
import json
import time
from datetime import datetime

# API base URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API. Make sure the server is running.")
        return False

def test_recommendations():
    """Test the recommendations endpoint"""
    print("\nTesting recommendations endpoint...")
    
    # Test with a valid user ID
    test_data = {
        "userId": 1,
        "numRecommendations": 5
    }
    
    try:
        response = requests.post(f"{BASE_URL}/recommend", json=test_data)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recommendations generated successfully:")
            print(f"   User ID: {data['user_id']}")
            print(f"   Count: {data['count']}")
            print(f"   Recommendations: {len(data['recommendations'])} items")
            
            # Print first recommendation as example
            if data['recommendations']:
                first_rec = data['recommendations'][0]
                print(f"   Example: {first_rec['title']} ({first_rec['genre']})")
            return True
        else:
            print(f"❌ Recommendations failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error testing recommendations: {e}")
        return False

def test_user_stats():
    """Test the user stats endpoint"""
    print("\nTesting user stats endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/user/1/stats")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ User stats retrieved successfully:")
            print(f"   User ID: {data['user_id']}")
            stats = data['stats']
            print(f"   Total ratings: {stats['total_ratings']}")
            print(f"   Average rating: {stats['average_rating']:.2f}")
            print(f"   High ratings: {stats['high_ratings']}")
            print(f"   Favorite genres: {stats['favorite_genres']}")
            return True
        else:
            print(f"❌ User stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing user stats: {e}")
        return False

def test_movie_search():
    """Test the movie search endpoint"""
    print("\nTesting movie search endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/movies/search?q=batman&limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Movie search successful:")
            print(f"   Query: {data['query']}")
            print(f"   Results: {data['count']}")
            
            if data['results']:
                print("   Sample results:")
                for i, movie in enumerate(data['results'][:2], 1):
                    print(f"     {i}. {movie['title']} ({movie['genre']})")
            return True
        else:
            print(f"❌ Movie search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing movie search: {e}")
        return False

def test_popular_movies():
    """Test the popular movies endpoint"""
    print("\nTesting popular movies endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/movies/popular?limit=3")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Popular movies retrieved successfully:")
            print(f"   Count: {data['count']}")
            
            if data['popular_movies']:
                print("   Sample popular movies:")
                for i, movie in enumerate(data['popular_movies'][:2], 1):
                    print(f"     {i}. {movie['title']} (Rating: {movie['avg_rating']:.2f}, Votes: {movie['rating_count']})")
            return True
        else:
            print(f"❌ Popular movies failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error testing popular movies: {e}")
        return False

def test_error_handling():
    """Test error handling"""
    print("\nTesting error handling...")
    
    # Test invalid user ID
    try:
        response = requests.post(f"{BASE_URL}/recommend", json={"userId": "invalid"})
        if response.status_code == 400:
            print("✅ Invalid user ID handled correctly")
        else:
            print(f"❌ Expected 400 for invalid user ID, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing invalid user ID: {e}")
    
    # Test missing user ID
    try:
        response = requests.post(f"{BASE_URL}/recommend", json={})
        if response.status_code == 400:
            print("✅ Missing user ID handled correctly")
        else:
            print(f"❌ Expected 400 for missing user ID, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing missing user ID: {e}")
    
    # Test movie not found
    try:
        response = requests.get(f"{BASE_URL}/movies/999999")
        if response.status_code == 404:
            print("✅ Movie not found handled correctly")
        else:
            print(f"❌ Expected 404 for non-existent movie, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing non-existent movie: {e}")

def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("FLASK ML BACKEND API TESTING")
    print("=" * 50)
    print(f"Testing API at: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health_check),
        ("Recommendations", test_recommendations),
        ("User Stats", test_user_stats),
        ("Movie Search", test_movie_search),
        ("Popular Movies", test_popular_movies),
        ("Error Handling", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
    
    print("\n" + "=" * 50)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! The API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
    
    return passed == total

if __name__ == "__main__":
    # Wait a moment for the server to start if needed
    print("Waiting for server to be ready...")
    time.sleep(2)
    
    success = run_all_tests()
    exit(0 if success else 1) 