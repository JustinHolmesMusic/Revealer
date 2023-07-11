class BotResponse:
    """
    In response to a message, reply to a message or take some action.
    """

    def __init__(self, triggers, initial_reply):
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