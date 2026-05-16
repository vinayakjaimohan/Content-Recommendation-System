import { Link } from 'react-router-dom';
import './HomePage.css';

function HomePage() {
  return (
    <div className="homepage">
      <div className="container">
        <div className="content">
          <h1 className="title">Welcome</h1>
          <p className="subtitle">Choose an option to continue</p>

          <div className="buttons">
            <Link to="/register" className="btn btn-primary">
              Get Started
            </Link>
            <Link to="/login" className="btn btn-secondary">
              Sign In
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default HomePage;