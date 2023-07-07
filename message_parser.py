async def parse_message(message):
    if "vegetables" in message.content.lower():
        await message.channel.send("I like vegetables too")