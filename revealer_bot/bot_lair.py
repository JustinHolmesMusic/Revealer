
from discord.ext import commands




import os
from typing import Optional

import discord
from discord import app_commands


JM_MUSIC = discord.Object(id=1126841404056948806)  # replace with your guild id


class RevealerBotDiscordClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=JM_MUSIC)
        await self.tree.sync(guild=JM_MUSIC)


intents = discord.Intents.default()
# intents.message_content = True  # TODO: Do we need this if we're using slash commands?

the_actual_revealer_bot = RevealerBotDiscordClient(intents=intents)
