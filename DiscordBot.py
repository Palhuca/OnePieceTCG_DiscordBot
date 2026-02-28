import os

import db_initialize
from discord import Intents, Client, Message
from responses import get_message_agent, get_message_agent_with_translation
from responses import translate_message

#load token from env file
TOKEN = os.getenv('DISCORD_TOKEN')

#BOT SETUP
intents = Intents.default()
intents.message_content = True
client = Client(intents=intents)

#message funtionality
async def send_message(message: Message, user_message: str, bot_id) -> None:
    if not user_message:
        print("No message to send")
        return

    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    if bot_id in message.mentions:
        try:
            user_message = user_message.replace(f"<@{bot_id.id}>", "").strip()
            #user_message = translate_message(user_message)
            #print(f"Tradução: {user_message}")
            #response = get_resposes(user_message)
            #response = get_message_agent(user_message)
            response = get_message_agent_with_translation(user_message)
            await message.author.send(response) if is_private else await message.channel.send(response)
        except Exception as e:
            #print the error stacktrace
            print(f"{e.__traceback__}")
            print(f"Error: {e}")
    else:
        print("Not for me")

#Hadleing the start event
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

#Handling the message event
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return

    username = message.author
    user_message = message.content
    channel = message.channel

    print(f'{username} said: {user_message} in {channel}')
    await send_message(message, user_message, client.user)

#main entry point
def initializeDiscord():
    client.run(TOKEN)