#!/usr/bin/env python3
"""
Enhanced Example Client for Multi-Content Recommendation API
Supports movies, TV shows, podcasts, and books
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

class RecommendationClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    def health_check(self):
        """Check API health and supported content types"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'healthy',
                    'model_loaded': data.get('model_loaded', False),
                    'supported_content_types': data.get('supported_content_types', [])
                }
            else:
                return {'status': 'unhealthy', 'error': f"HTTP {response.status_code}"}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}
    
    def get_content_types(self):
        """Get supported content types"""
        try:
            response = self.session.get(f"{self.base_url}/content/types")
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f"HTTP {response.status_code}"}
        except Exception as e:
            return {'error': str(e)}
    
    def get_recommendations(self, user_id, content_type=None, num_recommendations=5):
        """Get recommendations for a user with optional content type filtering"""
        payload = {
            'userId': user_id,
            'numRecommendations': num_recommendations
        }
        
        if content_type:
            payload['contentType'] = content_type
        
        try:
            response = self.session.post(f"{self.base_url}/recommend", json=payload)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f"HTTP {response.status_code}", 'details': response.text}
        except Exception as e:
            return {'error': str(e)}
    
    def get_user_stats(self, user_id):
        """Get user statistics with content type breakdown"""
        try:
            response = self.session.get(f"{self.base_url}/user/{user_id}/stats")
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f"HTTP {response.status_code}"}
        except Exception as e:
            return {'error': str(e)}
    
    def search_content(self, query, content_type=None, limit=10):
        """Search content across all types with optional filtering"""
        params = {'q': query, 'limit': limit}
        if content_type:
            params['type'] = content_type
        
        try:
            response = self.session.get(f"{self.base_url}/content/search", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f"HTTP {response.status_code}"}
        except Exception as e:
            return {'error': str(e)}
    
    def get_popular_content(self, content_type=None, limit=10):
        """Get popular content with optional type filtering"""
        params = {'limit': limit}
        if content_type:
            params['type'] = content_type
        
        try:
            response = self.session.get(f"{self.base_url}/content/popular", params=params)
            if response.status_code == 200:
                return response.json()
            else:
                return {'error': f"HTTP {response.status_code}"}
        except Exception as e:
            return {'error': str(e)}

def print_health_status(client):
    """Print health status with content types"""
    print("🏥 Checking API Health...")
    health = client.health_check()
    
    if health['status'] == 'healthy':
        print("✅ API is healthy!")
        print(f"   Model loaded: {health['model_loaded']}")
        print(f"   Supported content types: {', '.join(health['supported_content_types'])}")
        return True
    else:
        print(f"❌ API is unhealthy: {health.get('error', 'Unknown error')}")
        return False

def print_content_types(client):
    """Print supported content types"""
    print("\n📚 Supported Content Types:")
    content_types = client.get_content_types()
    
    if 'error' not in content_types:
        for content_type, display_name in content_types['content_types'].items():
            print(f"   - {content_type}: {display_name}")
    else:
        print(f"❌ Error getting content types: {content_types['error']}")

def print_recommendations(result, content_type=None):
    """Print recommendations in a formatted way"""
    if 'error' in result:
        print(f"❌ Error getting recommendations: {result['error']}")
        return
    
    print(f"\n🎯 Recommendations for User {result['user_id']}:")
    if content_type:
        print(f"   Content Type: {content_type}")
    print(f"   Count: {result['count']}")
    
    for i, rec in enumerate(result['recommendations'], 1):
        print(f"   {i}. {rec['title']}")
        print(f"      Type: {rec['content_type']}")
        print(f"      Genre: {rec['genre']}")
        if 'similarity_score' in rec:
            print(f"      Similarity: {rec['similarity_score']:.3f}")
        print()

def print_user_stats(result):
    """Print user statistics with content breakdown"""
    if 'error' in result:
        print(f"❌ Error getting user stats: {result['error']}")
        return
    
    stats = result['stats']
    print(f"\n👤 User {result['user_id']} Statistics:")
    print(f"   Total Ratings: {stats['total_ratings']}")
    print(f"   Average Rating: {stats['average_rating']:.2f}")
    print(f"   High Ratings: {stats['high_ratings']}")
    print(f"   Favorite Genres: {', '.join(stats['favorite_genres'])}")
    
    content_breakdown = stats.get('content_type_breakdown', {})
    print(f"   Content Type Breakdown:")
    for content_type, count in content_breakdown.items():
        print(f"     - {content_type}: {count}")

def print_search_results(result):
    """Print search results"""
    if 'error' in result:
        print(f"❌ Error searching content: {result['error']}")
        return
    
    print(f"\n🔍 Search Results for '{result['query']}':")
    if result.get('content_type_filter'):
        print(f"   Content Type Filter: {result['content_type_filter']}")
    print(f"   Found: {result['count']} results")
    
    for i, item in enumerate(result['results'], 1):
        print(f"   {i}. {item['title']}")
        print(f"      Type: {item['content_type']}")
        print(f"      Genre: {item['genre']}")
        print()

def print_popular_content(result):
    """Print popular content"""
    if 'error' in result:
        print(f"❌ Error getting popular content: {result['error']}")
        return
    
    print(f"\n⭐ Popular Content:")
    if result.get('content_type_filter'):
        print(f"   Content Type Filter: {result['content_type_filter']}")
    print(f"   Count: {result['count']}")
    
    for i, item in enumerate(result['popular_content'], 1):
        print(f"   {i}. {item['title']}")
        print(f"      Type: {item['content_type']}")
        print(f"      Rating: {item['avg_rating']:.2f} ({item['rating_count']} votes)")
        print()

def demo_mode():
    """Run a comprehensive demo of all features"""
    print("🎬 MULTI-CONTENT RECOMMENDATION SYSTEM DEMO")
    print("=" * 60)
    
    client = RecommendationClient()
    
    # Health check
    if not print_health_status(client):
        return
    
    # Content types
    print_content_types(client)
    
    # Demo for different content types
    content_types = ['movies', 'tv_shows', 'podcasts', 'books']
    
    for content_type in content_types:
        print(f"\n🎯 Getting {content_type.title()} Recommendations for User 1:")
        result = client.get_recommendations(1, content_type, 3)
        print_recommendations(result, content_type)
    
    # User stats
    print("\n📊 User Statistics:")
    stats_result = client.get_user_stats(1)
    print_user_stats(stats_result)
    
    # Search demo
    print("\n🔍 Search Demo:")
    search_result = client.search_content("star", limit=5)
    print_search_results(search_result)
    
    # Popular content
    print("\n⭐ Popular Content Demo:")
    popular_result = client.get_popular_content(limit=5)
    print_popular_content(popular_result)
    
    print("\n🎉 Demo completed!")

def interactive_mode():
    """Interactive mode for testing different features"""
    print("🎮 INTERACTIVE MODE")
    print("=" * 40)
    
    client = RecommendationClient()
    
    if not print_health_status(client):
        print("❌ Cannot connect to API. Make sure the server is running.")
        return
    
    while True:
        print("\n" + "=" * 40)
        print("Choose an option:")
        print("1. Get recommendations for a user")
        print("2. Get user statistics")
        print("3. Search content")
        print("4. Get popular content")
        print("5. Show supported content types")
        print("6. Health check")
        print("0. Exit")
        
        choice = input("\nEnter your choice (0-6): ").strip()
        
        if choice == '0':
            print("👋 Goodbye!")
            break
        elif choice == '1':
            user_id = input("Enter user ID: ").strip()
            content_type = input("Enter content type (movies/tv_shows/podcasts/books) or press Enter for all: ").strip()
            limit = input("Enter number of recommendations (default 5): ").strip()
            
            try:
                user_id = int(user_id)
                limit = int(limit) if limit else 5
                content_type = content_type if content_type else None
                
                result = client.get_recommendations(user_id, content_type, limit)
                print_recommendations(result, content_type)
            except ValueError:
                print("❌ Invalid input. Please enter valid numbers.")
        
        elif choice == '2':
            user_id = input("Enter user ID: ").strip()
            try:
                user_id = int(user_id)
                result = client.get_user_stats(user_id)
                print_user_stats(result)
            except ValueError:
                print("❌ Invalid user ID.")
        
        elif choice == '3':
            query = input("Enter search query: ").strip()
            content_type = input("Enter content type filter (optional): ").strip()
            limit = input("Enter limit (default 10): ").strip()
            
            try:
                limit = int(limit) if limit else 10
                content_type = content_type if content_type else None
                
                result = client.search_content(query, content_type, limit)
                print_search_results(result)
            except ValueError:
                print("❌ Invalid limit.")
        
        elif choice == '4':
            content_type = input("Enter content type filter (optional): ").strip()
            limit = input("Enter limit (default 10): ").strip()
            
            try:
                limit = int(limit) if limit else 10
                content_type = content_type if content_type else None
                
                result = client.get_popular_content(content_type, limit)
                print_popular_content(result)
            except ValueError:
                print("❌ Invalid limit.")
        
        elif choice == '5':
            print_content_types(client)
        
        elif choice == '6':
            print_health_status(client)
        
        else:
            print("❌ Invalid choice. Please try again.")

def main():
    """Main function"""
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'interactive':
        interactive_mode()
    else:
        demo_mode()

if __name__ == "__main__":
    main() 