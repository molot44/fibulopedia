import json

# Load current news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get content and reduce image size
content = data[0]['modalContent']['content']
content = content.replace(
    "style='max-width: 100%; border-radius: 8px;'",
    "style='max-width: 70%; border-radius: 8px;'"
)

# Update content
data[0]['modalContent']['content'] = content

# Save back
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✓ Zmniejszono obrazek w modalu do 70% szerokości")
