@echo off
echo ===================================
echo Chad Battles Music Player Verification
echo ===================================
echo.

REM Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if the verification script exists
if not exist verify_music_player.py (
    echo Error: verify_music_player.py not found
    echo Make sure you run this batch file from the project root directory
    pause
    exit /b 1
)

echo Choose environment to verify:
echo 1. Local development server (http://localhost:5000)
echo 2. Production server (https://chadbattles.fun)
echo.

set /p env_choice="Enter your choice (1 or 2): "

if "%env_choice%"=="1" (
    echo.
    echo Verifying music player on local development server...
    echo.
    python verify_music_player.py --local
) else if "%env_choice%"=="2" (
    echo.
    echo Verifying music player on production server...
    echo.
    python verify_music_player.py --prod
) else (
    echo.
    echo Invalid choice. Please enter 1 or 2.
    pause
    exit /b 1
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Verification failed! Check the logs for details.
) else (
    echo.
    echo Verification completed successfully!
    echo Results have been saved to MUSIC_PLAYER_VERIFICATION.md
)

echo.
echo Check the log file for detailed results
echo.

pause 