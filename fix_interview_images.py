import json
import base64
from pathlib import Path

def image_to_base64(image_path):
    """Convert image to base64 string"""
    with open(image_path, 'rb') as img_file:
        return base64.b64encode(img_file.read()).decode()

# Load news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert images to base64
eric_stream_b64 = image_to_base64('assets/interview_erik/eric_stream.png')
erik_char_b64 = image_to_base64('assets/interview_erik/erik_char.jpg')
gmerik_b64 = image_to_base64('assets/interview_erik/gmerik.png')

# Get the interview content
content = data[0]['modalContent']['content']

# Replace image paths with base64 data URIs
content = content.replace(
    "src='assets/interview_erik/eric_stream.png'",
    f"src='data:image/png;base64,{eric_stream_b64}'"
)

content = content.replace(
    "src='assets/interview_erik/erik_char.jpg'",
    f"src='data:image/jpeg;base64,{erik_char_b64}'"
)

content = content.replace(
    "src='assets/interview_erik/gmerik.png'",
    f"src='data:image/png;base64,{gmerik_b64}'"
)

# Update the content
data[0]['modalContent']['content'] = content

# Save back to JSON
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Done! Images converted to base64 and embedded in JSON.")
