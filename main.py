API_KEY = "AIzaSyA5as0MCGp3YnKju0R9s2T25DYfQy9a1sQ"

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import base64

client = genai.Client(api_key=API_KEY)

image = Image.open("test2.png")
prompt = ("Cambia el color de los dientes de blanco a negro")

response = client.models.generate_content(
    model='gemini-2.0-flash-exp-image-generation',
    contents=[prompt, image],
    config=types.GenerateContentConfig(response_modalities=['Text', 'Image']))

print(response)

for part in response.candidates[0].content.parts:
  if part.text is not None:
    print(part.text)
  elif part.inline_data is not None:
    image = Image.open(BytesIO((part.inline_data.data)))
    image.show()
