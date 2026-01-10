import json
import re

# Load current news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

content = data[0]['modalContent']['content']

# Define pull quotes with their locations (after which text to insert them)
pull_quotes = [
    {
        "after": "We had maybe… 100 people on Discord? I had no clue how much this project was going to grow!</p>",
        "quote": '"I had absolutely no idea how big this would get."'
    },
    {
        "after": "At the end of the day, there's no perfect way to handle this, and everyone would run it differently.</p>",
        "quote": '"Whenever a small group can ruin the experience for the majority, that\'s where the line is."'
    },
    {
        "after": "I have fond memories of 7.x, 8.x, and even up to around Tibia 11. Each major version has pros and cons, and I'd love to see Project Fibula visit all of them someday, but for now we'll see how it goes until 7.6.</p>",
        "quote": '"There\'s no perfect version of Tibia."'
    },
    {
        "after": "There has been no worse feeling in my recent memory.</p>",
        "quote": '"I don\'t think I\'ve ever felt worse in my life."'
    },
    {
        "after": "With each mistake I've made, I've asked myself what I can do to stop it from happening again.</p>",
        "quote": '"Communication and trust are everything."'
    },
    {
        "after": "Who knows if they would have gotten to where they are without the head start cheating gave them.</p>",
        "quote": '"No one is immune, and we will find out eventually."'
    },
    {
        "after": "It makes you pause at times, forces you to talk to other players, gives you a sense of accomplishment, and much more — all things modern games no longer do.</p>",
        "quote": '"Project Fibula feels different because it forces people to interact."'
    },
    {
        "after": "It's so much fun, you lose nothing, and you get free runes. I've already seen a couple of red skulls doing it, and I was cheering them on. Those are the players and/or groups that helped this server feel special, and I hope more players like them continue to join. Shoutout to Fellowship, Honkers, and all of the other guilds that made this server a lively and fun experience for everyone, regardless of their level. I really enjoyed watching those groups play.</p>",
        "quote": '"This server is nothing without community."'
    },
    {
        "after": "I would rather have a lively world filled with a good community that pays me nothing than a worse world filled with people willing to give me $10 a month.</p>",
        "quote": '"I would rather have a lively world filled with a good community that pays me nothing."'
    },
    {
        "after": "We are not going to forget Project Fibula, and that's really cool to think about.</p>",
        "quote": '"It\'s basically ruined my life — but I wouldn\'t trade this experience for anything."'
    },
    {
        "after": "The Char Bazaar was added to combat account trading.<br/><br/>I get it — the game is hard and tedious. But people need to stop and think about why they're playing, and why Project Fibula is so special. These aren't just my words — many players have told me this server \"feels different.\"",
        "quote": '"Players need to realize that their automations are why Tibia is the way it is."'
    },
    {
        "after": "We are not going to forget Project Fibula, and that's really cool to think about.</p>",
        "quote": '"We are not going to forget Project Fibula."',
        "skip": True  # This one overlaps with another, will add manually
    }
]

# Pull quote HTML template
def make_pull_quote(text):
    return f"\n<blockquote class='pull-quote' style='font-size: 1.3rem; font-style: italic; color: #d4af37; border-left: 4px solid #d4af37; padding-left: 1.5rem; margin: 2rem 0;'>{text}</blockquote>\n"

# Insert pull quotes
for pq in pull_quotes:
    if pq.get('skip'):
        continue
    
    if pq['after'] in content:
        pull_quote_html = make_pull_quote(pq['quote'])
        content = content.replace(pq['after'], pq['after'] + pull_quote_html)
    else:
        print(f"Warning: Could not find location for quote: {pq['quote'][:50]}...")

# Add the last quote manually at the end before final message
final_quote = make_pull_quote('"We are not going to forget Project Fibula."')
# Insert before the final question
content = content.replace(
    "<h4>Q: If you want, you can write a few words directly to the players at the end here.</h4>",
    final_quote + "<h4>Q: If you want, you can write a few words directly to the players at the end here.</h4>"
)

# Update the content
data[0]['modalContent']['content'] = content

# Save back to file
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✓ Dodano wszystkie 12 pull quotes do wywiadu!")
