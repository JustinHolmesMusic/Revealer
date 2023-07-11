from bot_responses import SimpleReply
from revealer_bot.decryption_action import decrypt_attached_tmk
from built_in_messages import simple_reply_defaults


available_responses = list()
for prompt, reply in simple_reply_defaults:
    available_responses.append(SimpleReply(triggers=(prompt,), initial_reply=reply))


async def parse_message(message):
    for candidate_response in available_responses:
        for trigger in candidate_response.triggers:
            if trigger in message.content.lower():
                await candidate_response.respond_to(message)

