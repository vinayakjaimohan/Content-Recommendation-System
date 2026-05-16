import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function InterestsPage() {
  const [interests, setInterests] = useState([]);
  const [newInterest, setNewInterest] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (!userData) {
      navigate('/login');
      return;
    }
    fetchInterests();
  }, [navigate]);

  const fetchInterests = async () => {
    try {
      const userData = JSON.parse(localStorage.getItem('user'));
      const token = localStorage.getItem('token');
      const response = await axios.get(
        `http://localhost:8000/api/interests/user/${userData.id}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );
      setInterests(response.data);
    } catch (err) {
      setError('Failed to fetch interests');
    }
  };

  const handleAddInterest = async (e) => {
    e.preventDefault();
    if (!newInterest.trim()) return;

    setLoading(true);
    setError('');
    setMessage('');

    try {
      const userData = JSON.parse(localStorage.getItem('user'));
      const token = localStorage.getItem('token');
      const response = await axios.post(
        'http://localhost:8000/api/interests/add',
        {
          category: newInterest.trim(),
          userId: userData.id
        },
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setInterests([...interests, response.data]);
      setNewInterest('');
      setMessage('Interest added successfully!');
    } catch (err) {
      setError(err.response?.data || 'Failed to add interest');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteInterest = async (interestId) => {
    if (!window.confirm('Are you sure you want to remove this interest?')) {
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      await axios.delete(
        `http://localhost:8000/api/interests/${interestId}`,
        {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        }
      );

      setInterests(interests.filter(interest => interest.id !== interestId));
      setMessage('Interest removed successfully!');
    } catch (err) {
      setError(err.response?.data || 'Failed to remove interest');
    } finally {
      setLoading(false);
    }
  };

  const predefinedInterests = [
    'Action', 'Comedy', 'Drama', 'Horror', 'Romance', 'Sci-Fi', 'Thriller',
    'Adventure', 'Animation', 'Documentary', 'Fantasy', 'Mystery', 'War',
    'Biography', 'Crime', 'Family', 'History', 'Music', 'Sport', 'Western'
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">My Interests</h1>

        {message && (
          <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
            {message}
          </div>
        )}

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Add New Interest</h2>
          <form onSubmit={handleAddInterest} className="flex gap-4">
            <input
              type="text"
              value={newInterest}
              onChange={(e) => setNewInterest(e.target.value)}
              placeholder="Enter your interest (e.g., Action, Comedy, Drama)"
              className="flex-1 p-3 bg-gray-100 rounded-lg focus:outline-none"
              required
            />
            <button
              type="submit"
              disabled={loading}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
            >
              {loading ? 'Adding...' : 'Add Interest'}
            </button>
          </form>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">Quick Add</h2>
          <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-2">
            {predefinedInterests.map((interest) => (
              <button
                key={interest}
                onClick={() => setNewInterest(interest)}
                className="px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
              >
                {interest}
              </button>
            ))}
          </div>
        </div>

        <div className="bg-white rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold text-gray-800 mb-4">My Interests</h2>
          {interests.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No interests added yet. Add some interests to get personalized recommendations!</p>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {interests.map((interest) => (
                <div
                  key={interest.id}
                  className="flex justify-between items-center p-4 bg-gray-50 rounded-lg"
                >
                  <span className="font-medium text-gray-800">{interest.category}</span>
                  <button
                    onClick={() => handleDeleteInterest(interest.id)}
                    disabled={loading}
                    className="text-red-600 hover:text-red-800 disabled:text-gray-400"
                  >
                    ✕
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="text-center mt-6">
          <button
            onClick={() => navigate('/dashboard')}
            className="px-6 py-3 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
          >
            Back to Dashboard
          </button>
        </div>
      </div>
    </div>
  );
}

export default InterestsPage; 