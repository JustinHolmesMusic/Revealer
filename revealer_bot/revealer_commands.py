import discord
from discord import app_commands

from revealer import epilogue
from revealer_bot.bot_lair import the_actual_revealer_bot
from revealer_bot.decryption_action import decrypt_attached_tmk
from revealer_bot.network_status import get_lynx_network_status


@the_actual_revealer_bot.tree.command()
@app_commands.describe(network="The network you want to get the status of - currently only 'lynx' or 'tapir'")
async def network_status(interaction: discord.Interaction, network: str):
    """Checks status of Threshold lynx testnet"""
    await get_lynx_network_status(interaction)

@the_actual_revealer_bot.tree.command()
@app_commands.describe(address="The address of a Revealer contract whose symmetric key you want to reveal.")
async def reveal(interaction: discord.Interaction, address: str):
    """Reveals a symmetric key for a given Revealer contract."""
    await interaction.response.send_message("OK!  I'll try to reveal the symmetric key for that contract, using Threshold Access Control.")
    try:
        sym_key = epilogue.reveal_symmetric_key(address)
    except PermissionError:
        await interaction.followup.send("Threshold Network is telling me that the conditions aren't met to decrypt this..")
        return
    await interaction.followup.send(f"Here's the symmetric key: {bytes(sym_key).hex()}")

@the_actual_revealer_bot.tree.context_menu(name="Decrypt using Threshold Network")
async def decrypt(interaction: discord.Interaction, message: discord.Message):
    """If Conditions are met, decrypts a TMK file using Threshold network."""
    await decrypt_attached_tmk(message)


