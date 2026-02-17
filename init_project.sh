#!/bin/bash

echo "==========================================="
echo "SMC Road Damage Management Platform Setup"
echo "==========================================="

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if [[ $(printf '%s\n' "3.11" "$PYTHON_VERSION" | sort -V | head -n1) != "3.11" ]]; then
    echo "Python version is lower than 3.11. Current version: $PYTHON_VERSION"
    echo "Please upgrade to Python 3.11 or higher."
    exit 1
fi

echo "✓ Python version check passed ($PYTHON_VERSION)"

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
echo "✓ Virtual environment created"

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip
echo "✓ Pip upgraded"

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Check if PostgreSQL is installed and running
if command -v pg_config &> /dev/null; then
    echo "✓ PostgreSQL client found"
else
    echo "⚠ PostgreSQL client not found, but continuing anyway"
fi

# Create media directory
echo "Creating media directory..."
mkdir -p media
echo "✓ Media directory created"

# Create staticfiles directory
echo "Creating staticfiles directory..."
mkdir -p staticfiles
echo "✓ Staticfiles directory created"

# Copy environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "Copying .env.example to .env..."
    cp .env.example .env
    echo "✓ Environment file copied"
    echo "⚠ IMPORTANT: Please edit .env file with your database credentials"
fi

echo ""
echo "==========================================="
echo "Initial Setup Complete!"
echo "==========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file with your database settings"
echo "2. Start PostgreSQL service if not running"
echo "3. Run: python manage.py migrate"
echo "4. Run: python manage.py load_initial_data"
echo "5. Run: python manage.py createsuperuser"
echo "6. Run: python manage.py runserver"
echo ""
echo "For Docker setup: docker-compose up --build"
echo ""
echo "Project is ready for development!"
echo "==========================================="