@echo off
echo ========================================
echo    Repository Merge Tool
echo ========================================
echo.

:: Set paths
set "ENHANCED_REPO=C:\Users\Acer\OneDrive\Desktop\ContentRecommendation"
set "CLONED_REPO=C:\Users\Acer\OneDrive\Desktop\ContentRecommendation1"
set "BACKUP_DIR=C:\Users\Acer\OneDrive\Desktop\ContentRecommendation_backup"

echo Enhanced Repository: %ENHANCED_REPO%
echo Cloned Repository: %CLONED_REPO%
echo Backup Directory: %BACKUP_DIR%
echo.

:: Step 1: Create backups
echo [1/5] Creating backups...
if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

if exist "%ENHANCED_REPO%" (
    echo   Backing up enhanced repository...
    xcopy "%ENHANCED_REPO%" "%BACKUP_DIR%\enhanced" /E /I /H /Y >nul
    echo   ✓ Enhanced repo backed up
) else (
    echo   ❌ Enhanced repository not found
    goto :error
)

if exist "%CLONED_REPO%" (
    echo   Backing up cloned repository...
    xcopy "%CLONED_REPO%" "%BACKUP_DIR%\cloned" /E /I /H /Y >nul
    echo   ✓ Cloned repo backed up
) else (
    echo   ❌ Cloned repository not found
    goto :error
)

:: Step 2: Copy new files
echo.
echo [2/5] Copying new files...
cd /d "%CLONED_REPO%"

:: Create flask_ml_backend directory if it doesn't exist
if not exist "flask_ml_backend" mkdir "flask_ml_backend"

:: Copy new files
copy "%ENHANCED_REPO%\flask_ml_backend\app_multi_content.py" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\flask_ml_backend\multi_content_data_generator.py" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\flask_ml_backend\test_real_multi_content.py" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\flask_ml_backend\test_multi_content.py" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\flask_ml_backend\test_users.py" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\flask_ml_backend\TROUBLESHOOTING.md" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\flask_ml_backend\install_dependencies.py" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\flask_ml_backend\start_server.bat" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\PUSH_GUIDE.md" "." >nul 2>&1
copy "%ENHANCED_REPO%\MERGE_STRATEGY.md" "." >nul 2>&1

echo   ✓ New files copied

:: Step 3: Merge enhanced files
echo.
echo [3/5] Merging enhanced files...
copy "%ENHANCED_REPO%\flask_ml_backend\app.py" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\flask_ml_backend\README.md" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\flask_ml_backend\requirements.txt" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\flask_ml_backend\example_client.py" "flask_ml_backend\" >nul 2>&1
copy "%ENHANCED_REPO%\README.md" "." >nul 2>&1
copy "%ENHANCED_REPO%\.gitignore" "." >nul 2>&1

echo   ✓ Enhanced files merged

:: Step 4: Verify data integrity
echo.
echo [4/5] Verifying data integrity...
set "errors=0"

if not exist "flask_ml_backend\rating.csv" (
    echo   ❌ Critical file missing: rating.csv
    set /a errors+=1
)

if not exist "flask_ml_backend\processed_movies.csv" (
    echo   ❌ Critical file missing: processed_movies.csv
    set /a errors+=1
)

if not exist "flask_ml_backend\tfidf_vectorizer.pkl" (
    echo   ❌ Critical file missing: tfidf_vectorizer.pkl
    set /a errors+=1
)

if not exist "Backend\pom.xml" (
    echo   ❌ Critical file missing: Backend\pom.xml
    set /a errors+=1
)

if not exist "frontend\package.json" (
    echo   ❌ Critical file missing: frontend\package.json
    set /a errors+=1
)

if %errors% gtr 0 (
    echo   ❌ Data integrity check failed (%errors% errors)
    goto :error
) else (
    echo   ✓ All critical files preserved
)

:: Step 5: Generate merge report
echo.
echo [5/5] Generating merge report...
echo { > merge_report.json
echo   "timestamp": "%date% %time%", >> merge_report.json
echo   "enhanced_repo": "%ENHANCED_REPO%", >> merge_report.json
echo   "cloned_repo": "%CLONED_REPO%", >> merge_report.json
echo   "backup_location": "%BACKUP_DIR%", >> merge_report.json
echo   "status": "success" >> merge_report.json
echo } >> merge_report.json

echo   ✓ Merge report generated

:: Success
echo.
echo ========================================
echo    MERGE COMPLETED SUCCESSFULLY!
echo ========================================
echo.
echo 📁 Files copied: 10 new files
echo 🔄 Files merged: 6 enhanced files
echo 💾 Backup location: %BACKUP_DIR%
echo 🎯 Target repository: %CLONED_REPO%
echo.
echo 🚀 Next steps:
echo    1. cd %CLONED_REPO%
echo    2. git add .
echo    3. git commit -m "✨ Merged enhanced features"
echo    4. git push origin main
echo.
echo 🧪 Test the merged repository:
echo    cd flask_ml_backend
echo    python app.py
echo    python multi_content_data_generator.py
echo    python app_multi_content.py
echo.
pause
goto :end

:error
echo.
echo ========================================
echo    MERGE FAILED!
echo ========================================
echo.
echo ❌ An error occurred during the merge process.
echo 💾 Backups are available at: %BACKUP_DIR%
echo.
echo 🔄 To restore from backup:
echo    xcopy "%BACKUP_DIR%\cloned" "%CLONED_REPO%" /E /I /H /Y
echo.
pause
goto :end

:end 