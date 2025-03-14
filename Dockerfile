FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements_deployment.txt .
RUN pip install --no-cache-dir -r requirements_deployment.txt

# Copy application code
COPY . .

# Add debug output before running the setup script
RUN ls -la && echo "Checking for setup_deployment_db.py:" && ls -la setup_deployment_db.py

# Run the setup script with debug mode
RUN python -u setup_deployment_db.py

# Create non-root user
RUN useradd -m chadbattles && \
    chown -R chadbattles:chadbattles /app

# Switch to non-root user
USER chadbattles

# Create directories for static files
RUN mkdir -p app/static/img/{chad,waifu,item,elixir}

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app \
    ENABLE_BLOCKCHAIN=false \
    ENABLE_TWITTER_BOT=false

# Expose port
EXPOSE 5000

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"] 