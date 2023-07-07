import discord
from discord.ext import commands
from message_parser import parse_message
import os

import dotenv
dotenv.load_dotenv()

bot_token = os.environ['BOT_TOKEN']

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if not message.channel.name in ("test-bot", "vegetables"):
        return
    await parse_message(message=message)

 #   await message.channel.send("Hello World")

    for channel in bot.get_all_channels():
        if isinstance(channel, discord.TextChannel):
            await channel.send(f'Message received: {message.content}')

bot.run(bot_token)
