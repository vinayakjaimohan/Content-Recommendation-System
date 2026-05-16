#!/usr/bin/env python3
"""
Debug script to identify which test is failing
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    print("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_recommendations():
    print("\nTesting recommendations...")
    try:
        response = requests.post(f"{BASE_URL}/recommend", json={"userId": 1, "numRecommendations": 5})
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Recommendations: {len(data.get('recommendations', []))} items")
            return True
        else:
            print(f"❌ Recommendations failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Recommendations error: {e}")
        return False

def test_user_stats():
    print("\nTesting user stats...")
    try:
        response = requests.get(f"{BASE_URL}/user/1/stats")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ User stats: {data.get('stats', {}).get('total_ratings', 0)} ratings")
            return True
        else:
            print(f"❌ User stats failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ User stats error: {e}")
        return False

def test_movie_search():
    print("\nTesting movie search...")
    try:
        response = requests.get(f"{BASE_URL}/movies/search?q=batman&limit=3")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Movie search: {data.get('count', 0)} results")
            return True
        else:
            print(f"❌ Movie search failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Movie search error: {e}")
        return False

def test_popular_movies():
    print("\nTesting popular movies...")
    try:
        response = requests.get(f"{BASE_URL}/movies/popular?limit=3")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Popular movies: {data.get('count', 0)} movies")
            return True
        else:
            print(f"❌ Popular movies failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Popular movies error: {e}")
        return False

def main():
    print("=" * 50)
    print("DEBUGGING API TESTS")
    print("=" * 50)
    
    tests = [
        ("Health Check", test_health),
        ("Recommendations", test_recommendations),
        ("User Stats", test_user_stats),
        ("Movie Search", test_movie_search),
        ("Popular Movies", test_popular_movies)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success))
        except Exception as e:
            print(f"❌ {name} crashed: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{name}: {status}")
    
    failed_tests = [name for name, success in results if not success]
    if failed_tests:
        print(f"\nFailed tests: {', '.join(failed_tests)}")
    else:
        print("\nAll tests passed!")

if __name__ == "__main__":
    main() 