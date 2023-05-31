import os
import discord
from dotenv import load_dotenv
import logging
from gtts import gTTS
import random
import asyncio


class MyClient(discord.Client):
    async def on_ready(self):
        self.voice_client_dict: dict[int, discord.VoiceProtocol] = {}
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")

    async def on_message(self, message: discord.Message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.content.startswith("$"):
            if message.content[1:] == "connect":
                if message.author.guild.id not in self.voice_client_dict:
                    self.voice_client_dict[message.author.guild.id] = await message.author.voice.channel.connect()

                filename = "audio.wav"

                text = "Hello World!"

                # get audio from server
                tts = gTTS(text=text, lang="ja")
                tts.save(filename)

                # source = discord.FFmpegOpusAudio(filename)
                source = discord.FFmpegPCMAudio(filename)
                logger.info("play sound")
                self.voice_client_dict[message.author.guild.id].play(source)

            if message.content[1:] == "disconnect":
                await self.voice_client_dict[message.author.guild.id].disconnect()


# .envファイルの読み込み(デバッグ環境のみ)
load_dotenv(verbose=True)
load_dotenv(".env")

# インテント設定
intents = discord.Intents.default()
intents.message_content = True

discord.utils.setup_logging(formatter=logging.Formatter("%(asctime)s %(levelname)s %(filename)s\t%(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger = logging.getLogger("test")

client = MyClient(intents=intents)
client.run(os.environ["BOT_TOKEN"], log_handler=None)
