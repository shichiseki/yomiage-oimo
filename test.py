import os
import discord
from dotenv import load_dotenv
import logging
from gtts import gTTS
import discord


# .envファイルの読み込み(デバッグ環境のみ)
load_dotenv(verbose=True)
load_dotenv(".env")

# インテント設定
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    logging.info(f"login as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if message.content.startswith("$"):
        if message.content[1:] == "connect":
            voice_client = await message.author.voice.channel.connect()

            filename = "audio.wav"

            text = "Hello World!"

            # get audio from server
            tts = gTTS(text=text, lang="ja")
            tts.save(filename)

            source = discord.FFmpegOpusAudio(filename)
            voice_client.play(source)

        if message.content[1:] == "disconnect":
            voice_client = [voice for voice in client.voice_clients if message.author.voice.channel == voice.channel][0]
            await voice_client.disconnect()


client.run(os.environ["BOT_TOKEN"], root_logger=True)
