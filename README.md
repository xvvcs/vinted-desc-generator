# Vinted Description Generator

A Python application that automatically generates clothing descriptions for Vinted listings based on uploaded images and measurements using Google's Gemini AI.

## Features

- Upload multiple clothing images
- Input clothing measurements
- Generate AI-powered descriptions using Google's Gemini Vision
- Customizable description styles
- Simple web interface

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```
4. Run the application:
   ```bash
   python app.py
   ```

## Usage

1. Open your browser and navigate to `http://localhost:5000`
2. Upload one or more clothing images
3. Enter the clothing measurements
4. Select your preferred description style
5. Generate the description

## Project Structure

- `app.py`: Main application file
- `templates/`: HTML templates for the web interface
- `static/`: CSS and JavaScript files
- `config/`: Configuration files for description styles
- `utils/`: Utility functions for image processing and description generation
