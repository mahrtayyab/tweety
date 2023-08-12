import threading
import time
from ..types.inbox import Inbox


class NewMessageUpdate:
    def __init__(self, request, callback):
        self.request = request
        self.callback_func = callback
        self.inbox = Inbox(self.request.user.id, self.request)
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
            self.text = self.message.text
            self.time = self.message.time
            self.id = self.message.id
            self.media = self.message.media

        def respond(self, text):
            return self.conversation.send_message(text)

        def __repr__(self):
            return "NewMessage(id={}, sender={}, receiver={}, time={}, text={})".format(
                self.id, self.sender, self.receiver, self.time, self.text
            )

    def wait_for_message(self):
        while True:
            new_chats = Inbox(None, self.request, cursor=self.cursor)
            self.cursor = new_chats.cursor
            if new_chats.conversations:
                for conv in new_chats.conversations:
                    for message in conv.messages:

                        if str(message.sender.id) != str(self.request.user.id):
                            event = self.NewMessage(conv, message)
                            threading.Thread(target=self.callback_func, args=(event,)).start()

            time.sleep(5)
