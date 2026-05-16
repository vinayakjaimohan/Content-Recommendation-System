# Content Recommendation System

A comprehensive content recommendation platform that provides personalized recommendations for movies, books, TV shows, and podcasts using machine learning and AI technologies.

## 🚀 Features

- **Multi-Content Support**: Recommendations for movies, books, TV shows, and podcasts
- **AI-Powered Recommendations**: Integration with Google's Gemini AI for intelligent suggestions
- **Machine Learning Backend**: Flask-based ML service with scikit-learn
- **Modern Web Interface**: React frontend with responsive design
- **User Authentication**: JWT-based authentication system
- **Personalized Experience**: User preferences and watch history tracking

## 🏗️ Architecture

The system consists of three main components:

### Frontend (React + Vite)
- **Location**: `/frontend`
- **Tech Stack**: React 19, Vite, Tailwind CSS, Bootstrap, Framer Motion
- **Purpose**: User interface for interacting with the recommendation system

### Backend (Spring Boot)
- **Location**: `/backend`
- **Tech Stack**: Spring Boot 3.5.4, Java 17, MySQL, JWT Authentication
- **Purpose**: API server, user management, and business logic



## 📋 Prerequisites

- **Java 17** or higher
- **Node.js 18** or higher
- **Python 3.8** or higher
- **MySQL** database
- **Maven** (for Java backend)
- **Git**

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ContentRecomendation
```

### 2. Set Up the Backend (Spring Boot)

```bash
cd backend

# Install dependencies
mvn clean install

# Configure database
# Edit src/main/resources/application.properties with your MySQL credentials

# Run the application
mvn spring-boot:run
```

The backend will start on `http://localhost:8080`



The ML backend will start on `http://localhost:5000`

### 4. Set Up the Frontend (React)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:5173`

## 🔑 Configuration

### Database Setup
1. Create a MySQL database
2. Update `backend/src/main/resources/application.properties` with your database credentials
3. The application will automatically create tables on first run

### Gemini AI Integration
To enable AI-powered recommendations:

1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Set the environment variable:
   ```bash
   # Windows (PowerShell)
   $env:GEMINI_API_KEY="your-api-key-here"
   
   # Windows (Command Prompt)
   set GEMINI_API_KEY=your-api-key-here
   
   # Linux/Mac
   export GEMINI_API_KEY="your-api-key-here"
   ```

3. Or add to `backend/src/main/resources/application.properties`:
   ```properties
   gemini.api.key=your-api-key-here
   ```

## 🚀 Quick Start

1. **Start all services**:
   ```bash
   # Terminal 1 - Backend
   cd backend && mvn spring-boot:run
   
   # Terminal 2 - Frontend
   cd frontend && npm run dev
   ```

2. **Open your browser** and navigate to `http://localhost:5173`

3. **Register a new account** or login

4. **Get recommendations**:
   - Select content type (movies, books, TV, podcasts)
   - Choose a genre (optional)
   - Add your preferences
   - Click "Get Recommendations"

## 📁 Project Structure

```
ContentRecomendation/
├── frontend/                 # React application
│   ├── src/                 # Source code
│   ├── public/              # Static assets
│   └── package.json         # Dependencies
├── backend/                 # Spring Boot application
│   ├── src/                 # Source code
│   ├── pom.xml             # Maven configuration
│   └── target/             # Build output
├── flask_ml_backend/        # Flask ML service
│   ├── app.py              # Main Flask application
│   ├── requirements.txt     # Python dependencies
│   └── *.pkl              # ML models
├── processed_movies.csv     # Movie dataset
├── processed_links.csv      # Links dataset
└── README.md               # This file
```

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run lint         # Run ESLint
```

### Backend Development
```bash
cd backend
mvn spring-boot:run  # Run with hot reload
mvn test            # Run tests
mvn clean install   # Clean build
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Recommendations
- `POST /api/recommendations/gemini` - AI-powered recommendations
- `GET /api/recommendations/{type}` - Get recommendations by type
- `POST /api/recommendations/preferences` - Save user preferences

### User Management
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update user profile
- `GET /api/user/history` - Get user watch history

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 8080, 5000, and 5173 are available
2. **Database connection**: Verify MySQL is running and credentials are correct
3. **Python dependencies**: Ensure you're using the correct Python version and virtual environment
4. **Node modules**: Delete `node_modules` and run `npm install` if you encounter dependency issues


---

