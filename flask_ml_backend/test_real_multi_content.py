#!/usr/bin/env python3
"""
Real Multi-Content Recommendation System Test Script
Tests the enhanced system with actual multi-content datasets
"""

import requests
import json
import pandas as pd
from datetime import datetime

BASE_URL = "http://localhost:5000"

def test_health_with_multi_content():
    """Test health endpoint with multi-content info"""
    print("Testing health endpoint with multi-content info...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed")
            print(f"   Model loaded: {data.get('model_loaded', False)}")
            print(f"   Supported content types: {data.get('supported_content_types', [])}")
            print(f"   Loaded content types: {data.get('loaded_content_types', [])}")
            print(f"   Total content items: {data.get('total_content_items', 0)}")
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
            print(f"   Supported types: {list(data['content_types'].keys())}")
            print(f"   Loaded types: {data.get('loaded_content_types', [])}")
            return True
        else:
            print(f"❌ Content types failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Content types error: {e}")
        return False

def test_multi_content_recommendations():
    """Test recommendations for all content types"""
    content_types = ['movies', 'tv_shows', 'podcasts', 'books']
    
    for content_type in content_types:
        print(f"\nTesting {content_type} recommendations...")
        try:
            response = requests.post(f"{BASE_URL}/recommend", 
                                   json={"userId": 1, "contentType": content_type, "numRecommendations": 3})
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {content_type.title()} recommendations generated:")
                print(f"   User ID: {data['user_id']}")
                print(f"   Content Type: {data['content_type']}")
                print(f"   Count: {data['count']}")
                
                for i, rec in enumerate(data['recommendations'], 1):
                    print(f"   {i}. {rec['title']} ({rec['content_type']}) - {rec.get('genre', 'N/A')}")
            else:
                print(f"❌ {content_type.title()} recommendations failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {content_type.title()} recommendations error: {e}")

def test_cross_content_recommendations():
    """Test recommendations without content type filter (cross-content)"""
    print("\nTesting cross-content recommendations...")
    try:
        response = requests.post(f"{BASE_URL}/recommend", 
                               json={"userId": 1, "numRecommendations": 5})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Cross-content recommendations generated:")
            print(f"   User ID: {data['user_id']}")
            print(f"   Count: {data['count']}")
            
            # Group by content type
            content_groups = {}
            for rec in data['recommendations']:
                content_type = rec['content_type']
                if content_type not in content_groups:
                    content_groups[content_type] = []
                content_groups[content_type].append(rec)
            
            for content_type, recs in content_groups.items():
                print(f"   {content_type.title()}: {len(recs)} items")
                for rec in recs:
                    print(f"     - {rec['title']}")
        else:
            print(f"❌ Cross-content recommendations failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Cross-content recommendations error: {e}")

def test_user_stats_multi_content():
    """Test user statistics with multi-content breakdown"""
    print("\nTesting user stats with multi-content breakdown...")
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

def test_multi_content_search():
    """Test search across all content types"""
    search_queries = [
        ("breaking", "TV shows"),
        ("serial", "Podcasts"),
        ("classic", "Books"),
        ("star", "Movies")
    ]
    
    for query, expected_type in search_queries:
        print(f"\nTesting search for '{query}' (expected: {expected_type})...")
        try:
            response = requests.get(f"{BASE_URL}/content/search?q={query}&limit=5")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Search successful:")
                print(f"   Query: {data['query']}")
                print(f"   Results: {data['count']}")
                
                # Show content type distribution
                content_types = {}
                for item in data['results']:
                    content_type = item['content_type']
                    content_types[content_type] = content_types.get(content_type, 0) + 1
                
                for content_type, count in content_types.items():
                    print(f"     {content_type}: {count} items")
            else:
                print(f"❌ Search failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Search error: {e}")

def test_content_type_filtered_search():
    """Test search with content type filtering"""
    content_types = ['movies', 'tv_shows', 'podcasts', 'books']
    
    for content_type in content_types:
        print(f"\nTesting {content_type} search...")
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

def test_popular_content_by_type():
    """Test popular content for each content type"""
    content_types = ['movies', 'tv_shows', 'podcasts', 'books']
    
    for content_type in content_types:
        print(f"\nTesting popular {content_type}...")
        try:
            response = requests.get(f"{BASE_URL}/content/popular?type={content_type}&limit=3")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Popular {content_type}:")
                print(f"   Results: {data['count']}")
                
                for i, item in enumerate(data['popular_content'], 1):
                    print(f"     {i}. {item['title']} - Rating: {item['avg_rating']:.2f}")
            else:
                print(f"❌ Popular {content_type} failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Popular {content_type} error: {e}")

def test_error_handling():
    """Test error handling for invalid requests"""
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
    
    # Test missing user ID
    try:
        response = requests.post(f"{BASE_URL}/recommend", 
                               json={"contentType": "movies"})
        if response.status_code == 400:
            print("✅ Missing user ID handled correctly")
        else:
            print(f"❌ Expected 400 for missing user ID, got {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing missing user ID: {e}")

def test_data_quality():
    """Test data quality and consistency"""
    print("\nTesting data quality...")
    
    # Test that recommendations have proper structure
    try:
        response = requests.post(f"{BASE_URL}/recommend", 
                               json={"userId": 1, "contentType": "movies", "numRecommendations": 1})
        if response.status_code == 200:
            data = response.json()
            if data['recommendations']:
                rec = data['recommendations'][0]
                required_fields = ['id', 'title', 'content_type', 'genre', 'description', 'similarity_score']
                missing_fields = [field for field in required_fields if field not in rec]
                
                if not missing_fields:
                    print("✅ Recommendation structure is correct")
                else:
                    print(f"❌ Missing fields in recommendation: {missing_fields}")
            else:
                print("⚠️  No recommendations returned")
        else:
            print(f"❌ Failed to get recommendations: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing data quality: {e}")

def main():
    """Run all multi-content tests"""
    print("=" * 80)
    print("REAL MULTI-CONTENT RECOMMENDATION SYSTEM TESTING")
    print("=" * 80)
    print(f"Testing API at: {BASE_URL}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    tests = [
        ("Health Check", test_health_with_multi_content),
        ("Content Types", test_content_types_endpoint),
        ("Multi-Content Recommendations", test_multi_content_recommendations),
        ("Cross-Content Recommendations", test_cross_content_recommendations),
        ("User Stats Multi-Content", test_user_stats_multi_content),
        ("Multi-Content Search", test_multi_content_search),
        ("Content Type Filtered Search", test_content_type_filtered_search),
        ("Popular Content by Type", test_popular_content_by_type),
        ("Error Handling", test_error_handling),
        ("Data Quality", test_data_quality)
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
        print("🎉 All real multi-content tests passed! The system is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the server logs for details.")
    
    print("\n" + "=" * 80)
    print("REAL MULTI-CONTENT TESTING COMPLETE!")
    print("=" * 80)
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 