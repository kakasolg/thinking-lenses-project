@echo off
echo Starting 지혜의 렌즈 - I Ching Divination System...
echo.

REM Check if virtual environment is activated
if not defined VIRTUAL_ENV (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
)

echo Starting Streamlit application...
echo.
echo Open your browser and go to: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.

streamlit run app_streamlit.py --server.address localhost --server.port 8501

pause
