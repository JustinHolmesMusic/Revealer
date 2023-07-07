
import discord
from discord.ext import commands
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

    for channel in bot.get_all_channels():
        if isinstance(channel, discord.TextChannel):
            await channel.send(f'Message received: {message.content}')

bot.run(bot_token)
