from bot_responses import SimpleReply
from revealer_bot.decryption_action import decrypt_attached_tmk
from built_in_messages import simple_reply_defaults


available_responses = list()
for prompt, reply in simple_reply_defaults:
    available_responses.append(SimpleReply(triggers=(prompt,), initial_reply=reply))


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
