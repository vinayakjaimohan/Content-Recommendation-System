# 🎬 Content Recommendation System

An AI-powered content recommendation platform that provides personalized suggestions for movies, books, TV shows, and podcasts using machine learning and Google's Gemini AI.

---

## 🚀 Features

- 🎥 Multi-Content Recommendations  
  Supports recommendations for:
  - Movies
  - Books
  - TV Shows
  - Podcasts

- 🤖 AI-Powered Suggestions  
  Integrated with Google Gemini AI for intelligent and context-aware recommendations.

- 🧠 Machine Learning Integration  
  Flask-based ML backend using scikit-learn for recommendation logic and experimentation.

- 🌐 Modern Responsive UI  
  Built using React, Vite, Tailwind CSS, and Framer Motion.

- 🔐 Secure Authentication  
  JWT-based user authentication and authorization.

- 👤 Personalized User Experience  
  Tracks user preferences and viewing history for better recommendations.

---

# 🏗️ System Architecture

The project consists of three major components:

## 🎨 Frontend (React + Vite)

**Location:** `/frontend`

### Tech Stack
- React 19
- Vite
- Tailwind CSS
- Bootstrap
- Framer Motion

### Responsibilities
- User Interface
- Content Browsing
- Authentication Pages
- Recommendation Display
- User Interaction

---

## ⚙️ Backend (Spring Boot)

**Location:** `/backend`

### Tech Stack
- Spring Boot 3
- Java 17
- MySQL
- JWT Authentication

### Responsibilities
- REST APIs
- Authentication & Authorization
- User Management
- Business Logic
- Gemini AI Integration

---

## 🧠 ML Recommendation Backend (Flask)

**Location:** `/flask_ml_backend`

### Tech Stack
- Python
- Flask
- scikit-learn
- Pandas
- NumPy

### Responsibilities
- Recommendation Model Experiments
- Similarity Calculations
- Content Filtering
- ML-based Suggestion Generation

---

# 👨‍💻 My Contributions

- Integrated Google Gemini AI for intelligent recommendations
- Worked on backend API development using Spring Boot
- Implemented and tested recommendation-related backend features
- Attempted training and experimentation of ML models for content suggestions
- Assisted in integrating frontend and backend communication

---

# 📋 Prerequisites

Before running the project, make sure you have:

- Java 17 or higher
- Node.js 18 or higher
- Python 3.8 or higher
- MySQL
- Maven
- Git

---

# 🛠️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone <repository-url>
cd ContentRecommendation
```

---

# ⚙️ Backend Setup (Spring Boot)

```bash
cd backend

# Install dependencies
mvn clean install

# Run the backend server
mvn spring-boot:run
```

Backend runs on:

```text
http://localhost:8080
```

---

# 🧠 ML Backend Setup (Flask)

```bash
cd flask_ml_backend

# Install dependencies
pip install -r requirements.txt

# Run Flask server
python app.py
```

ML backend runs on:

```text
http://localhost:5000
```

---

# 🌐 Frontend Setup (React)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# 🔑 Configuration

## 🗄️ Database Setup

1. Create a MySQL database
2. Update:

```text
backend/src/main/resources/application.properties
```

with your database credentials.

Example:

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/contentdb
spring.datasource.username=root
spring.datasource.password=yourpassword
```

---

# 🤖 Gemini AI Integration

To enable Gemini-powered recommendations:

## Step 1
Get a Gemini API key from Google AI Studio.

## Step 2
Set environment variable:

### Windows PowerShell
```powershell
$env:GEMINI_API_KEY="your-api-key"
```

### Windows CMD
```cmd
set GEMINI_API_KEY=your-api-key
```

### Linux / Mac
```bash
export GEMINI_API_KEY="your-api-key"
```

Or add directly in:

```properties
gemini.api.key=your-api-key
```

---

# 🚀 Quick Start

Start all services:

## Terminal 1 — Backend

```bash
cd backend
mvn spring-boot:run
```

## Terminal 2 — Flask ML Backend

```bash
cd flask_ml_backend
python app.py
```

## Terminal 3 — Frontend

```bash
cd frontend
npm run dev
```

---

# 📸 Screenshots

> Add screenshots here later for better project presentation.

Example:

```md
![Home Page](screenshots/home.png)
![Recommendations](screenshots/recommendations.png)
```

---

# 📁 Project Structure

```text
ContentRecommendation/
│
├── frontend/                  # React frontend
│   ├── src/
│   ├── public/
│   └── package.json
│
├── backend/                   # Spring Boot backend
│   ├── src/
│   ├── pom.xml
│   └── target/
│
├── flask_ml_backend/          # Flask ML recommendation service
│   ├── app.py
│   ├── requirements.txt
│   └── model_files/
│
├── datasets/                  # Dataset files
│
├── screenshots/               # Project screenshots
│
└── README.md
```

---

# 📊 API Endpoints

## 🔐 Authentication

| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | `/api/auth/register` | Register user |
| POST | `/api/auth/login` | Login user |
| POST | `/api/auth/logout` | Logout user |

---

## 🎯 Recommendations

| Method | Endpoint | Description |
|--------|-----------|-------------|
| POST | `/api/recommendations/gemini` | AI recommendations |
| GET | `/api/recommendations/{type}` | Recommendations by type |
| POST | `/api/recommendations/preferences` | Save user preferences |

---

## 👤 User Management

| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | `/api/user/profile` | Get user profile |
| PUT | `/api/user/profile` | Update profile |
| GET | `/api/user/history` | Get user history |

---

# 🔧 Development Commands

## Frontend

```bash
npm run dev
npm run build
npm run lint
```

---

## Backend

```bash
mvn spring-boot:run
mvn test
mvn clean install
```

---

# 🧪 Future Improvements

- Improved recommendation algorithms
- Better collaborative filtering models
- Deployment using Docker and Kubernetes
- Watchlist and bookmarking features
- Real-time recommendation updates
- Enhanced AI personalization

---

# 🤝 Contributing

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature/new-feature
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push to branch

```bash
git push origin feature/new-feature
```

5. Open a Pull Request

---

# 📝 License

This project is licensed under the MIT License.

---

# 🆘 Troubleshooting

## Common Issues

### Port Conflicts
Ensure ports:
- 8080
- 5000
- 5173

are available.

---

### Database Connection Issues
- Verify MySQL is running
- Check database credentials
- Ensure database exists

---

### Frontend Dependency Issues

```bash
rm -rf node_modules
npm install
```

---

### Python Dependency Issues

```bash
pip install -r requirements.txt
```

---

# ⭐ Acknowledgements

- Google Gemini AI
- Spring Boot
- React
- Flask
- scikit-learn
- Open-source community
