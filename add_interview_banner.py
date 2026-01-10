import json

# Load current news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get existing content
existing_content = data[0]['modalContent']['content']

# Add banner image at the beginning
banner_html = "<div style='text-align: center; margin-bottom: 2rem;'><img src='assets/interview_erik/interview_banner.png' alt='Interview with GM Erik' style='max-width: 100%; border-radius: 8px;'/></div>\n\n"

# Update the interview content with banner at the beginning
data[0]['modalContent']['content'] = banner_html + existing_content

# Save back to file
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✓ Dodano banner na górze wywiadu!")
