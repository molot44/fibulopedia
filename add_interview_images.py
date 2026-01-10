import json
import base64
from pathlib import Path

# Load current news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

content = data[0]['modalContent']['content']

# Load images and convert to base64
images = {
    'eric_stream': Path("assets/interview_erik/eric_stream.png"),
    'erik_char': Path("assets/interview_erik/erik_char.jpg"),
    'gmerik': Path("assets/interview_erik/gmerik.png")
}

image_data = {}
for key, path in images.items():
    if path.exists():
        with open(path, "rb") as f:
            ext = path.suffix[1:]  # jpg or png
            image_data[key] = f"data:image/{ext};base64,{base64.b64encode(f.read()).decode()}"
    else:
        print(f"Warning: {path} not found")

# Image template with golden border
def make_image(src, alt, caption=""):
    caption_html = f"<p style='text-align: center; color: #d4af37; font-style: italic; margin-top: 0.5rem; font-size: 0.9rem;'>{caption}</p>" if caption else ""
    return f"""
<div style='text-align: center; margin: 2rem 0;'>
    <img src='{src}' alt='{alt}' style='max-width: 60%; border: 3px solid #d4af37; border-radius: 8px; box-shadow: 0 4px 8px rgba(212, 175, 55, 0.3);'/>
    {caption_html}
</div>
"""

# 1. eric_stream.png - after the first answer about who he is
content = content.replace(
    "After that, I was hooked and would play every day at the library.</p>",
    "After that, I was hooked and would play every day at the library.</p>" +
    make_image(image_data['eric_stream'], "GM Erik", "Eric, the creator of Project Fibula")
)

# 2. erik_char.jpg - after talking about his history as a Tibia player
content = content.replace(
    "That's why I felt Project Fibula would be fun as a progression server similar to WoW — it gives us the chance to see what parts felt good and what parts didn't, without needing to play six separate OT servers.</p>",
    "That's why I felt Project Fibula would be fun as a progression server similar to WoW — it gives us the chance to see what parts felt good and what parts didn't, without needing to play six separate OT servers.</p>" +
    make_image(image_data['erik_char'], "Erik's character in Tibia", "Erik's character from the old days of Tibia")
)

# 3. gmerik.png - after talking about whether he plays a character himself
content = content.replace(
    "People were very friendly to me when I was streaming on launch day, but they haven't been as nice to my secret level 8!</p>",
    "People were very friendly to me when I was streaming on launch day, but they haven't been as nice to my secret level 8!</p>" +
    make_image(image_data['gmerik'], "GM Erik in Project Fibula", "GM Erik's character on Project Fibula")
)

# Update content
data[0]['modalContent']['content'] = content

# Save back
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✓ Dodano 3 obrazki do wywiadu ze złotymi ramkami!")
print("  - Zdjęcie Erica (po pierwszej odpowiedzi)")
print("  - Postać Erik w starej Tibii (po historii gracza)")
print("  - Postać GM Erik w Project Fibula (po pytaniu o granie postacią)")
