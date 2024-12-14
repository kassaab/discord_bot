"""
Discord Bot - Simple Server Information and Interaction Bot

This bot is designed for use in Discord channels and provides basic interaction and server information commands. 
It responds to specific messages in a designated channel and includes a default response for unrecognized commands.

### Features:
1. Greets users when they say "hello world" or "hi".
2. Bids farewell when users say "bye".
3. Tells a random joke when prompted with "tell me a joke".
4. Provides server instance information when users ask "tell me about my server".
5. Handles unrecognized messages gracefully with a helpful default response.

### Setup Instructions:
1. Ensure you have Python 3.9 or higher installed.
2. Install required dependencies:
3. Add your bot token to a `.env` file with the key `TOKEN`.
4. Run the script using:
"""


#Import required class libraries
import os, discord, random
from dotenv import load_dotenv
from ec2_metadata import ec2_metadata

#Load the token file and declare a token variable.
load_dotenv("token.env")
token = os.getenv('TOKEN')

bot = discord.Client()

#Give the bot access to read messages
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = discord.Bot(intents=intents)

#Exception handler to ensure the bot runs even if ec2 metadata is unavailable.
noData = "Data Unavailable"
instIP = None
instZone = None
instRegion = None

try:
    instIP = ec2_metadata.public_ipv4
    instZone = ec2_metadata.availability_zone
    instRegion = ec2_metadata.region

except Exception as e:
    instIP = noData
    instZone = noData
    instRegion = noData

#This runs once when we start the bot.
@bot.event
async def on_ready():
    print("Logged in as a bot {0.user}".format(bot))

#This runs everytime a message is sent
@bot.event
async def on_message(message):
    # Ignore the bot's own messages to prevent a loop
    if message.author == bot.user:
        return

    username = str(message.author)
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message {user_message} by {username} on {channel}')

    if channel == "bot":
        if user_message.lower() == "hello world" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')
            return
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
            return
        elif user_message.lower() == "tell me a joke":
            jokes = [
                "Can someone please shed more light on how my lamp got stolen?",
                "Why is she called llene? She stands on equal legs.",
                "What do you call a gazelle in a lion's territory? Denzel."
            ]
            await message.channel.send(random.choice(jokes))
            return
        elif user_message.lower() == "tell me about my server":
            await message.channel.send(f'# Here is some info about your instance:\n'
                                        f'IP: {instIP} | Availability Zone: {instZone} | Region: {instRegion}')
            return

        # Default response for unrecognized messages
        await message.channel.send(f"I'm sorry, {username}, I didn't understand that. Try asking me something like:\n"
                                    f"- 'hello world'\n"
                                    f"- 'bye'\n"
                                    f"- 'tell me a joke'\n"
                                    f"- 'tell me about my server'")
                                        

#Run the bot using the token
bot.run(token)