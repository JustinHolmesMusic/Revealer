import os

from bot_lair import the_actual_revealer_bot
from message_parser import parse_message

from revealer_bot.bob_and_other_networky_things import bob

bot_token = os.environ["DISCORD_BOT_TOKEN"]


@the_actual_revealer_bot.event
async def on_ready():
    print(f"Logged in as {the_actual_revealer_bot.user.name} ({the_actual_revealer_bot.user.id})")
    print("------synced------")


from revealer_commands import *

the_actual_revealer_bot.run(bot_token)
bob.start_learning_loop()
