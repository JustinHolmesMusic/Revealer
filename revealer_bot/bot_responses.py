import asyncio
import json
from typing import Iterable

import requests


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
        self.must_mention = must_mention

    async def _construct_and_send_response(self, message):
        raise NotImplementedError

    async def send_initial_reply_to(self, message):
        await message.reply(self.initial_reply)

    async def respond_to(self, message):
        if self.must_mention:
            if not bot_is_mentioned_in(message):
                return

        await self._construct_and_send_response(message)


class SimpleReply(BotResponse):
    """
    Reply to a message with a message.
    """

    thread = None

    async def _construct_and_send_response(self, message):
        self.initial_reply_task = self.send_initial_reply_to(message)


class BotActionResponse(BotResponse):
    """
    A bot takes some action in response to a message.
    """

    thread = None

    async def send_initial_reply_to(self, message):
        thread_name = f"Network Status requested by {message.author.display_name} at {message.created_at.isoformat()[0:16]}"
        self.thread = await message.create_thread(name=thread_name, auto_archive_duration=60)
        await self.thread.send(self.initial_reply)

    async def _construct_and_send_response(self, message):
        response_tasks = set()
        response_tasks.add(asyncio.create_task(self.send_initial_reply_to(message)))
        response_tasks.add(asyncio.create_task(self.action()))
        return response_tasks
