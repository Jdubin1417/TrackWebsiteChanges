# Steps to Get the Bot Up and Running:

# 1. Create a Discord Application and Bot:
#    - Go to the Discord Developer Portal: https://discord.com/developers/applications
#    - Click on "New Application" and give it a name.
#    - Go to the "Bot" tab and click "Add Bot". Confirm by clicking "Yes, do it!".
#    - Under "Token", click "Copy" to copy your bot token.

# 2. Invite the Bot to Your Server:
#    - Go to the "OAuth2" tab in your application.
#    - Under "OAuth2 URL Generator", select the "bot" scope.
#    - Under "Bot Permissions", select the permissions your bot needs (e.g., "Send Messages", "Read Messages").
#    - Copy the generated URL and open it in your browser.
#    - Select the server you want to add the bot to and click "Authorize". Complete the CAPTCHA if prompted.

# 3. Enable Privileged Intents:
#    - Go to the "Bot" tab in your application.
#    - Under "Privileged Gateway Intents", enable the "Message Content Intent".
#    - Save the changes.

# 4. Install Required Libraries:
#    - Open a terminal and run:
#      pip install requests discord beautifulsoup4 transformers

# 5. Update and Run Your Script:
#    - Replace 'YOUR_DISCORD_BOT_TOKEN' with your actual bot token.
#    - Replace YOUR_CHANNEL_ID with the ID of the channel where you want to send messages.
#    - Save your script to a file, for example, WebChanges.py.
#    - Open a terminal and run:
#      python WebChanges.py

# Websites with a lot of traffic to test:
#    - BBC News: https://www.bbc.com/news
#    - CNN: https://www.cnn.com
#    - Reddit: https://www.reddit.com
#    - TechCrunch: https://techcrunch.com
#    - The New York Times: https://www.nytimes.com
#    - GitHub Trending: https://github.com/trending
#    - Hacker News: https://news.ycombinator.com
#    - Stack Overflow: https://stackoverflow.com
#    - Product Hunt: https://www.producthunt.com
#    - Wikipedia: https://en.wikipedia.org/wiki/Main_Page

# Your bot should now be running and monitoring the specified website for changes. It will send a message to the specified Discord channel if any changes are detected.
# eCTF Channel ID = 1297419767749021767
import requests
import discord
from discord.ext import tasks
from bs4 import BeautifulSoup
from difflib import Differ
from datetime import datetime
from collections import Counter

# Discord bot token and channel ID
DISCORD_TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
CHANNEL_ID = YOUR_CHANNEL_ID

# URL of the website to track
URL = 'https://news.ycombinator.com'

# Define the intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent

# Initialize the Discord client with intents
client = discord.Client(intents=intents)

# Store the initial state of the website
initial_content = None

@client.event
async def on_ready():
    # Print a message when the bot is ready
    print(f'Logged in as {client.user}')
    # Notify that website monitoring has started
    channel = await client.fetch_channel(CHANNEL_ID)
    if isinstance(channel, discord.TextChannel):
        await channel.send(f'Website monitoring has started for {URL}.')
    # Start the task to check for website changes
    check_website_change.start()

@tasks.loop(minutes=1)
async def check_website_change():
    global initial_content
    # Send a GET request to the website
    response = requests.get(URL)
    # Parse the HTML content of the website
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract the text content of the website
    current_content = soup.get_text()

    if initial_content is None:
        # If this is the first run, store the current content as the initial content
        initial_content = current_content
        return

    # Compare the current content with the initial content
    differ = Differ()
    diff = list(differ.compare(initial_content.splitlines(), current_content.splitlines()))

    # Filter out unchanged lines
    changes = [line for line in diff if line.startswith('+ ') or line.startswith('- ')]

    if changes:
        # Count the types of changes
        added_lines = len([line for line in changes if line.startswith('+ ')])
        removed_lines = len([line for line in changes if line.startswith('- ')])
        
        # Create a summary of the changes
        summary = f"There are {added_lines} new additions and {removed_lines} removals on the website."

        # Fetch the channel by ID
        channel = await client.fetch_channel(CHANNEL_ID)
        if isinstance(channel, discord.TextChannel):
            current_time = datetime.now().strftime("%I:%M%p %m/%d/%Y")
            await channel.send(f'Website changes detected at {current_time}:\n{summary}')
    else:
        current_time = datetime.now().strftime("%I:%M%p %m/%d/%Y")
        channel = await client.fetch_channel(CHANNEL_ID)
        if isinstance(channel, discord.TextChannel):
            await channel.send(f'No changes as of {current_time}')

    # Update the initial content
    initial_content = current_content

# Run the bot
client.run(DISCORD_TOKEN)