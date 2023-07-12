from typing import Iterable, Callable

from revealer_bot.bot_lair import the_actual_revealer_bot

def bot_is_mentioned_in(message):
    for mention in message.mentions:
        if mention.bot:
            return True
    else:
        return False



class BotResponse:
    """
    In response to a message, reply to a message or take some action.
    """

    def __init__(self, triggers: Iterable, initial_reply: str, must_mention: bool = False):
        self.triggers = triggers
        self.initial_reply = initial_reply


class SimpleReply(BotResponse):
    """
    Reply to a message with a message.
    """

    async def respond_to(self, message):
        await message.reply(self.initial_reply)


class BotActionResponse(BotResponse):
    """
    A bot takes some action in response to a message.
    """