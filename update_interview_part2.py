import json

# Load current news.json
with open('content/news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Get existing content
existing_content = data[0]['modalContent']['content']

# Add part 2
part2_content = """

<h3>Launch, growth & challenges</h3>

<h4>Q: The daily peak of 800+ players and strong online records are impressive. What do you think worked best – both in promotion and in the server's design or timing?</h4>
<p><strong>Erik:</strong><br/>Well, you definitely can't have a good server with zero promotion. I think my initial Twitch streams and YouTube video attracted a good chunk of players, and I also think the unique twist of version progression, plus the timing of launching the server before the holidays, helped. However, I attribute the majority of the growth to the streamers who came out to play. I hope Project Fibula can help these streamers leverage their way into better deals, because they really blew this server up. I'm happy to vouch for them if it was ever needed.</p>

<h4>Q: The community stayed strong despite three 24-hour rollbacks. How did you feel making those calls as the person responsible for the project?</h4>
<p><strong>Erik:</strong><br/>Truthfully, I felt awful. It's one thing when a crash is due to intentional abuse — that really sucks — but it's another thing when it's due to inexperience or carelessness.<br/><br/>I mentioned in my news post that one of the crashes, which involved around 22 hours of progress, was entirely caused by me. I don't know if I've ever felt worse in my life. Knowing that I lost an entire day's worth of progress multiplied by all those players sank my heart to the bottom of my chest. There has been no worse feeling in my recent memory.</p>

<h4>Q: Looking back, what did you learn from handling those rollbacks — especially in terms of communication and maintaining trust?</h4>
<p><strong>Erik:</strong><br/>Communication and trust are everything. If you make a mistake, you have to be honest about it. When I crashed the server, I could have lied about it — who would have known? It would have been much easier to blame it on an attacker again, and nobody would have questioned me. But that would change the way I view myself, and that's not a good thing.<br/><br/>I've also learned that simply apologizing for making a mistake is not enough. "Sorry" is cheap. You also need a plan for how you're going to prevent that mistake from happening again, or you will lose people's trust. With each mistake I've made, I've asked myself what I can do to stop it from happening again.</p>

<h4>Q: The connection issues and DDoS impact for European players have been a major topic, with many relying on VPNs. How do you view the situation now, and what solutions feel the most realistic?</h4>
<p><strong>Erik:</strong><br/>This has been a very difficult problem to handle, and honestly, you can never get rid of DDoS for good. It's all about how motivated an attacker is. I've taken steps to harden protections, and I have a plan to migrate to a new server, but it's taking longer than I thought due to everything else going on.</p>

<h3>Community, moderation & fairness</h3>

<h4>Q: The Discord community is highly engaged. How do you see the role of community feedback in shaping the server — and where is your "non-negotiable" core vision?</h4>
<p><strong>Erik:</strong><br/>This is a tough one. Recreating the original experience is kind of my "non-negotiable" vision. I've made some of my own changes, sure, but I don't feel like there's a lot of room for feedback. Not that I don't think player feedback is valuable — more that I'm tucking that feedback away for the future, in case I ever want to try to make a "better" Tibia.</p>

<h4>Q: There have been a lot of bans overall. From your perspective, what types of abuse have been the biggest issue since launch, and what message would you like to send about your approach to enforcement?</h4>
<p><strong>Erik:</strong><br/>Jeez, I can barely remember because there have been so many. It all mostly falls under botting — whether it's a bot making runes, fishing, hunting, etc. Some people use homemade macros, sure, but those are obviously far less advanced. If there's one message I'd like to send, it's that no one is immune, and that we will eventually find out. Many high-level players who get banned claim they only did "one little thing ages ago," but it doesn't matter. I wish I could ban them before they sank more time into the game, but just because they gained a lot of experience doesn't change the fact that they cheated. Who knows if they would have gotten to where they are without the head start cheating gave them.</p>

<h4>Q: How do you approach bots/macros in a classic environment where the grind is real and the temptation to automate is high?</h4>
<p><strong>Erik:</strong><br/>Players need to realize that their automations are why Tibia is the way it is today. Runes are sold in the store because of runefarms. Stamina exists because of account sharing. The Char Bazaar was added to combat account trading.<br/><br/>I get it — the game is hard and tedious. But people need to stop and think about why they're playing, and why Project Fibula is so special. These aren't just my words — many players have told me this server "feels different." It's not because the content is engaging; we're acknowledging that here. It's not because the game is hard. It's because the game fosters community. It makes you pause at times, forces you to talk to other players, gives you a sense of accomplishment, and much more — all things modern games no longer do.</p>

<h3>What's next</h3>

<h4>Q: Many players are asking for an EU server and/or a non-PvP world. What conditions would need to be met for that to make sense technically and socially?</h4>
<p><strong>Erik:</strong><br/>At this point, either more money or a decline in players on Amera. I had no idea what I was in for when I launched this project. I had a million ideas, but I didn't realize how much administrative work would be required due to the number of players, which has pulled me away from those ideas.<br/><br/>If this server had simply been 100 players, and launching a second world would add another 100 without taking away from the first, it would have been a no-brainer already. But I was being careful because I didn't want to harm Amera's population. I wanted to keep that "full world" feeling. Now we are at max capacity. I'm spending every waking hour I have on this server, and it's still not enough. I either have to hire outside help, or the server needs to slow down to a much more manageable level.</p>

<h4>Q: Some community members also wonder about premium models or tokens. Do you see any path toward monetization, or do you prefer to keep the project strictly community-first?</h4>
<p><strong>Erik:</strong><br/>When you sent me this interview, the Patreon didn't exist yet, but it does now. I am keeping the project free because that was my original vision, but I have allowed players the option to support the server if they wish. Instead of gating the game behind premium, I have currently gated account creation behind applications, and I am also exploring other options. I would rather have a lively world filled with a good community that pays me nothing than a worse world filled with people willing to give me $10 a month.</p>

<h4>Q: What are your top priorities for the next period of development?</h4>
<p><strong>Erik:</strong><br/>Honestly, just catching up. There are so many outstanding issues to address and not enough time. Too many to name here.</p>"""

# Update the interview content
data[0]['modalContent']['content'] = existing_content + part2_content

# Save back to file
with open('content/news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✓ Dodano część 2 wywiadu!")
