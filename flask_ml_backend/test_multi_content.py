#!/usr/bin/env python3
"""
Multi-Content Recommendation System Test Script
Tests recommendations for movies, TV shows, podcasts, and books
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_health_with_content_types():
    """Test health endpoint with content types"""
    print("Testing health endpoint with content types...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Supported content types: {data.get('supported_content_types', [])}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_content_types_endpoint():
    """Test content types endpoint"""
    print("\nTesting content types endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/content/types")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Content types retrieved:")
            for content_type, display_name in data['content_types'].items():
                print(f"   - {content_type}: {display_name}")
            return True
        else:
            print(f"❌ Content types failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Content types error: {e}")
        return False

def test_movie_recommendations():
    """Test movie recommendations"""
    print("\nTesting movie recommendations...")
    try:
        response = requests.post(f"{BASE_URL}/recommend", 
                               json={"userId": 1, "contentType": "movies", "numRecommendations": 3})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Movie recommendations generated:")
            print(f"   User ID: {data['user_id']}")
            print(f"   Content Type: {data['content_type']}")
            print(f"   Count: {data['count']}")
            
            for i, rec in enumerate(data['recommendations'], 1):
                print(f"   {i}. {rec['title']} ({rec['content_type']}) - {rec['genre']}")
            return True
        else:
            print(f"❌ Movie recommendations failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Movie recommendations error: {e}")
        return False

def test_tv_show_recommendations():
    """Test TV show recommendations"""
    print("\nTesting TV show recommendations...")
    try:
        response = requests.post(f"{BASE_URL}/recommend", 
                               json={"userId": 1, "contentType": "tv_shows", "numRecommendations": 3})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ TV show recommendations generated:")
            print(f"   User ID: {data['user_id']}")
            print(f"   Content Type: {data['content_type']}")
            print(f"   Count: {data['count']}")
            
            for i, rec in enumerate(data['recommendations'], 1):
                print(f"   {i}. {rec['title']} ({rec['content_type']}) - {rec['genre']}")
            return True
        else:
            print(f"❌ TV show recommendations failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ TV show recommendations error: {e}")
        return False

def test_podcast_recommendations():
    """Test podcast recommendations"""
    print("\nTesting podcast recommendations...")
    try:
        response = requests.post(f"{BASE_URL}/recommend", 
                               json={"userId": 1, "contentType": "podcasts", "numRecommendations": 3})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Podcast recommendations generated:")
            print(f"   User ID: {data['user_id']}")
            print(f"   Content Type: {data['content_type']}")
            print(f"   Count: {data['count']}")
            
            for i, rec in enumerate(data['recommendations'], 1):
                print(f"   {i}. {rec['title']} ({rec['content_type']}) - {rec['genre']}")
            return True
        else:
            print(f"❌ Podcast recommendations failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Podcast recommendations error: {e}")
        return False

def test_book_recommendations():
    """Test book recommendations"""
    print("\nTesting book recommendations...")
    try:
        response = requests.post(f"{BASE_URL}/recommend", 
                               json={"userId": 1, "contentType": "books", "numRecommendations": 3})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Book recommendations generated:")
            print(f"   User ID: {data['user_id']}")
            print(f"   Content Type: {data['content_type']}")
            print(f"   Count: {data['count']}")
            
            for i, rec in enumerate(data['recommendations'], 1):
                print(f"   {i}. {rec['title']} ({rec['content_type']}) - {rec['genre']}")
            return True
        else:
            print(f"❌ Book recommendations failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Book recommendations error: {e}")
        return False

def test_user_stats_with_content_breakdown():
    """Test user stats with content type breakdown"""
    print("\nTesting user stats with content breakdown...")
    try:
        response = requests.get(f"{BASE_URL}/user/1/stats")
        if response.status_code == 200:
            data = response.json()
            stats = data['stats']
            print(f"✅ User stats retrieved:")
            print(f"   Total Ratings: {stats['total_ratings']}")
            print(f"   Average Rating: {stats['average_rating']:.2f}")
            print(f"   High Ratings: {stats['high_ratings']}")
            print(f"   Favorite Genres: {', '.join(stats['favorite_genres'])}")
            
            content_breakdown = stats.get('content_type_breakdown', {})
            print(f"   Content Type Breakdown:")
            for content_type, count in content_breakdown.items():
                print(f"     - {content_type}: {count}")
            return True
        else:
            print(f"❌ User stats failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ User stats error: {e}")
        return False

def test_content_search():
    """Test content search across all types"""
    print("\nTesting content search...")
    try:
        response = requests.get(f"{BASE_URL}/content/search?q=star&limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Content search successful:")
            print(f"   Query: {data['query']}")
            print(f"   Results: {data['count']}")
            
            for i, item in enumerate(data['results'], 1):
                print(f"   {i}. {item['title']} ({item['content_type']}) - {item['genre']}")
            return True
        else:
            print(f"❌ Content search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Content search error: {e}")
        return False

def test_popular_content():
    """Test popular content endpoint"""
    print("\nTesting popular content...")
    try:
        response = requests.get(f"{BASE_URL}/content/popular?limit=5")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Popular content retrieved:")
            print(f"   Count: {data['count']}")
            
            for i, item in enumerate(data['popular_content'], 1):
                print(f"   {i}. {item['title']} ({item['content_type']}) - Rating: {item['avg_rating']:.2f}")
            return True
        else:
            print(f"❌ Popular content failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Popular content error: {e}")
        return False

def test_content_type_filtered_search():
    """Test content search with type filtering"""
    print("\nTesting content search with type filtering...")
    
    content_types = ['movies', 'tv_shows', 'podcasts', 'books']
    
    for content_type in content_types:
        try:
            response = requests.get(f"{BASE_URL}/content/search?q=the&type={content_type}&limit=3")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {content_type.title()} search:")
                print(f"   Results: {data['count']}")
                
                for i, item in enumerate(data['results'], 1):
                    print(f"     {i}. {item['title']} ({item['content_type']})")
            else:
                print(f"❌ {content_type.title()} search failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {content_type.title()} search error: {e}")

def test_error_handling():
    """Test error handling for invalid content types"""
    print("\nTesting error handling...")
    
    # Test invalid content type
    try:
        response = requests.post(f"{BASE_URL}/recommend", 
                               json={"userId": 1, "contentType": "invalid_type"})
        if response.status_code == 400:
            print("✅ Invalid content type handled correctly")
        else:
            print(f"❌ Expected 400 for invalid content type, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing invalid content type: {e}")

def main():
    """Run all multi-content tests"""
    print("=" * 80)
    print("MULTI-CONTENT RECOMMENDATION SYSTEM TESTING")
    print("=" * 80)
    print(f"Testing API at: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    tests = [
        ("Health Check", test_health_with_content_types),
        ("Content Types", test_content_types_endpoint),
        ("Movie Recommendations", test_movie_recommendations),
        ("TV Show Recommendations", test_tv_show_recommendations),
        ("Podcast Recommendations", test_podcast_recommendations),
        ("Book Recommendations", test_book_recommendations),
        ("User Stats with Content Breakdown", test_user_stats_with_content_breakdown),
        ("Content Search", test_content_search),
        ("Popular Content", test_popular_content),
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
    
    print("\n" + "=" * 80)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print("=" * 80)
    
    if passed == total:
        print("🎉 All multi-content tests passed! The system is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
    
    # Test content type filtered search
    print("\n" + "=" * 80)
    print("CONTENT TYPE FILTERED SEARCH TESTING")
    print("=" * 80)
    test_content_type_filtered_search()
    
    print("\n" + "=" * 80)
    print("MULTI-CONTENT TESTING COMPLETE!")
    print("=" * 80)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 