import json

# Load current news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

content = data[0]['modalContent']['content']

# Find and replace only the erik_char image to make it smaller
content = content.replace(
    "<img src='data:image/jpg;base64,",
    "<img src='data:image/jpg;base64,MARKER"
)

# Split to find the erik_char image specifically
parts = content.split("Erik's character from the old days of Tibia")
if len(parts) > 1:
    # Work backwards from the caption to find the img tag
    before_caption = parts[0]
    after_caption = parts[1]
    
    # Replace the style in the section before this caption
    if "max-width: 60%;" in before_caption:
        # Find the last occurrence before this caption
        last_img_pos = before_caption.rfind("<img src='data:image/jpg;base64,MARKER")
        if last_img_pos != -1:
            # Replace in this specific img tag
            img_end = before_caption.find("'/>", last_img_pos)
            if img_end != -1:
                img_tag = before_caption[last_img_pos:img_end+3]
                new_img_tag = img_tag.replace("max-width: 60%;", "max-width: 35%;")
                content = before_caption[:last_img_pos] + new_img_tag + before_caption[img_end+3:] + "Erik's character from the old days of Tibia" + after_caption

# Remove marker
content = content.replace("MARKER", "")

# Update content
data[0]['modalContent']['content'] = content

# Save back
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✓ Zmniejszono obrazek postaci Erika z Tibii do 35%")
