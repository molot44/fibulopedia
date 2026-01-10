import json

# Load current news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get existing content
existing_content = data[0]['modalContent']['content']

# Add part 3
part3_content = """

<h3>Personal reflections</h3>

<h4>Q: How has the project's rapid growth affected you personally – your routines, relationships, and emotions?</h4>
<p><strong>Erik:</strong><br/>I've joked about this a lot — it's basically ruined my life. My sleep is destroyed, I haven't exercised since Nov 8, 2025, my wife has been supporting me more than anyone ever should, and I have experienced some of the best and worst emotions of my life. I'm not kidding here. But I also wouldn't trade this experience — it has given me so much joy. It's given my life a purpose I was missing; it's brought so many people together and reconnected old friendships; and I've said this from day one, but it's going to be a crazy memory. Not just for me, but for everyone who was here for it. We are not going to forget Project Fibula, and that's really cool to think about.</p>

<h4>Q: What has been your biggest positive surprise since launch?</h4>
<p><strong>Erik:</strong><br/>The number of players! I remember before launch, during my stream, people were asking what my expectations were. Deep down, I thought I could pull over 100 players for launch, but I didn't want my ego to get the best of me. I knew that server launches usually have the highest player counts, so I told myself I would be happy with 50 players logging in daily. I had no idea so many people would come to play! It's been insane!</p>

<h4>Q: If you could go back to launch day, what would you do differently?</h4>
<p><strong>Erik:</strong><br/>I would have prepared myself better for the sheer amount of instant feedback and reassured myself that everything would be fine despite the reactions of a crowd. One of the first conflicts on the server involved a guy preventing Tom the Tanner from speaking to anyone else. Nobody was able to sell dead rats, and he was using this as a strategy to get his team ahead. I still think moving him was a decent idea — it was essentially griefing multiplied by a launch full of players — but I acted from a place of panic or fear, not because I truly believed it was the right decision. As it turns out, you can sell dead rats to Seymour! Players would have been fine. This server and its players have taught me so many interesting things about old Tibia that I never knew!</p>

<h3>Quick-fire / lighter questions</h3>

<h4>Q: What's your favorite GM command?</h4>
<p><strong>Erik:</strong><br/>Haha, a custom one I added. Let's just say summoning monsters! ;)</p>

<h4>Q: If you could give yourself one "unobtainable" item just as a symbolic trophy, which one would it be?</h4>
<p><strong>Erik:</strong><br/>Golden Boots! I farmed Zugurosh so many times over the years on real Tibia and never looted them.</p>

<h4>Q: "Tell us about your first dragon." What do you remember from that moment, and why do you think stories like this still resonate?</h4>
<p><strong>Erik:</strong><br/>I'm so sad that I don't remember my first dragon, lol. I do remember my sister teaching me how to hunt dragons with demon skeletons, but I have no idea which dragon was actually my first.</p>

<h4>Q: How can we support you/the server?</h4>
<p><strong>Erik:</strong><br/>Honestly, foster community. Run a guild, connect other players, summon a monk for someone — anything like that. This server is nothing without community. It doesn't matter what the player count is or how many bots there are… it's how the server feels.<br/><br/>If I were a player, I would make a character called "Chief of Police" and go around interrogating runemakers, like under the depots. I'd make a guild and clean the server of bots. Why not? It's so much fun, you lose nothing, and you get free runes. I've already seen a couple of red skulls doing it, and I was cheering them on. Those are the players and/or groups that helped this server feel special, and I hope more players like them continue to join. Shoutout to Fellowship, Honkers, and all of the other guilds that made this server a lively and fun experience for everyone, regardless of their level. I really enjoyed watching those groups play.</p>

<h4>Q: Do you regret it?</h4>
<p><strong>Erik:</strong><br/>Absolutely not, although I do wish at times that I could reclaim some of my life without the server suffering as a result.</p>

<h4>Q: If CipSoft were to start classic servers today, in what form, shape, rules, and changes would you like them to launch with?</h4>
<p><strong>Erik:</strong><br/>I'm biased here, but I think they should do exactly what I'm doing. Obviously not as subjectively, and with much better tools like BattlEye to help them. I think Project Fibula has been an amazing server, and CipSoft could do it even better than I could.</p>

<h4>Q: What were your expectations of the project prior to launch — and what aspects turned out as you thought versus the biggest surprises?</h4>
<p><strong>Erik:</strong><br/>My expectations were really just a chill community server where people would enjoy the old content and have fun exploring each version. I've said this many times already, but the player count surprised me the most. The server is nowhere near chill!</p>

<h4>Q: If you want, you can write a few words directly to the players at the end here.</h4>
<p><strong>Erik:</strong><br/>Thanks for playing, even if you no longer do. Thanks for giving me grace with the rollbacks and the mistakes I've made along the way. I hope you walk away from this project with a positive experience, and that you let CipSoft know how badly you want this to become real. I'd love to join you and be a player myself!</p>"""

# Update the interview content
data[0]['modalContent']['content'] = existing_content + part3_content

# Save back to file
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✓ Dodano część 3 (finałową) wywiadu!")
