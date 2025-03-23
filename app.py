import os
import json
import uuid
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
app.config['TEMPLATES_FILE'] = 'templates.json'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize Gemini API
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please check your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

def load_templates():
    if os.path.exists(app.config['TEMPLATES_FILE']):
        with open(app.config['TEMPLATES_FILE'], 'r', encoding='utf-8') as f:
            templates = json.load(f)
            # Convert Unicode escape sequences to actual emojis
            for template in templates:
                if 'description' in template:
                    template['description'] = template['description'].encode('utf-8').decode('unicode-escape')
            return templates
    return []

def save_templates(templates):
    with open(app.config['TEMPLATES_FILE'], 'w', encoding='utf-8') as f:
        json.dump(templates, f, indent=2, ensure_ascii=False)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def generate_description(images, measurements, style, category='clothing', languages=['en']):
    # Load relevant templates
    templates = load_templates()
    category_templates = [t for t in templates if t['category'] == category]
    
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
    - Category: {category}
    - Languages: {', '.join(languages)}

    Here are some example descriptions to follow the style and format of:
    {json.dumps([t['description'] for t in category_templates], indent=2, ensure_ascii=False)}

    Please provide a detailed description that includes:
    1. Item type and style
    2. Material and condition
    3. Measurements
    4. Key features and details
    5. Any notable wear or imperfections

    Generate the description in the following languages: {', '.join(languages)}
    
    Important formatting instructions:
    1. For each language, use the format: "[Language]: [Description]"
    2. Follow the exact style of the example templates, including:
       - Using the same bilingual/multilingual format if present in templates
       - Maintaining consistent terminology across languages
       - Following the same structure for measurements and details
       - Using appropriate emojis in the same style as the templates (e.g., for measurements, condition, etc.)
    3. If the templates show items with multiple language versions (e.g., "T-shirt: blue / Koszulka: niebieska"), 
       use the same parallel format in your response
    4. Keep the same level of detail and style across all language versions
    5. Ensure measurements and technical details are consistent across languages
    6. Use emojis naturally and appropriately, similar to the example templates
    7. Do not use Unicode escape sequences or raw emoji codes - use actual emoji characters

    Hashtag Instructions (VERY IMPORTANT):
    1. Include a comprehensive set of hashtags at the end of the description
    2. Include hashtags in both English and the other selected languages
    3. Use multiple variations of important terms (e.g., #tshirt #tee #t-shirt)
    4. Include hashtags for:
       - Brand name (multiple variations)
       - Item type (multiple variations)
       - Style/design
       - Size
       - Color
       - Condition
       - Category
       - Special features
    5. Format hashtags without spaces or special characters
    6. Use lowercase for all hashtags
    7. Include compound hashtags (e.g., #longsleeve, #sportswear)
    8. Repeat important hashtags 2-3 times for better visibility
    9. Place hashtags at the end of the description, separated from the main text by a line break

    Format the description in a clear, professional manner suitable for Vinted listings, following the style and structure of the example descriptions above."""

    try:
        # Generate content using Gemini
        response = model.generate_content([prompt, *pil_images])
        return response.text
    except Exception as e:
        return f"Error generating description: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/templates')
def templates_page():
    return render_template('templates.html')

@app.route('/api/templates', methods=['GET'])
def get_templates():
    return jsonify(load_templates())

@app.route('/api/templates', methods=['POST'])
def add_template():
    template = request.json
    template['id'] = str(uuid.uuid4())
    
    templates = load_templates()
    templates.append(template)
    save_templates(templates)
    
    return jsonify(template), 201

@app.route('/api/templates/<template_id>', methods=['DELETE'])
def delete_template(template_id):
    templates = load_templates()
    templates = [t for t in templates if t['id'] != template_id]
    save_templates(templates)
    return '', 204

@app.route('/generate', methods=['POST'])
def generate():
    if 'images' not in request.files:
        return jsonify({'error': 'No images uploaded'}), 400
    
    files = request.files.getlist('images')
    measurements = request.form.get('measurements', '')
    style = request.form.get('style', 'professional')
    category = request.form.get('category', 'clothing')
    languages = json.loads(request.form.get('languages', '["en"]'))

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

    description = generate_description(valid_files, measurements, style, category, languages)

    # Clean up uploaded files
    for filepath in valid_files:
        try:
            os.remove(filepath)
        except:
            pass

    return jsonify({'description': description})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True) 