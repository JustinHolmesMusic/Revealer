import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

the_actual_revealer_bot = commands.Bot(command_prefix='!', intents=intents)