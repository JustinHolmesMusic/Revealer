def bot_is_mentioned_in(message):
    for mention in message.mentions:
        if mention.bot:
            return True
    else:
        return False