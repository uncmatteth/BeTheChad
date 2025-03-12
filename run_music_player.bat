@echo off
echo Starting Chad Battles with Music Player...
echo.
set FLASK_APP=app.py
set FLASK_ENV=development
python -m flask run
echo.
echo Server has been stopped.
pause 