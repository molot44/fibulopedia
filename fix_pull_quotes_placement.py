import json
import re

# Load current news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

content = data[0]['modalContent']['content']

# Remove all existing pull quotes first
content = re.sub(r'\n<blockquote class=\'pull-quote\'.*?</blockquote>\n', '', content, flags=re.DOTALL)

# Pull quote template
def make_pull_quote(text):
    return f"\n<blockquote class='pull-quote' style='font-size: 1.3rem; font-style: italic; color: #d4af37; border-left: 4px solid #d4af37; padding-left: 1.5rem; margin: 2rem 0;'>{text}</blockquote>\n"

# Now add pull quotes in the CORRECT locations based on where the text actually appears

# 1. "I had absolutely no idea how big this would get."
content = content.replace(
    "We had maybe… 100 people on Discord? I had no clue how much this project was going to grow!</p>",
    "We had maybe… 100 people on Discord? I had no clue how much this project was going to grow!</p>" + 
    make_pull_quote('"I had absolutely no idea how big this would get."')
)

# 2. "Whenever a small group can ruin the experience for the majority, that's where the line is."
content = content.replace(
    "Sure, this happens on main, but at least the majority collectively have the tools to do something about it.</p>",
    "Sure, this happens on main, but at least the majority collectively have the tools to do something about it.</p>" + 
    make_pull_quote('"Whenever a small group can ruin the experience for the majority, that\'s where the line is."')
)

# 3. "There's no perfect version of Tibia."
content = content.replace(
    "Each major version has pros and cons, and I'd love to see Project Fibula visit all of them someday, but for now we'll see how it goes until 7.6.</p>",
    "Each major version has pros and cons, and I'd love to see Project Fibula visit all of them someday, but for now we'll see how it goes until 7.6.</p>" + 
    make_pull_quote('"There\'s no perfect version of Tibia."')
)

# 4. "I don't think I've ever felt worse in my life."
content = content.replace(
    "There has been no worse feeling in my recent memory.</p>",
    "There has been no worse feeling in my recent memory.</p>" + 
    make_pull_quote('"I don\'t think I\'ve ever felt worse in my life."')
)

# 5. "Communication and trust are everything."
content = content.replace(
    "With each mistake I've made, I've asked myself what I can do to stop it from happening again.</p>",
    "With each mistake I've made, I've asked myself what I can do to stop it from happening again.</p>" + 
    make_pull_quote('"Communication and trust are everything."')
)

# 6. "No one is immune, and we will find out eventually."
content = content.replace(
    "Who knows if they would have gotten to where they are without the head start cheating gave them.</p>",
    "Who knows if they would have gotten to where they are without the head start cheating gave them.</p>" + 
    make_pull_quote('"No one is immune, and we will find out eventually."')
)

# 7. "Players need to realize that their automations are why Tibia is the way it is."
content = content.replace(
    "The Char Bazaar was added to combat account trading.</p>",
    "The Char Bazaar was added to combat account trading.</p>" + 
    make_pull_quote('"Players need to realize that their automations are why Tibia is the way it is."')
)

# 8. "Project Fibula feels different because it forces people to interact."
content = content.replace(
    "It makes you pause at times, forces you to talk to other players, gives you a sense of accomplishment, and much more — all things modern games no longer do.</p>",
    "It makes you pause at times, forces you to talk to other players, gives you a sense of accomplishment, and much more — all things modern games no longer do.</p>" + 
    make_pull_quote('"Project Fibula feels different because it forces people to interact."')
)

# 9. "This server is nothing without community."
content = content.replace(
    "I really enjoyed watching those groups play.</p>",
    "I really enjoyed watching those groups play.</p>" + 
    make_pull_quote('"This server is nothing without community."')
)

# 10. "I would rather have a lively world filled with a good community that pays me nothing."
content = content.replace(
    "I would rather have a lively world filled with a good community that pays me nothing than a worse world filled with people willing to give me $10 a month.</p>",
    "I would rather have a lively world filled with a good community that pays me nothing than a worse world filled with people willing to give me $10 a month.</p>" + 
    make_pull_quote('"I would rather have a lively world filled with a good community that pays me nothing."')
)

# 11. "It's basically ruined my life — but I wouldn't trade this experience for anything."
content = content.replace(
    "We are not going to forget Project Fibula, and that's really cool to think about.</p>",
    "We are not going to forget Project Fibula, and that's really cool to think about.</p>" + 
    make_pull_quote('"It\'s basically ruined my life — but I wouldn\'t trade this experience for anything."')
)

# 12. "We are not going to forget Project Fibula."
# This one is already included in #11, so we skip it to avoid duplication

# Update content
data[0]['modalContent']['content'] = content

# Save back
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✓ Poprawiono umiejscowienie wszystkich pull quotes!")
