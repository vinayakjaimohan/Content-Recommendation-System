import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiUser, FiLogOut } from 'react-icons/fi';
import RecommendationCard from './RecommendationCard';
import './DashboardPage.css';

const genreOptions = [
  'Sci-Fi',
  'Comedy',
  'Fantasy',
  'Drama',
  'Horror',
  'Thriller',
  'Action',
];

const Dashboard = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [selectedType, setSelectedType] = useState('');
  const [selectedGenre, setSelectedGenre] = useState('');
  const [userPreferences, setUserPreferences] = useState('');
  const [showPreferences, setShowPreferences] = useState(false);
  const [activeTab, setActiveTab] = useState('recommendations');
  const [watchHistory, setWatchHistory] = useState([]);
  const [newHistoryItem, setNewHistoryItem] = useState({ title: '', type: '', genre: '', rating: '' });
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.clear(); 
    navigate('/login'); 
  };

  const addToHistory = () => {
    if (newHistoryItem.title && newHistoryItem.type) {
      const historyItem = {
        id: Date.now(),
        ...newHistoryItem,
        dateAdded: new Date().toLocaleDateString()
      };
      setWatchHistory([...watchHistory, historyItem]);
      setNewHistoryItem({ title: '', type: '', genre: '', rating: '' });
    }
  };

  const removeFromHistory = (id) => {
    setWatchHistory(watchHistory.filter(item => item.id !== id));
  };

  const fetchRecommendations = async () => {
    try {
      const requestData = {
        type: selectedType,
        genre: selectedGenre,
        preferences: userPreferences,
        watchHistory: watchHistory,
        timestamp: new Date().toISOString()
      };

      console.log('Sending to Gemini:', requestData);

      const response = await fetch('http://localhost:8000/api/recommendations/gemini', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestData)
      });

      if (response.ok) {
        const data = await response.json();
        console.log('Gemini recommendations received:', data);
        setRecommendations(data);
      } else {
        console.error('Failed to fetch recommendations:', response.status);
        setRecommendations(getFallbackRecommendations());
      }
    } catch (error) {
      console.error('Error fetching recommendations:', error);
      setRecommendations(getFallbackRecommendations());
    }
  };

  const getFallbackRecommendations = () => {
    let dummyData = [];
    switch (selectedType) {
      case 'books':
        dummyData = [
          { id: 1, title: 'Dune', type: 'Sci-Fi' },
          { id: 2, title: 'The Hobbit', type: 'Fantasy' },
          { id: 3, title: 'Gone Girl', type: 'Thriller' },
          { id: 4, title: 'The Shining', type: 'Horror' },
        ];
        break;
      case 'movies':
        dummyData = [
          { id: 5, title: 'Inception', type: 'Sci-Fi' },
          { id: 6, title: 'The Godfather', type: 'Drama' },
          { id: 7, title: 'Interstellar', type: 'Sci-Fi' },
          { id: 8, title: 'The Conjuring', type: 'Horror' },
        ];
        break;
      case 'tv':
        dummyData = [
          { id: 9, title: 'Stranger Things', type: 'Fantasy' },
          { id: 10, title: 'Breaking Bad', type: 'Drama' },
          { id: 11, title: 'The Boys', type: 'Action' },
        ];
        break;
      case 'podcast':
        dummyData = [
          { id: 12, title: 'Lore', type: 'Horror' },
          { id: 13, title: 'Serial', type: 'Thriller' },
          { id: 14, title: 'Science Vs', type: 'Sci-Fi' },
        ];
        break;
      default:
        dummyData = [];
    }

    const filtered = selectedGenre
      ? dummyData.filter((item) => item.type === selectedGenre)
      : dummyData;

    return filtered;
  };

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <button className="logout-btn" onClick={handleLogout} title="Logout">
          <FiLogOut />
        </button>
        <button className="profile-btn" onClick={() => navigate('/profile')} title="Profile">
          <FiUser />
        </button>
      </div>

      <div className="dashboard-container">
        <div className="dashboard-content">
          <div className="title-section">
            <h1 className="dashboard-title">Dashboard</h1>
            <p className="dashboard-subtitle">Manage your preferences and get personalized recommendations</p>
          </div>

          <div className="tabs-section">
            <div className="tabs">
              <button 
                className={`tab ${activeTab === 'recommendations' ? 'active' : ''}`}
                onClick={() => setActiveTab('recommendations')}
              >
                Get Recommendations
              </button>
              <button 
                className={`tab ${activeTab === 'history' ? 'active' : ''}`}
                onClick={() => setActiveTab('history')}
              >
                My History ({watchHistory.length})
              </button>
            </div>
          </div>

          {activeTab === 'recommendations' && (
            <>
              <div className="preferences-section">
                <div className="preferences-header">
                  <h3 className="section-title">Your Preferences</h3>
                  <button 
                    className="toggle-preferences-btn"
                    onClick={() => setShowPreferences(!showPreferences)}
                  >
                    {showPreferences ? 'Hide' : 'Add Preferences'}
                  </button>
                </div>
                
                {showPreferences && (
                  <div className="preferences-form">
                    <label htmlFor="preferences" className="preferences-label">
                      Tell us what you like (this helps tailor recommendations):
                    </label>
                    <textarea
                      id="preferences"
                      className="preferences-input"
                      placeholder="e.g., I love complex characters, mind-bending plots, stories with strong female leads, dark themes, comedy with heart, true crime, space exploration..."
                      value={userPreferences}
                      onChange={(e) => setUserPreferences(e.target.value)}
                      rows={4}
                    />
                  </div>
                )}
              </div>

              <div className="category-section">
                <h3 className="section-title">Choose Category</h3>
                <div className="category-grid">
                  {['tv', 'books', 'movies', 'podcast'].map((type) => (
                    <button
                      key={type}
                      className={`category-btn ${selectedType === type ? 'active' : ''}`}
                      onClick={() => {
                        setSelectedType(type);
                        setRecommendations([]);
                        setSelectedGenre('');
                      }}
                    >
                      {type.charAt(0).toUpperCase() + type.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              {selectedType && (
                <div className="genre-section">
                  <h3 className="section-title">Select Genre</h3>
                  <div className="genre-grid">
                    {genreOptions.map((genre) => (
                      <button
                        key={genre}
                        className={`genre-btn ${selectedGenre === genre ? 'active' : ''}`}
                        onClick={() => setSelectedGenre((prev) => (prev === genre ? '' : genre))}
                      >
                        {genre}
                      </button>
                    ))}
                  </div>
                  <div className="action-section">
                    <button className="recommend-btn" onClick={fetchRecommendations}>
                      Get Recommendations
                    </button>
                  </div>
                </div>
              )}

              {recommendations.length > 0 && (
                <div className="results-section">
                  <h3 className="section-title">Recommendations</h3>
                  <div className="recommendations-grid">
                    {recommendations.map((item) => (
                      <RecommendationCard key={item.id} title={item.title} type={item.type} />
                    ))}
                  </div>
                </div>
              )}

              {selectedType && recommendations.length === 0 && (
                <div className="empty-state">
                  <p>Click "Get Recommendations" to see results</p>
                </div>
              )}
            </>
          )}

          {activeTab === 'history' && (
            <div className="history-section">
              <div className="add-history-form">
                <h3 className="section-title">Add to Your History</h3>
                <div className="history-form-grid">
                  <div className="form-group">
                    <label className="form-label">Title</label>
                    <input
                      type="text"
                      className="form-input"
                      placeholder="Enter title"
                      value={newHistoryItem.title}
                      onChange={(e) => setNewHistoryItem({...newHistoryItem, title: e.target.value})}
                    />
                  </div>
                  <div className="form-group">
                    <label className="form-label">Type</label>
                    <select
                      className="form-input"
                      value={newHistoryItem.type}
                      onChange={(e) => setNewHistoryItem({...newHistoryItem, type: e.target.value})}
                    >
                      <option value="">Select type</option>
                      <option value="tv">TV Show</option>
                      <option value="movies">Movie</option>
                      <option value="books">Book</option>
                      <option value="podcast">Podcast</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Genre</label>
                    <select
                      className="form-input"
                      value={newHistoryItem.genre}
                      onChange={(e) => setNewHistoryItem({...newHistoryItem, genre: e.target.value})}
                    >
                      <option value="">Select genre</option>
                      {genreOptions.map(genre => (
                        <option key={genre} value={genre}>{genre}</option>
                      ))}
                    </select>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Rating (1-5)</label>
                    <select
                      className="form-input"
                      value={newHistoryItem.rating}
                      onChange={(e) => setNewHistoryItem({...newHistoryItem, rating: e.target.value})}
                    >
                      <option value="">Rate it</option>
                      <option value="5">5 - Loved it</option>
                      <option value="4">4 - Really liked it</option>
                      <option value="3">3 - It was okay</option>
                      <option value="2">2 - Didn't like it</option>
                      <option value="1">1 - Hated it</option>
                    </select>
                  </div>
                </div>
                <button className="add-history-btn" onClick={addToHistory}>
                  Add to History
                </button>
              </div>

              <div className="history-list">
                <h3 className="section-title">Your Watch History</h3>
                {watchHistory.length === 0 ? (
                  <div className="empty-state">
                    <p>No items in your history yet. Add some above!</p>
                  </div>
                ) : (
                  <div className="history-grid">
                    {watchHistory.map((item) => (
                      <div key={item.id} className="history-item">
                        <div className="history-item-header">
                          <h4 className="history-item-title">{item.title}</h4>
                          <button 
                            className="remove-history-btn"
                            onClick={() => removeFromHistory(item.id)}
                            title="Remove from history"
                          >
                            ×
                          </button>
                        </div>
                        <div className="history-item-details">
                          <span className="history-item-type">{item.type}</span>
                          {item.genre && <span className="history-item-genre">{item.genre}</span>}
                          {item.rating && <span className="history-item-rating">★ {item.rating}/5</span>}
                        </div>
                        <div className="history-item-date">Added: {item.dateAdded}</div>
                      </div>
                    ))}
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

export default Dashboard;
