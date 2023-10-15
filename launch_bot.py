from dotenv import load_dotenv

from revealer.bob_and_other_networky_things import bob
from revealer_bot.revealer_commands import *  # noqa

load_dotenv()

bot_token = os.environ["DISCORD_BOT_TOKEN"]


@the_actual_revealer_bot.event
async def on_ready():
    print(f"Logged in as {the_actual_revealer_bot.user.name} ({the_actual_revealer_bot.user.id})")
    print("------synced------")


the_actual_revealer_bot.run(bot_token)
print("Bot is running - now starting learning loop.")
bob.start_learning_loop()
