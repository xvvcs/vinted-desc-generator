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

## ⚡ Quick Start Guide (For Beginners)

1. **Download & Install**: Download the ZIP, extract it, install Python 3.8+
2. **Set Up**: Create `.env` file with your Google API key
3. **Run**: Open terminal in the folder and run `python app.py`
4. **Use**: Open your web browser and go to `http://localhost:5001`

Need more details? Follow the complete installation steps below.

## 💻 Installation

### Prerequisites

Before you start, make sure you have these installed on your computer:

1. **Python 3.8 or higher**

   Python is the programming language needed to run Vintly.

   - **Windows**:

     - Download from [Python's official website](https://www.python.org/downloads/)
     - **IMPORTANT**: During installation, check the box that says "Add Python to PATH"
     - To verify installation: Open Command Prompt (search for "cmd" in Start menu) and type:
       ```
       python --version
       ```

   - **Mac**:
     - Most Macs come with Python installed
     - To verify installation: Open Terminal (find in Applications > Utilities) and type:
       ```
       python3 --version
       ```
     - If not installed, download from [Python's official website](https://www.python.org/downloads/)

2. **Google API key for Gemini AI**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy your API key (you'll need it in Step 4)

### Step-by-Step Installation with Pictures

1. **Download the Program**

   - Download the ZIP file from the download link
   - Extract/unzip the file to a folder on your computer
   - Remember where you saved it! (Example: Desktop/vintly)

2. **Open Terminal/Command Prompt**

   - **Windows**:

     - Press Windows key + R
     - Type "cmd" and press Enter
     - Navigate to your folder by typing (replace with your actual path):
       ```
       cd Desktop\vintly
       ```

   - **Mac**:
     - Open Terminal (Applications > Utilities > Terminal)
     - Navigate to your folder by typing (replace with your actual path):
       ```
       cd Desktop/vintly
       ```

3. **Set Up Python Environment**

   A virtual environment is like a separate space for Vintly that won't affect other programs.

   - Create a virtual environment:

     **Windows**:

     ```
     python -m venv .venv
     ```

     **Mac**:

     ```
     python3 -m venv .venv
     ```

   - <i>Make sure you make running the shell scripts available</i>

     **Windows**:

     ```bash
     Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
     ```

   - Activate the virtual environment:

     **Windows**:

     ```
     .venv\Scripts\activate
     ```

     **Mac**:

     ```
     source .venv/bin/activate
     ```

   You'll know it's working when you see `(.venv)` at the beginning of your command line.

4. **Install Required Packages**

   - With the virtual environment activated, run:
     ```
     pip install -r requirements.txt
     ```
   - This may take a few minutes as it downloads all necessary components

5. **Set Up API Key**

   - Create a new text file in the program folder
   - Name it exactly `.env` (including the period at the beginning)
   - Open it with Notepad (Windows) or TextEdit (Mac)
   - Type ONLY this line, replacing with your actual API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   - Save the file
   - **WARNING**: The file must contain ONLY this line with no comments or other text!

6. **Run the Program**

   - Make sure your virtual environment is active (you'll see `(.venv)` in your terminal)
   - Run:

     **Windows**:

     ```
     python app.py
     ```

     **Mac**:

     ```
     python3 app.py
     ```

   - You should see a message that says the server is running
   - Open your web browser and go to: `http://localhost:5001`

### ❓ Troubleshooting

If you encounter any issues:

1. **"Python is not recognized" error**

   - Windows: Reinstall Python and make sure to check "Add Python to PATH"
   - Mac: Try using `python3` instead of `python`

2. **API key not working**

   - Make sure your `.env` file contains ONLY the API key line with no comments
   - Ensure there are no spaces around the equals sign
   - Check that you've copied the entire key correctly
   - Try generating a new API key at Google AI Studio

3. **"Module not found" errors**

   - Make sure you see `(.venv)` in your terminal
   - Try running `pip install -r requirements.txt` again

4. **Can't connect to the application**

   - Make sure the terminal shows the server is running
   - Try going to `http://localhost:5001` in your browser
   - Check if any antivirus or firewall is blocking the connection

5. **Description generation fails**
   - Your API key might have expired - generate a new one
   - Make sure you have internet connection
   - Try with a smaller image file

## 🖱️ How to Use Vintly

1. **Upload Images**

   - Drag and drop images or click to select files
   - Supported formats: PNG, JPG, JPEG
   - Maximum file size: 16MB

2. **Add Product Details**

   - Enter measurements (e.g., chest 40cm, length 70cm)
   - Select category: Clothing, Shoes, or Accessories
   - Choose a description style

3. **Generate Description**

   - Click the "Generate Description" button
   - The AI will create a description based on your image and information
   - Copy the text with the "Copy to Clipboard" button

4. **Customize Your Experience**
   - Use the Settings button (⚙️) to set preferred languages
   - Switch between Light/Dark mode with the moon/sun icon
   - Create templates on the Templates page for consistent descriptions

Need help? Feel free to contact me in dm or create an issue.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

xvvcs
