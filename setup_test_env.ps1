# Setup Test Environment Script
Write-Host "Setting up test environment..."

# Set execution policy for this process
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# Remove existing venv if it exists
if (Test-Path ".venv") {
    Write-Host "Removing existing virtual environment..."
    Remove-Item -Recurse -Force ".venv"
}

# Create new virtual environment
Write-Host "Creating new virtual environment..."
python -m venv .venv

# Activate virtual environment
Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

# Install requirements
Write-Host "Installing requirements..."
python -m pip install --upgrade pip
pip install -r requirements.txt

# Install test dependencies if not in requirements.txt
Write-Host "Installing test dependencies..."
pip install pytest pytest-flask selenium pytest-cov

Write-Host "Setup complete! Virtual environment is activated and dependencies are installed." 