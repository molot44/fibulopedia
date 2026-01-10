import json

# Load current news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Format the interview content with proper HTML
interview_content = """<h3>About you / your background</h3>

<h4>Q: Could you tell us something about yourself – who you are, where you're from, and how your journey with Tibia began?</h4>
<p><strong>Erik:</strong><br/>I'm Eric, a guy from the USA who somehow got addicted to this 2D MMORPG, lol. It all started when I was 9 or 10 years old. A friend and I used to ride our bikes to the public library in the summer, and we met another kid there who showed us Tibia. He actually let us log into his brother's account during a test server that summer, from what I remember (ban for account sharing!). After that, I was hooked and would play every day at the library.</p>

<h4>Q: How did your history as a Tibia player influence your decision to create Project Fibula?</h4>
<p><strong>Erik:</strong><br/>After playing Tibia off and on my whole life, I finally left the game around five years ago and just couldn't bring myself to play anymore. It's not a bad game, but it's much different — we all know that. After playing both Classic WoW and Old School RuneScape, I knew Tibia needed the same thing: a return to the past to rediscover why we loved it in the first place. If you ever want to start an argument, just say "7.x is the best Tibia version!" and you'll get a ton of people going. That's why I felt Project Fibula would be fun as a progression server similar to WoW — it gives us the chance to see what parts felt good and what parts didn't, without needing to play six separate OT servers.</p>

<h4>Q: Do you play a character yourself in any form, or do you prefer a complete separation between being a GM and being a player?</h4>
<p><strong>Erik:</strong><br/>I do think it can be a conflict of interest to be both a GM and a player, and it certainly opens the door to fair criticism. For this reason, I only planned to make a public character that I could use to help other players and promote the server, but I just haven't had the time. I made a level 8 with my wife that I never announced, but otherwise I haven't played.<br/><br/>I think it's really interesting to see the game from the player's point of view, though. People were very friendly to me when I was streaming on launch day, but they haven't been as nice to my secret level 8!</p>

<h4>Q: How has the popularity of your YouTube presence helped — and how has it challenged — the launch of the project?</h4>
<p><strong>Erik:</strong><br/>Having a background on YouTube certainly helped bring initial players in; nobody but my close friends would have logged in without that. But you're spot on that it has brought its own challenges too.<br/><br/>Not only was I the initial promoter — the friendly guy telling you to come relive the nostalgia — but now I am also the administrator. I am responsible for every issue with the server, every ban, every outlying cheater, every message sent on Discord… the list goes on. It has created a lot of tough moments and ruined many good relationships I had before launching the server.</p>

<h3>Origins of Project Fibula</h3>

<h4>Q: When did you first feel that this idea could realistically become a serious, long-term project?</h4>
<p><strong>Erik:</strong><br/>I've had the idea in my head for a really long time — I'm sure many others have too. Seeing other MMORPGs make classic versions just makes you think, "Why won't Tibia do this?"<br/><br/>I believe it was late 2024 when I first heard about the engine I'm currently using — The Violet Project. I saw a promotional video for it and was instantly hit with nostalgia seeing all the old features. I bought the engine just to have it for personal use and to own a slice of Tibia history.<br/><br/>I'm not sure what exactly motivated me next, but I credited a Reddit post in my video for sparking some of this. I kept tinkering with the server and finally bought some hosting. Once I saw my friends were able to log in, I knew this could be real.</p>

<h4>Q: What was the hardest conceptual decision you had to make before launch?</h4>
<p><strong>Erik:</strong><br/>Whether or not to keep things 100% the same or make what I call "Modern Adjustments." Even now, players are constantly discussing things they feel are broken: "Why did you add this but not that?" "Will Ankrahmun be the same?! But it's broken!" At the end of the day, there's no perfect way to handle this, and everyone would run it differently.</p>

<h4>Q: What was the biggest unknown right before opening the server?</h4>
<p><strong>Erik:</strong><br/>This one's easy: how many people would join! During the test server, we were literally having discussions about whether MCing should be allowed because we thought there might not be enough people making runes. The test server only got 11 people logged in at once. We had maybe… 100 people on Discord? I had no clue how much this project was going to grow!</p>

<h3>Vision, authenticity & technical foundations</h3>

<h4>Q: You've said the server aims to feel like early Tibia but isn't an exact 1:1 replica. What 2–3 compromises were necessary to make it stable, fair, and engaging for a modern audience?</h4>
<p><strong>Erik:</strong><br/>I'm definitely going to echo the modern adjustments page here, because those felt necessary to implement and I still don't regret them.</p>

<p><strong>Open PvP</strong><br/>We all know Tibia 7.1 didn't have skulls, but it wasn't considered "Hardcore PvP" back then. It was just a world where you could kill other players. It wouldn't have made sense to start the server as Hardcore PvP, let the veterans kill everyone unchecked, and then add skulls months later (7.2) when everyone had already quit.</p>

<p><strong>Quest System</strong><br/>In original 7.1, quests were literally just containers with loot inside them that either reset daily or on map updates — I'm not sure which, or if it was a mix of both. Players had to naturally find these quests, and there are even screenshots of people saying things like "that demon legs quest was grabbed X times on Antica." In 2025, quests would have been rushed immediately, and then it would have devolved into people parking level 8s at every quest and checking at server save for the loot. Sure, it would have forced players to loot more items instead of grabbing them from quests, but the abusers would have been the real winners. Like Open PvP, I felt it was better to just advance to 7.2 for this, which is when the actual quest system was introduced.</p>

<p><strong>Amulet of Life</strong><br/>Check any tibiacam from 7.1 and you will see every player wearing this amulet. The Amulet of Life protected items as well as experience and skill loss. It effectively removed death as a feature of the game, which is why it was introduced and nerfed in just a single update. While I still have it in the game for nostalgia, I advanced it to 7.2 so it functionally works like an Amulet of Loss. Without doing this, I felt players would have simply refused to play the game until they had grinded 50k, and it would have definitely encouraged much more RMT.</p>

<h4>Q: How do you personally draw the line between nostalgia and modern quality-of-life, so the spirit of 7.1 stays intact?</h4>
<p><strong>Erik:</strong><br/>For me, the line seems to be drawn whenever a small group can ruin the experience for the majority. A small, coordinated war team could destroy most players if this were Hardcore PvP. A small group could hoard all quest loot if there wasn't a quest system. This is also why we prevented spawn blocking on Rookgaard at the beginning of the server — a small group could easily block entire sections of the map so the majority couldn't play. Sure, this happens on main, but at least the majority collectively have the tools to do something about it.</p>

<h4>Q: The project revisits different chapters of Tibia's evolution across phases. What are the main goals of this approach?</h4>
<p><strong>Erik:</strong><br/>The main goal of Project Fibula is to experience all of Tibia, because I don't think there is a perfect version. I don't even think there's an old Tibia and a new Tibia — there are more like three or four Tibias if you consider how radically the game has changed over the years. I have fond memories of 7.x, 8.x, and even up to around Tibia 11. Each major version has pros and cons, and I'd love to see Project Fibula visit all of them someday, but for now we'll see how it goes until 7.6.</p>"""

# Update the interview content
data[0]['modalContent']['content'] = interview_content

# Save back to file
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✓ Dodano część 1 wywiadu!")
