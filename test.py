import os
import discord
from dotenv import load_dotenv
import logging

load_dotenv(verbose=True)
load_dotenv(".env")


intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info(f'We have logged in as {client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(os.environ["BOT_TOKEN"])
