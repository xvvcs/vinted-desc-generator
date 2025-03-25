<div align="center">

# Vintly

A powerful tool that generates professional, multilingual descriptions for Vinted listings using AI. Upload your product images and get detailed, SEO-optimized descriptions in multiple languages.

![Vintly Logo](img/vintly-logo.png)

<div align="center">
  
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.2-lightgrey.svg)](https://flask.palletsprojects.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-3.1.1-red.svg)](https://www.sqlalchemy.org/)
[![Google Gemini AI](https://img.shields.io/badge/Gemini_AI-0.3.2-green.svg)](https://ai.google.dev/)
[![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple.svg)](https://getbootstrap.com/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6-yellow.svg)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)

</div>
</div>

## Features

- 🤖 AI-powered description generation
- 🌍 Multilingual support (English, Polish, Danish)
- 🖼️ Drag-and-drop image upload
- 🎨 Multiple description styles (Professional, Casual, Detailed)
- 📏 Custom measurements support
- 🏷️ Category-specific descriptions
- 🌓 Dark/Light mode
- 💾 Save your preferences
- 📋 Copy to clipboard functionality

## Video Demo

<div align="center">
  <img src="img/showcase.gif" alt="Vintly Demo">
</div>

## Installation

### Prerequisites

Before you start, make sure you have these installed on your computer:

1. **Python 3.8 or higher**

   - Download from [Python's official website](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"
   - To verify installation, open Terminal (Mac/Linux) or Command Prompt (Windows) and type:
     ```bash
     python --version
     ```
   - You should see something like "Python 3.8.x"

2. **pip (Python package installer)**

   - Usually comes with Python installation
   - To verify installation, type:
     ```bash
     pip --version
     ```

3. **Google API key for Gemini AI**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy your API key (you'll need it later)

### Step-by-Step Installation

1. **Download the Program**

   - Click the green "Code" button on this page
   - Select "Download ZIP"
   - Extract the ZIP file to a folder on your computer
   - Open Terminal (Mac/Linux) or Command Prompt (Windows)
   - Navigate to the extracted folder:
     ```bash
     cd path/to/vinted-desc-generator
     ```
   - Replace "path/to" with the actual path where you extracted the files

2. **Set Up Python Environment**

   - Create a virtual environment (this keeps the program's files separate from other Python programs):
     ```bash
     python -m venv .venv
     ```
   - Activate the virtual environment:
     - On Mac/Linux:
       ```bash
       source .venv/bin/activate
       ```
     - On Windows:
       ```bash
       .venv\Scripts\activate
       ```
   - You'll know it's activated when you see `(.venv)` at the start of your command line

3. **Install Required Packages**

   - With the virtual environment activated, run:
     ```bash
     pip install -r requirements.txt
     ```
   - Wait for all packages to install (this might take a few minutes)

4. **Set Up API Key**

   - In the program folder, create a new file named `.env`
   - Open it with any text editor (like Notepad or TextEdit)
   - Add this line, replacing `your_api_key_here` with your actual Google API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   - Save the file
   - ⚠️ Important: Never share your API key with anyone!

5. **Run the Program**
   - Make sure your virtual environment is activated (you should see `(.venv)` in your terminal)
   - Run the program:
     ```bash
     python app.py
     ```
   - You should see a message that the server is running
   - Open your web browser and go to: `http://localhost:5000`

### Troubleshooting

If you encounter any issues:

1. **"Python is not recognized" error**

   - Make sure Python is added to your PATH during installation
   - Try reinstalling Python and check "Add Python to PATH"

2. **"pip is not recognized" error**

   - Try using `python -m pip` instead of just `pip`

3. **"Module not found" errors**

   - Make sure you're in the virtual environment (you should see `(.venv)`)
   - Try running `pip install -r requirements.txt` again

4. **Program won't start**
   - Check if you're in the correct directory
   - Make sure the `.env` file is created with your API key
   - Try closing and reopening your terminal

Need help? Feel free to open an issue on GitHub or contact the developer!

## Usage

1. **Upload Images**

   - Drag and drop images or click to select files (currently supporting single image ONLY)
   - Supported formats: PNG, JPG, JPEG
   - Maximum file size: 16MB
   - Preview and remove images before generating description

2. **Configure Settings**

   - Click the settings icon (⚙️) to open settings panel
   - Set your preferred languages and description style
   - Save your preferences for future use

3. **Add Details**

   - Enter product measurements
   - Select category (Clothing, Shoes, Accessories)
   - Choose description style if different from preferred

4. **Generate Description**

   - Click "Generate Description"
   - Wait for AI to process your images
   - Copy the generated description to clipboard

5. **Manage Templates**

   - Access the templates page to manage your description templates
   - Add, edit, or delete custom templates
   - Templates are saved automatically

6. **Theme Toggle**
   - Use the moon/sun icon to switch between light and dark modes

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request or send me a dm.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Google Gemini AI for providing the AI capabilities
- Flask for the web framework
- Bootstrap for the UI components
- Font Awesome for icons
