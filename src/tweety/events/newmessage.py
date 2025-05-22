import asyncio
from typing import Union, List

from ..types.inbox import Inbox, Message
from ..utils import get_running_loop
from .base import BaseUpdateMethod

class NewMessageUpdate(BaseUpdateMethod):
    def __init__(
            self,
            from_users: Union[str, List[str]] = None,
            blacklist_users: Union[str, List[str]] = None,
            func = None
    ):
        self.from_users = from_users
        self.blacklist_users = blacklist_users
        self.func = func
        self.inbox = None
        self.cursor = None
        self.client = None
        self.callback_func = None

    def __call__(self, client, callback):
        self.client = client
        self.callback_func = callback
        self.inbox = None
        self.cursor = None
        return self

    async def start(self):
        self.inbox = await self.client.get_inbox(pages=1)
        self.cursor = self.inbox.cursor
        await self.wait_for_message()

    class NewMessage:
        def __init__(self, conversation, message):
            self.conversation = conversation
            self.message = message
            self.conversation.messages = [message]
            self.participants = self.conversation.participants
            self.sender = self.message.sender
            self.receiver = self.message.receiver
            self.text = self.message.text if hasattr(self.message, "text") else None
            self.time = self.message.time
            self.id = self.message.id
            self.media = self.message.media if hasattr(self.message, "media") else None

        async def respond(self, text, file=None, reply_to_message_id=None, audio_only=False, quote_tweet_id=None):
            return await self.conversation.send_message(text, file, reply_to_message_id, audio_only, quote_tweet_id)

        def __repr__(self):
            return "NewMessage(id={}, sender={}, receiver={}, time={}, text={})".format(
                self.id, self.sender, self.receiver, self.time, self.text
            )

    async def parse_filters(self):
        if self.blacklist_users:
            if not isinstance(self.blacklist_users, list):
                self.blacklist_users = [self.blacklist_users]

        if self.from_users:
            if not isinstance(self.from_users, list):
                self.from_users = [self.from_users]

    async def wait_for_message(self):
        while True:
            new_chats = await self.inbox.get_new_messages()
            if new_chats:
                for conv in new_chats:
                    for message in conv.messages:
                        event = None

                        if isinstance(message, Message):
                            if not message.sender or str(message.sender.id) != str(self.client.user.id):
                                event = self.NewMessage(conv, message)
                        else:
                            event = message

                        # TODO: Filtering User Messages

                        if event:
                            get_running_loop().create_task(self.callback_func(event))

            await asyncio.sleep(5)
