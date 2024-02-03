import re
import threading
import time
from . import User, Media, URL, Hashtag, ShortUser, Symbol
from ..utils import parse_time, parse_wait_time


class Inbox(dict):
    HAS_MORE_STATUS = "HAS_MORE"
    AT_END_STATUS = "AT_END"

    def __init__(self, user_id, client, cursor=None):
        super().__init__()
        self._client = client
        self._tmp_conv_id = []
        self.conversations = []
        self.messages = []
        self.cursor = cursor
        self.last_seen_event_id = None
        self.trusted_last_seen_event_id = None
        self.untrusted_last_seen_event_id = None
        self.user_id = user_id
        self.get_initial()

    def _parse_response(self, response):
        _initial_inbox = response.get('inbox_initial_state') or response.get('user_events') or response.get('inbox_timeline')

        if _initial_inbox.get('conversations'):
            for conservation in _initial_inbox['conversations'].values():
                _conversation = Conversation(conservation, _initial_inbox, self._client)
                if str(_conversation.id) not in self._tmp_conv_id:
                    self.conversations.append(_conversation)

        for conv in self.conversations:
            self._tmp_conv_id.append(str(conv.id))

        return _initial_inbox or {}

    def get_initial(self):
        _threads = []
        response = self._client.http.get_inbox(self.user_id, cursor=self.cursor)

        _initial_inbox = self._parse_response(response)

        self.cursor = self['cursor'] = _initial_inbox.get('cursor')
        self.last_seen_event_id = self['last_seen_event_id'] = _initial_inbox.get('last_seen_event_id')
        self.trusted_last_seen_event_id = self['trusted_last_seen_event_id'] = _initial_inbox.get('trusted_last_seen_event_id')
        self.untrusted_last_seen_event_id = self['untrusted_last_seen_event_id'] = _initial_inbox.get('untrusted_last_seen_event_id')

        if _initial_inbox.get("inbox_timelines"):
            for key, value in _initial_inbox['inbox_timelines'].items():
                new_thread = threading.Thread(target=self.get_more, args=(value,))
                _threads.append(new_thread)
                new_thread.start()

            for _ in _threads:
                _.join()

        self._parse_messages()
        return self, self.conversations

    def _parse_messages(self):
        for conv in self.conversations:
            for message in conv.messages:
                self.messages.append(message)

        self['conversations'] = self.conversations
        self['messages'] = self.messages

    def get_more(self, status):
        stage = status.get('status', self.AT_END_STATUS)
        min_entry_id = status.get('min_entry_id', 0)
        while stage != self.AT_END_STATUS:
            response = self._client.http.get_trusted_inbox(min_entry_id)
            inbox = self._parse_response(response)
            min_entry_id = inbox.get('min_entry_id', 0)
            stage = inbox.get('status', self.AT_END_STATUS)

    def get_conversation(self, conversation_id):
        for conv in self.conversations:
            if str(conv.id) == conversation_id:
                return conv

        return None

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.conversations[index]

    def __iter__(self):
        for __tweet in self.conversations:
            yield __tweet

    def __len__(self):
        return len(self.conversations)

    def __repr__(self):
        return f"Inbox(user_id={self.user_id}, count={self.__len__()})"


class Conversation(dict):
    HAS_MORE_STATUS = Inbox.HAS_MORE_STATUS
    AT_END_STATUS = Inbox.AT_END_STATUS
    TYPE_GROUP_DM = "GROUP_DM"

    def __init__(self, conversation, inbox, client, get_all_messages=False):
        super().__init__()
        self._inbox = inbox
        self._client = client
        self._raw = conversation
        self._get_all_messages = get_all_messages
        self.id = self['id'] = self._get_key("conversation_id")
        self.last_read_event_id = self['last_read_event_id'] = self._get_key("last_read_event_id")
        self.low_quality = self['low_quality'] = self._get_key("low_quality")
        self.max_entry_id = self['max_entry_id'] = self._get_key("max_entry_id")
        self.min_entry_id = self['min_entry_id'] = self._get_key("min_entry_id")
        self.muted = self['muted'] = self._get_key("muted")
        self.notifications_disabled = self['notifications_disabled'] = self._get_key("notifications_disabled")
        self.nsfw = self['nsfw'] = self._get_key("nsfw")
        self.read_only = self['read_only'] = self._get_key("read_only")
        self.trusted = self['trusted'] = self._get_key("trusted")
        self.type = self['type'] = self._get_key("type")
        self.participants = self['participants'] = self.get_participants()
        self.name = self['name'] = self._get_key("name", self._get_one_to_one_name())
        self.messages = self['messages'] = self.parse_messages()
        self.cursor = None
        self.conversation_status = self.HAS_MORE_STATUS

    def _get_one_to_one_name(self):
        for participant in self.participants:
            if isinstance(participant, User):
                if participant != self._client.me:
                    return participant.name
        return ""

    def get_participants(self):
        users = []
        participants = self._raw['participants']
        for participant in participants:
            try:
                user = self._inbox['users'].get(str(participant['user_id']))
                if user:
                    user['__typename'] = "User"
                    users.append(User(self._client, user))
            except Exception as e:
                users.append(str(participant['user_id']))

        return users

    def _get_key(self, keyName, default=None):
        return self._raw.get(keyName, default)

    def parse_messages(self):
        messages = []
        if not self._get_all_messages:
            for entry in self._inbox.get('entries', []):
                if entry.get('message'):
                    if str(entry['message']['conversation_id']) == str(self.id):
                        messages.append(Message(entry['message'], self._inbox, self._client))
        else:
            messages = self.get_all_messages()

        messages = sorted(messages, key=lambda x: x.time, reverse=True)
        return messages

    def get_page(self, cursor, till_date=None):
        messages = []
        response = self._client.http.get_conversation(self.id, cursor)
        conversation_status = response.get('conversation_timeline', {}).get('status', "AT_END")
        cursor = response.get('conversation_timeline', {}).get('min_entry_id', 0)
        for entry in response.get('conversation_timeline', {}).get('entries', []):
            if entry.get("message"):
                _message = Message(entry['message'], response['conversation_timeline'], self._client)

                if till_date and int(_message.time.timestamp()) <= int(till_date.timestamp()):
                    break

                messages.append(_message)

        return messages, conversation_status, cursor

    def get_next_page(self, till_date=None):
        messages, self.conversation_status, self.cursor = self.get_page(self.cursor, till_date=till_date)
        return messages

    def get_all_messages(self, wait_time=2, cursor=0, till_date=None, count=None):
        all_messages = []
        for _, messages in self.iter_all_messages(wait_time=wait_time, cursor=cursor, till_date=till_date, count=count):
            all_messages.extend(messages)
        return all_messages

    def iter_all_messages(self, wait_time=2, cursor=0, till_date=None, count=None):
        messages = []
        self.cursor = cursor if cursor != 0 else self.cursor
        while True:
            _page = self.get_next_page(till_date)

            actual_page = []
            for message in _page:
                if count and len(messages) == count:
                    break
                else:
                    messages.append(message)
                    actual_page.append(message)

            yield self, actual_page

            if self.conversation_status == self.AT_END_STATUS or (count and len(messages) >= count):
                break

            time.sleep(parse_wait_time(wait_time))
        return messages

    def send_message(self, text, file=None):
        return self._client.send_message(self.id, text=text, file=file, in_group=self.type == self.TYPE_GROUP_DM)

    def __eq__(self, other):
        if isinstance(other, Conversation):
            return str(self.id) == str(other.id)

        return str(self.id) == str(other)

    def __repr__(self):
        return "Conversation(id={}, muted={}, nsfw={}, participants={})".format(
            self.id, self.muted, self.nsfw, self.participants
        )


class Message(dict):
    def __init__(self, message, _inbox, client):
        super().__init__()
        self._raw = message
        self._inbox = _inbox
        self._client = client
        self._entities = self._get_message_data('entities', {})
        self.conversation_id = self['conversation_id'] = self._raw.get('conversation_id')
        self.id = self['id'] = self._raw.get('id')
        self.epoch_time = self['epoch_time'] = self._get_message_data('time')
        self.time = self['time'] = parse_time(self.epoch_time)
        self.request_id = self['request_id'] = self._raw.get('request_id')
        self.text = self['text'] = self._get_text()
        self.receiver = self['receiver'] = self.get_recipient('recipient_id')
        self.sender = self['sender'] = self.get_recipient('sender_id')
        self.media = self['media'] = self._get_media()
        self.urls = self['urls'] = self._get_urls()
        self.symbols = self['symbols'] = self._get_symbols()
        self.hashtags = self['hashtags'] = self._get_hashtags()
        self.user_mentions = self['user_mentions'] = self._get_user_mentions()

    def _get_urls(self):
        return [URL(self._client, i) for i in self._entities.get('urls', [])]

    def _get_hashtags(self):
        return [Hashtag(self._client, i) for i in self._entities.get('hashtags', [])]

    def _get_symbols(self):
        return [Symbol(self._client, i) for i in self._entities.get('symbols', [])]

    def _get_user_mentions(self):
        return [ShortUser(self._client, i) for i in self._entities.get('user_mentions', [])]

    def _get_message_data(self, dataKey, default=None):
        return self._raw['message_data'].get(dataKey, default)

    def get_recipient(self, target):
        user = self._get_message_data(target)
        if not user:
            return None

        user = self._inbox.get('users', {}).get(str(user))
        if user:
            user['__typename'] = "User"
            return User(self._client, user)

        return None

    def _get_text(self):
        text = self._get_message_data('text')

        if text:
            return re.sub(r"https://t\.co/\S+", "", text).strip()

        return ""

    def _get_media(self):
        media = None
        if self._get_message_data("attachment"):
            attachment = self._get_message_data("attachment")
            if "photo" in list(attachment.keys()):
                media = attachment.get('photo')

            if "video" in list(attachment.keys()):
                media = attachment.get('video')

            if "animated_gif" in list(attachment.keys()):
                media = attachment.get('animated_gif')

            if media:
                return Media(self._client, media)

        return None

    def __eq__(self, other):
        if isinstance(other, Message):
            return str(self.id) == str(other.id) and str(self.conversation_id) == str(other.conversation_id)

        return str(self.id) == str(other.id)

    def __repr__(self):
        return "Message(id={}, conversation_id={}, time={})".format(
            self.id, self.conversation_id, self.time
        )


class SendMessage:
    def __init__(self, client, conversation_id, text, file=None):
        self._conv = conversation_id
        self._text = text
        self._client = client
        self._file = file

    def send(self):
        response = self._client.http.send_message(self._conv, self._text, self._file)
        return Message(response['entries'][0]['message'], response, self._client)
