import os
from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io
import base64

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please check your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_description(images, measurements, style):
    # Prepare images for Gemini
    pil_images = []
    for image_path in images:
        img = Image.open(image_path)
        # Resize image if too large
        if img.size[0] > 800 or img.size[1] > 800:
            img.thumbnail((800, 800))
        pil_images.append(img)

    # Create prompt for Gemini
    prompt = f"""Generate a Vinted clothing description based on the following information:
    - Measurements: {measurements}
    - Style: {style}

    Please provide a detailed description that includes:
    1. Item type and style
    2. Material and condition
    3. Measurements
    4. Key features and details
    5. Any notable wear or imperfections

    Format the description in a clear, professional manner suitable for Vinted listings."""

    try:
        # Generate content using Gemini
        response = model.generate_content([prompt, *pil_images])
        return response.text
    except Exception as e:
        return f"Error generating description: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if 'images' not in request.files:
        return jsonify({'error': 'No images uploaded'}), 400
    
    files = request.files.getlist('images')
    measurements = request.form.get('measurements', '')
    style = request.form.get('style', 'professional')

    if not files or files[0].filename == '':
        return jsonify({'error': 'No selected files'}), 400

    valid_files = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            valid_files.append(filepath)

    if not valid_files:
        return jsonify({'error': 'No valid files uploaded'}), 400

    description = generate_description(valid_files, measurements, style)

    # Clean up uploaded files
    for filepath in valid_files:
        try:
            os.remove(filepath)
        except:
            pass

    return jsonify({'description': description})

if __name__ == '__main__':
    app.run(debug=True) 