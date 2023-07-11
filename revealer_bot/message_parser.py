from revealer_bot.decryption_action import decrypt_attached_tmk




async def parse_message(message):
    if "decrypt" in message.content.lower():
        message_to_look_for_attachments = message.reference.resolved
        if message_to_look_for_attachments.attachments:
            await decrypt_attached_tmk(message_to_look_for_attachments)
        # await message.reply(reply)
############################


    for question, reply in command_maping:

        if question in message.content.lower():
            await message.reply(reply)
