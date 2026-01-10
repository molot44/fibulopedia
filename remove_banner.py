import json

# Load news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Remove the interview_banner.png image
content = data[0]['modalContent']['content']
content = content.replace(
    "<img src='assets/news/interview_banner.png' alt='Interview with GM Erik' style='max-width: 100%; margin-bottom: 2rem; border-radius: 8px;'/>",
    ""
)

# Update the content
data[0]['modalContent']['content'] = content

# Save back to JSON
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("Done! Removed interview_banner.png")
