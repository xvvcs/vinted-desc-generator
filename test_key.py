import os
import sys
import google.generativeai as genai
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# Check original environment before loading .env
print("Environment variables BEFORE loading .env file:")
original_api_key = os.environ.get('GOOGLE_API_KEY')
print(f"GOOGLE_API_KEY (before .env): {original_api_key[:5]}..." if original_api_key else "GOOGLE_API_KEY not set in environment")

# Find .env file and show its path without verbose flag
print("\nSearching for .env file...")
dotenv_path = find_dotenv()
print(f"Found .env file at: {dotenv_path}")

# Show content of .env file
if os.path.exists(dotenv_path):
    print("\nContent of .env file:")
    with open(dotenv_path, 'r') as f:
        env_content = f.read()
        print(env_content)
else:
    print("\nNo .env file found!")

# Check all .env files in the project directory
print("\nSearching for all .env files in project directory:")
project_dir = Path('/Users/maciej/vinDesc')
env_files = list(project_dir.rglob('*.env')) + list(project_dir.glob('.env'))
for env_file in env_files:
    print(f"\nFound file: {env_file}")
    try:
        with open(env_file, 'r') as f:
            print(f"Content:\n{f.read()}")
    except Exception as e:
        print(f"Error reading file: {e}")

# Load from .env file
print("\nLoading from .env file...")
load_dotenv(dotenv_path, override=True)  # Force override existing env vars

# Get and print API key after loading .env
api_key = os.getenv('GOOGLE_API_KEY')
print(f"\nGOOGLE_API_KEY (after loading .env): {api_key[:5]}..." if api_key else "API Key not found!")

# Check if the key was actually changed
if original_api_key and api_key and original_api_key == api_key:
    print("WARNING: .env file did not override existing environment variable!")

if api_key:
    try:
        # Configure the API
        print("\nConfiguring Gemini API...")
        genai.configure(api_key=api_key)
        
        # Simple test
        print("Testing with simple query...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello in one word")
        print(f"Response: {response.text}")
        print("\nAPI KEY WORKS! ✅")
    except Exception as e:
        print(f"\nAPI TEST FAILED: {str(e)} ❌")