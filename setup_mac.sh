#!/bin/bash
# Vintly Installation Script for Mac/Unix

echo ""
echo "========================================"
echo "        Vintly Setup Assistant"
echo "========================================"
echo ""

# Check if Python 3.12.9 is installed
echo "Checking for Python 3.12.9..."
if python3 -c "import sys; exit(0 if sys.version_info[:3] == (3, 12, 9) else 1)" &> /dev/null; then
    echo "[SUCCESS] Python 3.12.9 is already installed."
    echo ""
else
    echo "[INFO] Python 3.12.9 is not installed."
    echo ""
    
    # Check if Homebrew is installed
    if command -v brew &> /dev/null; then
        echo "Homebrew is installed. Attempting to install Python 3.12.9..."
        echo "This may take a few minutes..."
        
        # Install Python 3.12.9 via Homebrew
        brew install python@3.12
        
        if [ $? -ne 0 ]; then
            echo "[ERROR] Failed to install Python via Homebrew."
            echo "Please install Python 3.12.9 manually from https://www.python.org/downloads/"
            echo ""
            exit 1
        fi
        
        # Create a symlink to ensure we use Python 3.12
        echo "Setting up Python 3.12 as default python3..."
        brew link --force python@3.12
        
        echo "[SUCCESS] Python 3.12 has been installed via Homebrew."
        echo ""
    else
        # Offer to install Homebrew
        echo "Homebrew is not installed. Would you like to install it? (recommended)"
        read -p "Install Homebrew? (y/n): " INSTALL_HOMEBREW
        
        if [[ $INSTALL_HOMEBREW == "y" || $INSTALL_HOMEBREW == "Y" ]]; then
            echo "Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            
            if [ $? -ne 0 ]; then
                echo "[ERROR] Failed to install Homebrew."
                echo "Please install Python 3.12.9 manually from https://www.python.org/downloads/"
                echo ""
                exit 1
            fi
            
            echo "[SUCCESS] Homebrew installed. Now installing Python 3.12.9..."
            
            # Add Homebrew to PATH for the current session
            eval "$(/opt/homebrew/bin/brew shellenv)" || eval "$(/usr/local/bin/brew shellenv)"
            
            # Install Python 3.12.9
            brew install python@3.12
            
            if [ $? -ne 0 ]; then
                echo "[ERROR] Failed to install Python via Homebrew."
                echo "Please install Python 3.12.9 manually from https://www.python.org/downloads/"
                echo ""
                exit 1
            fi
            
            # Create a symlink to ensure we use Python 3.12
            brew link --force python@3.12
            
            echo "[SUCCESS] Python 3.12 has been installed."
            echo ""
        else
            echo "Please install Python 3.12.9 manually from https://www.python.org/downloads/"
            echo "Then run this setup script again."
            echo ""
            exit 1
        fi
    fi
fi

# Create virtual environment (optional)
read -p "Would you like to create a virtual environment? (y/n): " CREATE_VENV
if [[ $CREATE_VENV == "y" || $CREATE_VENV == "Y" ]]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment."
        echo "Continuing without virtual environment..."
        ACTIVATE_CMD="python3"
    else
        echo "[SUCCESS] Virtual environment created."
        echo "Activating virtual environment..."
        source .venv/bin/activate
        ACTIVATE_CMD="source .venv/bin/activate && python3"
    fi
else
    ACTIVATE_CMD="python3"
fi

# Install dependencies
echo "Installing required packages..."
pip3 install flask==3.1.0 Werkzeug==3.1.3 python-dotenv==1.1.0 google-generativeai==0.8.4 Pillow==11.1.0 flask-sqlalchemy==3.1.1 flask-migrate==4.0.5

if [ $? -ne 0 ]; then
    echo "[WARNING] Some packages may not have installed correctly."
    echo "We'll continue anyway, but you might encounter issues."
    echo ""
else
    echo "[SUCCESS] Packages installed."
    echo ""
fi

# Prompt for API key
echo "========================================"
echo "Now let's set up your Google API key:"
echo "========================================"
echo ""
echo "You can get an API key from: https://makersuite.google.com/app/apikey"
echo ""
read -p "Enter your Google API key: " API_KEY

# Validate input
if [ -z "$API_KEY" ]; then
    echo "[ERROR] API key cannot be empty."
    echo "Please run the setup again and provide a valid key."
    exit 1
fi

# Create .env file
echo "Creating .env file with your API key..."
echo "GOOGLE_API_KEY=$API_KEY" > .env
echo ""
echo "[SUCCESS] API key saved to .env file."
echo ""

# Offer to start the application
echo "========================================"
echo "        Installation Complete!"
echo "========================================"
echo ""
echo "Vintly has been successfully set up on your computer."
echo ""
read -p "Would you like to start Vintly now? (y/n): " START_APP

if [[ $START_APP == "y" || $START_APP == "Y" ]]; then
    echo ""
    echo "Starting Vintly..."
    
    if [[ $CREATE_VENV == "y" || $CREATE_VENV == "Y" ]]; then
        echo "To run Vintly in the future, use the run-vintly.sh script:"
        echo "./run-vintly.sh"
        source .venv/bin/activate && python3 app.py &
    else
        echo "To run Vintly in the future, use the run-vintly.sh script:"
        echo "./run-vintly.sh"
        python3 app.py &
    fi
    
    # Wait for server to start and open browser
    sleep 3
    open http://localhost:5001
else
    echo ""
    echo "To start Vintly later, use the run-vintly.sh script:"
    echo "./run-vintly.sh"
    echo "This will start the application and open it in your browser."
fi

echo ""
echo "Thank you for installing Vintly!"
echo ""

# Make run script executable
chmod +x run-vintly.sh