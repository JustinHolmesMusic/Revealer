import asyncio
import json

import requests
from bot_responses import SimpleReply
from built_in_messages import simple_reply_defaults
from icmplib import async_ping

from revealer_bot.bot_responses import BotActionResponse

available_responses = list()
for prompt, reply in simple_reply_defaults:
    available_responses.append(SimpleReply(triggers=(prompt,), initial_reply=reply))

network_status_response = BotActionResponse(
    must_mention=True,
    triggers=("network status",),
    initial_reply="OK!  I'll check Threshold TACo network status.",
)

available_responses.append(network_status_response)


async def parse_message(message):
    for candidate_response in available_responses:
        for trigger in candidate_response.triggers:
            if trigger in message.content.lower():
                await candidate_response.respond_to(message)
