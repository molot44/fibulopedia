import json

# Load JSON
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get content
content = data[0]['modalContent']['content']

# Add first image after intro, before "About Erik"
content = content.replace(
    '</p><h3>About Erik</h3>',
    '</p><div style=\'text-align: center; margin: 2rem 0;\'><img src=\'assets/interview_erik/eric_stream.png\' alt=\'GM Erik\' style=\'max-width: 400px; width: 100%; border: 3px solid #d4af37; border-radius: 8px; box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);\'/></div><h3>About Erik</h3>'
)

# Add second image after first answer
content = content.replace(
    'I played every day at the library.</p>',
    'I played every day at the library.</p><div style=\'text-align: center; margin: 2rem 0;\'><img src=\'assets/interview_erik/erik_char.jpg\' alt=\'Erik playing Tibia\' style=\'max-width: 500px; width: 100%; border: 3px solid #d4af37; border-radius: 8px; box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);\'/><p style=\'font-style: italic; color: #888; margin-top: 0.5rem; font-size: 0.9rem;\'>Erik\'s character back in the day</p></div>'
)

# Add third image before "The Origins of Project Fibula"
content = content.replace(
    'my secret level 8.</p><h3>The Origins',
    'my secret level 8.</p><div style=\'text-align: center; margin: 2rem 0;\'><img src=\'assets/interview_erik/gmerik.png\' alt=\'GM Erik in Project Fibula\' style=\'max-width: 400px; width: 100%; border: 3px solid #d4af37; border-radius: 8px; box-shadow: 0 0 20px rgba(212, 175, 55, 0.3);\'/><p style=\'font-style: italic; color: #888; margin-top: 0.5rem; font-size: 0.9rem;\'>GM Erik\'s character on Project Fibula</p></div><h3>The Origins'
)

# Update content
data[0]['modalContent']['content'] = content

# Save JSON
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print('Done! Images added successfully.')
