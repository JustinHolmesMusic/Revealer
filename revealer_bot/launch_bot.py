import os

from bot_lair import the_actual_revealer_bot
from message_parser import parse_message
from revealer_bot.bob_and_other_networky_things import bob

bot_token = os.environ["DISCORD_BOT_TOKEN"]


@the_actual_revealer_bot.event
async def on_ready():
    print(f'Logged in as {the_actual_revealer_bot.user.name} ({the_actual_revealer_bot.user.id})')
    print('------')


@the_actual_revealer_bot.event
async def on_message(message):
    print(message.content)

    if message.author.bot:
        return

    if not message.channel.name in (
            "test-bot", "vegetables", "nft", "threshold", "contributed", "website", "art", "reset", "not enough",
            "verify",
            "number", "minimum", "usd", "after", "3 ETH",):
        return

    await parse_message(message=message)


the_actual_revealer_bot.run(bot_token)
bob.start_learning_loop()
