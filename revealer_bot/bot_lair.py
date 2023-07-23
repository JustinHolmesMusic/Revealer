import discord
from discord import app_commands

JM_MUSIC_GUILD_ID = discord.Object(id=1126841404056948806)  # replace with your guild id


class RevealerBotDiscordClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=JM_MUSIC_GUILD_ID)
        await self.tree.sync(guild=JM_MUSIC_GUILD_ID)


intents = discord.Intents.default()
the_actual_revealer_bot = RevealerBotDiscordClient(intents=intents)
