import json

# Load current interview content
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

content = data[0]['modalContent']['content']

# Replace blockquote with p for the YouTube question answer
old_text = """<h4>Q: How has the popularity of your YouTube presence helped—and how has it challenged—the launch of the project?</h4>
<blockquote>Having a background on YouTube certainly helped bring the initial players to the project; without it, nobody outside of my close friends would have logged in. However, you are absolutely right that it has also introduced its own challenges. I was not only the initial promoter—the friendly guy encouraging people to relive the nostalgia—but I am now also the administrator. I am responsible for every server issue, every ban, every cheater operating on the fringes, every message sent on Discord—the list goes on. This has led to many difficult moments and has damaged several good relationships I had before launching the server.</blockquote>"""

new_text = """<h4>Q: How has the popularity of your YouTube presence helped—and how has it challenged—the launch of the project?</h4>
<p><strong>Erik:</strong><br/>Having a background on YouTube certainly helped bring the initial players to the project; without it, nobody outside of my close friends would have logged in. However, you are absolutely right that it has also introduced its own challenges. I was not only the initial promoter—the friendly guy encouraging people to relive the nostalgia—but I am now also the administrator. I am responsible for every server issue, every ban, every cheater operating on the fringes, every message sent on Discord—the list goes on. This has led to many difficult moments and has damaged several good relationships I had before launching the server.</p>"""

if old_text in content:
    new_content = content.replace(old_text, new_text)
    
    # Update the JSON
    data[0]['modalContent']['content'] = new_content
    
    # Save back to file
    with open('content/news.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print("✓ Successfully fixed YouTube answer style!")
else:
    print("✗ Could not find the text to replace")
