import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiCheck, FiX, FiHeart } from 'react-icons/fi';
import './OnboardingPage.css';

const OnboardingPage = () => {
  const [currentStep, setCurrentStep] = useState(1);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [likedItems, setLikedItems] = useState([]);
  const [currentRecommendations, setCurrentRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const initialItems = {
    movies: [
      { id: 1, title: 'The Dark Knight', genre: 'Action' },
      { id: 2, title: 'Inception', genre: 'Sci-Fi' },
      { id: 3, title: 'The Godfather', genre: 'Drama' },
      { id: 4, title: 'Pulp Fiction', genre: 'Crime' },
      { id: 5, title: 'Interstellar', genre: 'Sci-Fi' },
      { id: 6, title: 'The Shawshank Redemption', genre: 'Drama' },
    ],
    books: [
      { id: 7, title: 'Dune', genre: 'Sci-Fi' },
      { id: 8, title: 'The Hobbit', genre: 'Fantasy' },
      { id: 9, title: '1984', genre: 'Dystopian' },
      { id: 10, title: 'To Kill a Mockingbird', genre: 'Drama' },
      { id: 11, title: 'Harry Potter', genre: 'Fantasy' },
      { id: 12, title: 'The Great Gatsby', genre: 'Classic' },
    ],
    tv: [
      { id: 13, title: 'Breaking Bad', genre: 'Drama' },
      { id: 14, title: 'Stranger Things', genre: 'Sci-Fi' },
      { id: 15, title: 'The Office', genre: 'Comedy' },
      { id: 16, title: 'Game of Thrones', genre: 'Fantasy' },
      { id: 17, title: 'Friends', genre: 'Comedy' },
      { id: 18, title: 'The Crown', genre: 'Drama' },
    ],
    podcast: [
      { id: 19, title: 'Serial', genre: 'True Crime' },
      { id: 20, title: 'This American Life', genre: 'Storytelling' },
      { id: 21, title: 'Joe Rogan Experience', genre: 'Interview' },
      { id: 22, title: 'Radiolab', genre: 'Science' },
      { id: 23, title: 'My Favorite Murder', genre: 'True Crime' },
      { id: 24, title: 'Conan O\'Brien Needs a Friend', genre: 'Comedy' },
    ]
  };

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
    setCurrentStep(2);
  };

  const handleItemLike = async (item) => {
    const newLikedItems = [...likedItems, item];
    setLikedItems(newLikedItems);
    
    setIsLoading(true);
    
    setTimeout(() => {
      const similarItems = getSimilarItems(item, selectedCategory);
      setCurrentRecommendations(similarItems);
      setIsLoading(false);
    }, 800);
  };

  const getSimilarItems = (likedItem, category) => {
    const allItems = initialItems[category];
    return allItems
      .filter(item => 
        item.genre === likedItem.genre && 
        item.id !== likedItem.id &&
        !likedItems.some(liked => liked.id === item.id)
      )
      .slice(0, 4);
  };

  const handleSkipItem = (item) => {
    setCurrentRecommendations(prev => 
      prev.filter(rec => rec.id !== item.id)
    );
  };

  const handleFinishOnboarding = () => {
    localStorage.setItem('userLikes', JSON.stringify(likedItems));
    localStorage.setItem('onboardingComplete', 'true');
    navigate('/dashboard');
  };

  const getInitialItems = () => {
    return selectedCategory ? initialItems[selectedCategory] : [];
  };

  return (
    <div className="onboarding-page">
      <div className="onboarding-container">
        <div className="onboarding-content">
          {currentStep === 1 && (
            <div className="step-content">
              <div className="step-header">
                <h1 className="onboarding-title">Welcome! Let's personalize your experience</h1>
                <p className="onboarding-subtitle">Choose a category to get started</p>
              </div>

              <div className="category-selection">
                {Object.keys(initialItems).map((category) => (
                  <button
                    key={category}
                    className="category-card"
                    onClick={() => handleCategorySelect(category)}
                  >
                    <div className="category-icon">
                      {category === 'movies' && '🎬'}
                      {category === 'books' && '📚'}
                      {category === 'tv' && '📺'}
                      {category === 'podcast' && '🎧'}
                    </div>
                    <span className="category-name">
                      {category.charAt(0).toUpperCase() + category.slice(1)}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {currentStep === 2 && (
            <div className="step-content">
              <div className="step-header">
                <h2 className="onboarding-title">
                  Great! Now tell us what you like
                </h2>
                <p className="onboarding-subtitle">
                  Click the heart on items you enjoy. We'll find similar recommendations for you.
                </p>
                <div className="progress-info">
                  <span className="liked-count">{likedItems.length} items liked</span>
                  <button className="finish-btn" onClick={handleFinishOnboarding}>
                    Done
                  </button>
                </div>
              </div>

              <div className="items-section">
                {!isLoading && currentRecommendations.length === 0 && (
                  <div className="initial-items">
                    <h3 className="section-title">Popular {selectedCategory}</h3>
                    <div className="items-grid">
                      {getInitialItems().map((item) => (
                        <div key={item.id} className="item-card">
                          <div className="item-info">
                            <h4 className="item-title">{item.title}</h4>
                            <span className="item-genre">{item.genre}</span>
                          </div>
                          <button
                            className="like-btn"
                            onClick={() => handleItemLike(item)}
                            title="I like this"
                          >
                            <FiHeart />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {isLoading && (
                  <div className="loading-state">
                    <div className="loading-spinner"></div>
                    <p>Finding similar recommendations...</p>
                  </div>
                )}

                {!isLoading && currentRecommendations.length > 0 && (
                  <div className="recommendations-section">
                    <h3 className="section-title">Based on your likes, you might enjoy:</h3>
                    <div className="items-grid">
                      {currentRecommendations.map((item) => (
                        <div key={item.id} className="item-card">
                          <div className="item-info">
                            <h4 className="item-title">{item.title}</h4>
                            <span className="item-genre">{item.genre}</span>
                          </div>
                          <div className="item-actions">
                            <button
                              className="like-btn"
                              onClick={() => handleItemLike(item)}
                              title="I like this"
                            >
                              <FiHeart />
                            </button>
                            <button
                              className="skip-btn"
                              onClick={() => handleSkipItem(item)}
                              title="Not interested"
                            >
                              <FiX />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {likedItems.length > 0 && (
                  <div className="liked-items-summary">
                    <h3 className="section-title">Your Likes ({likedItems.length})</h3>
                    <div className="liked-items-list">
                      {likedItems.slice(-3).map((item) => (
                        <span key={item.id} className="liked-item-tag">
                          {item.title}
                        </span>
                      ))}
                      {likedItems.length > 3 && (
                        <span className="more-items">+{likedItems.length - 3} more</span>
                      )}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default OnboardingPage;
