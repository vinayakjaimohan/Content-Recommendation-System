import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FiArrowLeft } from 'react-icons/fi';
import axios from 'axios';
import './ProfilePage.css';

function ProfilePage() {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [statusMessage, setStatusMessage] = useState('');
  const [statusType, setStatusType] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchUserData = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/api/user/profile', {
          headers: { Authorization: `Bearer ${token}` },
        });

        const { name, email } = response.data;
        setName(name);
        setEmail(email);
      } catch (error) {
        console.error('Failed to fetch user data:', error);
        setStatusMessage('Failed to load user profile');
        setStatusType('error');
      }
    };

    fetchUserData();
  }, []);

  const updateProfile = async () => {
    try {
      const token = localStorage.getItem('token');

      const payload = { name, email };
      if (password) payload.password = password;

      await axios.put('http://localhost:8000/api/user/profile', payload, {
        headers: { Authorization: `Bearer ${token}` },
      });

      setStatusMessage('Profile updated successfully!');
      setStatusType('success');
      setPassword('');
    } catch (error) {
      console.error('Error updating profile:', error);
      setStatusMessage('Failed to update profile.');
      setStatusType('error');
    }
  };

  const deleteProfile = async () => {
    const confirmDelete = window.confirm(
      'Are you sure you want to delete your profile? This action cannot be undone.'
    );
    if (!confirmDelete) return;

    try {
      const token = localStorage.getItem('token');

      await axios.delete('http://localhost:8000/api/user/profile', {
        headers: { Authorization: `Bearer ${token}` },
      });

      localStorage.removeItem('token');
      setStatusMessage('Profile deleted successfully');
      setStatusType('success');

      setTimeout(() => {
        navigate('/login');
      }, 1500);
    } catch (error) {
      console.error('Error deleting profile:', error);
      setStatusMessage('Failed to delete profile');
      setStatusType('error');
    }
  };

  const handleBack = () => {
    navigate('/dashboard');
  };

  return (
    <div className="profile-page">
      <div className="profile-header">
        <button className="back-btn" onClick={handleBack} title="Back to Dashboard">
          <FiArrowLeft />
        </button>
      </div>

      <div className="profile-container">
        <div className="profile-content">
          <div className="title-section">
            <h1 className="profile-title">Profile Settings</h1>
            <p className="profile-subtitle">Update your account information</p>
          </div>

          <form className="profile-form">
            {statusMessage && (
              <div className={`message ${statusType === 'success' ? 'success-message' : 'error-message'}`}>
                {statusMessage}
              </div>
            )}

            <div className="form-group">
              <label htmlFor="name" className="form-label">Name</label>
              <input
                id="name"
                type="text"
                placeholder="Enter your name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="email" className="form-label">Email</label>
              <input
                id="email"
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="form-input"
              />
            </div>

            <div className="form-group">
              <label htmlFor="password" className="form-label">New Password</label>
              <input
                id="password"
                type="password"
                placeholder="Enter new password (optional)"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="form-input"
              />
            </div>

            <div className="button-group">
              <button
                type="button"
                className="update-btn"
                onClick={updateProfile}
              >
                Update Profile
              </button>
              <button
                type="button"
                className="delete-btn"
                onClick={deleteProfile}
              >
                Delete Account
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}

export default ProfilePage;
