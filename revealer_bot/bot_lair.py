import discord
from discord import app_commands

JM_MUSIC_GUILD_ID = discord.Object(id=1126841404056948806)
THRESHOLD_GUILD_ID = discord.Object(id=866378471868727316)


class RevealerBotDiscordClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=JM_MUSIC_GUILD_ID)
        self.tree.copy_global_to(guild=THRESHOLD_GUILD_ID)

        await self.tree.sync(guild=JM_MUSIC_GUILD_ID)
        await self.tree.sync(guild=THRESHOLD_GUILD_ID)

intents = discord.Intents.default()
the_actual_revealer_bot = RevealerBotDiscordClient(intents=intents)
