#!/usr/bin/env python3
"""
Multi-Content Data Generator
Creates mock datasets for TV shows, podcasts, and books to demonstrate
a real multi-content recommendation system.
"""

import pandas as pd
import numpy as np
import json
from datetime import datetime

def generate_tv_shows_data():
    """Generate mock TV shows dataset"""
    tv_shows = [
        {"id": 10001, "title": "Breaking Bad", "genres": "Crime|Drama|Thriller", "type": "tv_shows", "description": "A high school chemistry teacher turned methamphetamine manufacturer"},
        {"id": 10002, "title": "Game of Thrones", "genres": "Action|Adventure|Drama|Fantasy", "type": "tv_shows", "description": "Nine noble families fight for control over the lands of Westeros"},
        {"id": 10003, "title": "The Office", "genres": "Comedy|Documentary", "type": "tv_shows", "description": "A mockumentary on a group of typical office workers"},
        {"id": 10004, "title": "Stranger Things", "genres": "Drama|Horror|Mystery|Sci-Fi", "type": "tv_shows", "description": "When a young boy disappears, his mother must confront terrifying forces"},
        {"id": 10005, "title": "Friends", "genres": "Comedy|Romance", "type": "tv_shows", "description": "Follows the personal and professional lives of six twenty to thirty-something-year-old friends"},
        {"id": 10006, "title": "The Crown", "genres": "Biography|Drama|History", "type": "tv_shows", "description": "Follows the political rivalries and romance of Queen Elizabeth II's reign"},
        {"id": 10007, "title": "Black Mirror", "genres": "Drama|Sci-Fi|Thriller", "type": "tv_shows", "description": "An anthology series exploring a twisted, high-tech world"},
        {"id": 10008, "title": "The Mandalorian", "genres": "Action|Adventure|Drama|Sci-Fi", "type": "tv_shows", "description": "The travels of a lone bounty hunter in the outer reaches of the galaxy"},
        {"id": 10009, "title": "The Witcher", "genres": "Action|Adventure|Drama|Fantasy", "type": "tv_shows", "description": "Geralt of Rivia, a solitary monster hunter, struggles to find his place in a world"},
        {"id": 10010, "title": "The Queen's Gambit", "genres": "Drama", "type": "tv_shows", "description": "Orphaned at the tender age of nine, prodigious introvert Beth Harmon discovers and masters the game of chess"},
        {"id": 10011, "title": "Planet Earth", "genres": "Documentary|Nature", "type": "tv_shows", "description": "A nature documentary series exploring the Earth's most spectacular natural wonders"},
        {"id": 10012, "title": "The Last Dance", "genres": "Documentary|Sport", "type": "tv_shows", "description": "Charting the rise of the 1990's Chicago Bulls, led by Michael Jordan"},
        {"id": 10013, "title": "The Bachelor", "genres": "Reality-TV|Romance", "type": "tv_shows", "description": "A single bachelor dates multiple women over several weeks"},
        {"id": 10014, "title": "Survivor", "genres": "Adventure|Game-Show|Reality-TV", "type": "tv_shows", "description": "A group of people are stranded on an island and compete for a cash prize"},
        {"id": 10015, "title": "The Great British Bake Off", "genres": "Game-Show|Reality-TV", "type": "tv_shows", "description": "Bakers compete against each other in a series of challenges"}
    ]
    
    df = pd.DataFrame(tv_shows)
    df['combined_features'] = df['title'] + ' ' + df['genres'] + ' ' + df['description']
    return df

def generate_podcasts_data():
    """Generate mock podcasts dataset"""
    podcasts = [
        {"id": 20001, "title": "The Joe Rogan Experience", "genres": "Talk-Show|Comedy|News", "type": "podcasts", "description": "Long form conversations with guests from various fields"},
        {"id": 20002, "title": "Serial", "genres": "Crime|Documentary|Mystery", "type": "podcasts", "description": "Investigative journalism podcast that tells one story over multiple episodes"},
        {"id": 20003, "title": "This American Life", "genres": "Documentary|News|Stories", "type": "podcasts", "description": "Weekly public radio program and podcast"},
        {"id": 20004, "title": "The Daily", "genres": "News|Politics", "type": "podcasts", "description": "Daily news podcast from The New York Times"},
        {"id": 20005, "title": "Radiolab", "genres": "Science|Documentary|Education", "type": "podcasts", "description": "Investigates a strange world through science and storytelling"},
        {"id": 20006, "title": "Stuff You Should Know", "genres": "Education|Comedy", "type": "podcasts", "description": "Educational podcast that explains how things work"},
        {"id": 20007, "title": "The Tim Ferriss Show", "genres": "Business|Education|Interviews", "type": "podcasts", "description": "Interviews with world-class performers to extract tools and tactics"},
        {"id": 20008, "title": "Freakonomics Radio", "genres": "Economics|Education|News", "type": "podcasts", "description": "Explores the hidden side of everything"},
        {"id": 20009, "title": "How I Built This", "genres": "Business|Interviews|Stories", "type": "podcasts", "description": "Stories behind some of the world's best known companies"},
        {"id": 20010, "title": "The Moth", "genres": "Stories|Comedy|Drama", "type": "podcasts", "description": "True stories told live without notes"},
        {"id": 20011, "title": "99% Invisible", "genres": "Design|Documentary|Education", "type": "podcasts", "description": "About all the thought that goes into the things we don't think about"},
        {"id": 20012, "title": "Reply All", "genres": "Technology|Stories|Mystery", "type": "podcasts", "description": "Stories about people grappling with the forces reshaping our world"},
        {"id": 20013, "title": "WTF with Marc Maron", "genres": "Comedy|Interviews|Talk-Show", "type": "podcasts", "description": "Comedian Marc Maron interviews celebrities and fellow comedians"},
        {"id": 20014, "title": "The Ezra Klein Show", "genres": "Politics|News|Interviews", "type": "podcasts", "description": "Conversations about big ideas and important questions"},
        {"id": 20015, "title": "Hidden Brain", "genres": "Psychology|Science|Education", "type": "podcasts", "description": "Explores the unconscious patterns that drive human behavior"}
    ]
    
    df = pd.DataFrame(podcasts)
    df['combined_features'] = df['title'] + ' ' + df['genres'] + ' ' + df['description']
    return df

def generate_books_data():
    """Generate mock books dataset"""
    books = [
        {"id": 30001, "title": "To Kill a Mockingbird", "genres": "Classic|Drama|Fiction", "type": "books", "description": "Harper Lee's classic novel about racial injustice in the American South"},
        {"id": 30002, "title": "1984", "genres": "Dystopian|Fiction|Political", "type": "books", "description": "George Orwell's dystopian novel about totalitarian surveillance society"},
        {"id": 30003, "title": "The Great Gatsby", "genres": "Classic|Drama|Fiction|Romance", "type": "books", "description": "F. Scott Fitzgerald's novel about the Jazz Age and American Dream"},
        {"id": 30004, "title": "Pride and Prejudice", "genres": "Classic|Romance|Fiction", "type": "books", "description": "Jane Austen's romantic novel about the relationship between Elizabeth Bennet and Mr. Darcy"},
        {"id": 30005, "title": "The Catcher in the Rye", "genres": "Classic|Coming-of-age|Fiction", "type": "books", "description": "J.D. Salinger's novel about teenage alienation and loss of innocence"},
        {"id": 30006, "title": "Lord of the Flies", "genres": "Allegory|Fiction|Thriller", "type": "books", "description": "William Golding's novel about the dark side of human nature"},
        {"id": 30007, "title": "Animal Farm", "genres": "Allegory|Political|Satire", "type": "books", "description": "George Orwell's allegorical novella about the Russian Revolution"},
        {"id": 30008, "title": "The Hobbit", "genres": "Fantasy|Adventure|Fiction", "type": "books", "description": "J.R.R. Tolkien's fantasy novel about Bilbo Baggins' journey"},
        {"id": 30009, "title": "The Alchemist", "genres": "Fiction|Philosophy|Adventure", "type": "books", "description": "Paulo Coelho's novel about following one's dreams"},
        {"id": 30010, "title": "The Kite Runner", "genres": "Drama|Fiction|Historical", "type": "books", "description": "Khaled Hosseini's novel about friendship and redemption in Afghanistan"},
        {"id": 30011, "title": "Sapiens", "genres": "History|Science|Non-fiction", "type": "books", "description": "Yuval Noah Harari's exploration of human history"},
        {"id": 30012, "title": "The Power of Habit", "genres": "Psychology|Self-help|Non-fiction", "type": "books", "description": "Charles Duhigg's book about how habits work and can be changed"},
        {"id": 30013, "title": "Atomic Habits", "genres": "Self-help|Psychology|Non-fiction", "type": "books", "description": "James Clear's guide to building good habits and breaking bad ones"},
        {"id": 30014, "title": "The Subtle Art of Not Giving a F*ck", "genres": "Self-help|Philosophy|Non-fiction", "type": "books", "description": "Mark Manson's counterintuitive approach to living a good life"},
        {"id": 30015, "title": "Thinking, Fast and Slow", "genres": "Psychology|Science|Non-fiction", "type": "books", "description": "Daniel Kahneman's exploration of the two systems that drive the way we think"}
    ]
    
    df = pd.DataFrame(books)
    df['combined_features'] = df['title'] + ' ' + df['genres'] + ' ' + df['description']
    return df

def generate_ratings_data():
    """Generate mock ratings data for all content types"""
    ratings = []
    
    # Generate ratings for TV shows (IDs 10001-10015)
    for user_id in range(1, 51):  # 50 users
        for show_id in range(10001, 10016):
            if np.random.random() < 0.3:  # 30% chance of rating
                rating = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.15, 0.25, 0.3, 0.2])
                ratings.append({
                    'userId': user_id,
                    'contentId': show_id,
                    'contentType': 'tv_shows',
                    'rating': rating,
                    'timestamp': datetime.now().isoformat()
                })
    
    # Generate ratings for podcasts (IDs 20001-20015)
    for user_id in range(1, 51):
        for podcast_id in range(20001, 20016):
            if np.random.random() < 0.25:  # 25% chance of rating
                rating = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.15, 0.25, 0.3, 0.2])
                ratings.append({
                    'userId': user_id,
                    'contentId': podcast_id,
                    'contentType': 'podcasts',
                    'rating': rating,
                    'timestamp': datetime.now().isoformat()
                })
    
    # Generate ratings for books (IDs 30001-30015)
    for user_id in range(1, 51):
        for book_id in range(30001, 30016):
            if np.random.random() < 0.2:  # 20% chance of rating
                rating = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.15, 0.25, 0.3, 0.2])
                ratings.append({
                    'userId': user_id,
                    'contentId': book_id,
                    'contentType': 'books',
                    'rating': rating,
                    'timestamp': datetime.now().isoformat()
                })
    
    return pd.DataFrame(ratings)

def create_multi_content_datasets():
    """Create all multi-content datasets"""
    print("🎬 Generating Multi-Content Datasets...")
    
    # Generate datasets
    tv_shows_df = generate_tv_shows_data()
    podcasts_df = generate_podcasts_data()
    books_df = generate_books_data()
    ratings_df = generate_ratings_data()
    
    # Save datasets
    tv_shows_df.to_csv('tv_shows.csv', index=False)
    podcasts_df.to_csv('podcasts.csv', index=False)
    books_df.to_csv('books.csv', index=False)
    ratings_df.to_csv('multi_content_ratings.csv', index=False)
    
    # Create combined content dataset
    combined_content = pd.concat([
        tv_shows_df,
        podcasts_df,
        books_df
    ], ignore_index=True)
    combined_content.to_csv('combined_content.csv', index=False)
    
    print("✅ Datasets created successfully!")
    print(f"   TV Shows: {len(tv_shows_df)} items")
    print(f"   Podcasts: {len(podcasts_df)} items")
    print(f"   Books: {len(books_df)} items")
    print(f"   Ratings: {len(ratings_df)} ratings")
    print(f"   Combined Content: {len(combined_content)} items")
    
    return {
        'tv_shows': tv_shows_df,
        'podcasts': podcasts_df,
        'books': books_df,
        'ratings': ratings_df,
        'combined': combined_content
    }

def create_sample_queries():
    """Create sample API queries for testing"""
    queries = {
        "tv_shows": [
            "GET /content/search?q=breaking&type=tv_shows",
            "GET /content/popular?type=tv_shows&limit=5",
            "POST /recommend -d '{\"userId\": 1, \"contentType\": \"tv_shows\", \"numRecommendations\": 3}'"
        ],
        "podcasts": [
            "GET /content/search?q=serial&type=podcasts",
            "GET /content/popular?type=podcasts&limit=5",
            "POST /recommend -d '{\"userId\": 1, \"contentType\": \"podcasts\", \"numRecommendations\": 3}'"
        ],
        "books": [
            "GET /content/search?q=classic&type=books",
            "GET /content/popular?type=books&limit=5",
            "POST /recommend -d '{\"userId\": 1, \"contentType\": \"books\", \"numRecommendations\": 3}'"
        ]
    }
    
    print("\n📝 Sample API Queries:")
    for content_type, queries_list in queries.items():
        print(f"\n{content_type.upper()}:")
        for query in queries_list:
            print(f"   {query}")

if __name__ == "__main__":
    datasets = create_multi_content_datasets()
    create_sample_queries()
    
    print("\n🎉 Multi-content datasets ready for integration!")
    print("\nNext steps:")
    print("1. Integrate these datasets into your Flask app")
    print("2. Update the content type determination logic")
    print("3. Test with the new multi-content data") 