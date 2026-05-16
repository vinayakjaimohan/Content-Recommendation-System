# Troubleshooting Guide

## Common Issues and Solutions

### 1. Python 3.13 Compatibility Issues

**Problem**: `BackendUnavailable: Cannot import 'setuptools.build_meta'`

**Solutions**:
1. **Use Python 3.11 or 3.12** (Recommended)
   ```bash
   # Install Python 3.11 or 3.12 from python.org
   # Then create a virtual environment
   python3.11 -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   pip install -r requirements.txt
   ```

2. **Upgrade setuptools first**
   ```bash
   pip install --upgrade setuptools wheel
   pip install -r requirements.txt
   ```

3. **Use the advanced installer**
   ```bash
   python install_dependencies.py
   ```

### 2. Package Installation Failures

**Problem**: `pip install` fails with dependency conflicts

**Solutions**:
1. **Install packages individually**:
   ```bash
   pip install Flask Flask-CORS pandas numpy scikit-learn joblib requests
   ```

2. **Use conda** (if available):
   ```bash
   conda install flask flask-cors pandas numpy scikit-learn joblib requests
   ```

3. **Create a clean virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   pip install --upgrade pip setuptools wheel
   pip install -r requirements.txt
   ```

### 3. Missing Data Files

**Problem**: `FileNotFoundError` for model files

**Solutions**:
1. **Ensure all files are present**:
   - `tfidf_vectorizer.pkl`
   - `processed_movies.csv`
   - `rating.csv`

2. **Check file permissions**:
   ```bash
   # Windows
   dir *.pkl *.csv
   
   # Linux/Mac
   ls -la *.pkl *.csv
   ```

### 4. Memory Issues

**Problem**: Out of memory errors with large datasets

**Solutions**:
1. **Increase system RAM** or use a machine with more memory
2. **Use data sampling** for development:
   ```python
   # In app.py, add sampling for development
   ratings_df = pd.read_csv(RATINGS_DATA_PATH).sample(n=100000)  # Sample 100k rows
   ```

### 5. Port Already in Use

**Problem**: `Address already in use`

**Solutions**:
1. **Change the port**:
   ```python
   app.run(debug=True, port=5001, host='0.0.0.0')  # Use port 5001
   ```

2. **Kill existing process**:
   ```bash
   # Windows
   netstat -ano | findstr :5000
   taskkill /PID <PID> /F
   
   # Linux/Mac
   lsof -ti:5000 | xargs kill -9
   ```

### 6. Import Errors

**Problem**: `ModuleNotFoundError`

**Solutions**:
1. **Check virtual environment activation**:
   ```bash
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Reinstall packages**:
   ```bash
   pip uninstall -y flask flask-cors pandas numpy scikit-learn joblib requests
   pip install -r requirements.txt
   ```

### 7. Model Loading Errors

**Problem**: `joblib.load()` fails

**Solutions**:
1. **Check file integrity**:
   ```python
   import joblib
   try:
       model = joblib.load('tfidf_vectorizer.pkl')
       print("Model loaded successfully")
   except Exception as e:
       print(f"Error loading model: {e}")
   ```

2. **Regenerate model files** if corrupted

### 8. Performance Issues

**Problem**: Slow response times

**Solutions**:
1. **Use smaller dataset** for development
2. **Add caching**:
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def get_user_profile_vector(user_id):
       # ... existing code
   ```

3. **Optimize data loading**:
   ```python
   # Load data once at startup
   movies_df = pd.read_csv('processed_movies.csv', index_col=0)
   ```

## Quick Fix Commands

### For Windows:
```cmd
# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install Flask Flask-CORS pandas numpy scikit-learn joblib requests

# Start server
python start_server.py
```

### For Linux/Mac:
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install Flask Flask-CORS pandas numpy scikit-learn joblib requests

# Start server
python start_server.py
```

## Testing the Installation

After installation, test with:
```bash
python test_api.py
```

## Getting Help

1. **Check the logs**: Look at `recommendation_api.log` for detailed error messages
2. **Run the test suite**: `python test_api.py`
3. **Use the interactive client**: `python example_client.py interactive`
4. **Check Python version**: `python --version`

## Common Error Messages

| Error | Solution |
|-------|----------|
| `BackendUnavailable` | Use Python 3.11/3.12 or upgrade setuptools |
| `ModuleNotFoundError` | Activate virtual environment |
| `FileNotFoundError` | Check data files are present |
| `Address already in use` | Change port or kill existing process |
| `MemoryError` | Use smaller dataset or more RAM |
| `ImportError` | Reinstall packages |

## Performance Tips

1. **Use virtual environment** for clean dependency management
2. **Sample data** for development (use full dataset for production)
3. **Monitor memory usage** with large datasets
4. **Use caching** for frequently accessed data
5. **Optimize data loading** by loading once at startup 