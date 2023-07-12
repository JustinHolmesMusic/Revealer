from bot_responses import SimpleReply
from built_in_messages import simple_reply_defaults
from revealer_bot.bot_responses import BotActionResponse
from bob_and_other_networky_things import bob

available_responses = list()
for prompt, reply in simple_reply_defaults:
    available_responses.append(SimpleReply(triggers=(prompt,), initial_reply=reply))


def network_status(message):
    assert False


network_status_response = BotActionResponse(action=network_status,
                                            must_mention=True,
                                            triggers=("network status",),
                                            initial_reply="Network status")

available_responses.append(network_status_response)


async def parse_message(message):
    for candidate_response in available_responses:
        for trigger in candidate_response.triggers:
            if trigger in message.content.lower():
                await candidate_response.respond_to(message)
