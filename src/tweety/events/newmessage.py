import threading
import time
from ..types.inbox import Inbox, Message


class NewMessageUpdate:
    def __init__(self, client, callback):
        self.client = client
        self.callback_func = callback
        self.inbox = Inbox(self.client.user.id, self.client, 1)
        list(self.inbox.generator())
        self.cursor = self.inbox.cursor
        self.wait_for_message()

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

        def respond(self, text, file=None, reply_to_message_id=None, audio_only=False, quote_tweet_id=None):
            return self.conversation.send_message(text, file, reply_to_message_id, audio_only, quote_tweet_id)

        def __repr__(self):
            return "NewMessage(id={}, sender={}, receiver={}, time={}, text={})".format(
                self.id, self.sender, self.receiver, self.time, self.text
            )

    def wait_for_message(self):
        while True:
            new_chats = self.inbox.get_new_messages()
            if new_chats:
                for conv in new_chats:
                    for message in conv.messages:
                        event = None
                        if isinstance(message, Message):
                            if not message.sender or str(message.sender.id) != str(self.client.user.id):
                                event = self.NewMessage(conv, message)
                        else:
                            event = message

                        if event:
                            threading.Thread(target=self.callback_func, args=(event,)).start()

            time.sleep(5)
