import discord
from discord import app_commands

from revealer_bot.bot_lair import the_actual_revealer_bot
from revealer_bot.decryption_action import decrypt_attached_tmk
from revealer_bot.network_status import get_lynx_network_status


@the_actual_revealer_bot.tree.command()
@app_commands.describe(network="The network you want to get the status of - currently only 'lynx'")
async def network_status(interaction: discord.Interaction, network: str):
    """Checks status of Threshold lynx testnet"""
    if not network == "lynx":
        await interaction.response.send_message(f"Currently, only the lynx network is supported")

    await get_lynx_network_status(interaction)


@the_actual_revealer_bot.tree.context_menu(name="Decrypt using Threshold Network")
async def decrypt(interaction: discord.Interaction, message: discord.Message):
    """If Conditions are met, decrypts a TMK file using Threshold network."""
    await decrypt_attached_tmk(message)
