from flask import Flask, render_template, request, send_from_directory
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'static'


API_KEY = "AIzaSyA5as0MCGp3YnKju0R9s2T25DYfQy9a1sQ"
client = genai.Client(api_key=API_KEY)

# Asegura carpetas necesarias
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    result_image = None
    if request.method == 'POST':
        prompt = request.form['prompt']
        image_file = request.files['image']
        
        if image_file and prompt:
            img_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(img_path)

            image = Image.open(img_path)

            response = client.models.generate_content(
                model='gemini-2.0-flash-exp-image-generation',
                contents=[prompt, image],
                config=types.GenerateContentConfig(response_modalities=['Text', 'Image'])
            )

            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    result_img = Image.open(BytesIO(part.inline_data.data))
                    result_path = os.path.join(app.config['RESULT_FOLDER'], 'result.png')
                    result_img.save(result_path)
                    result_image = 'static/result.png'

    return render_template('index.html', result_image=result_image)

if __name__ == '__main__':
    app.run(debug=True)
