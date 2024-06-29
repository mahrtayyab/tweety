import re
import time
from .twDataTypes import User, Media, URL, Hashtag, ShortUser, Symbol, Tweet
from ..constants import INBOX_PAGE_TYPES, INBOX_PAGE_TYPE_UNTRUSTED, INBOX_PAGE_TYPE_TRUSTED
from ..utils import parse_time, parse_wait_time, get_next_index
from ..exceptions import TwitterError


class Inbox(dict):
    HAS_MORE_STATUS = "HAS_MORE"
    AT_END_STATUS = "AT_END"

    def __init__(self, user_id, client, pages, wait_time=2, page_types=INBOX_PAGE_TYPES):
        _page_types = [page_types] if not isinstance(page_types, (list, tuple)) else page_types
        super().__init__()
        self._client = client
        self._got_initial = False
        self._inbox_timelines = {}
        self._retries = 2
        self._types = [i for i in _page_types if i in INBOX_PAGE_TYPES]
        self.pages = pages
        self.wait_time = wait_time
        self.conversations = []
        self.messages = []
        self.cursor = None
        self.last_seen_event_id = None
        self.trusted_last_seen_event_id = None
        self.untrusted_last_seen_event_id = None
        self.user_id = user_id

    def _parse_response(self, response):
        this_page = []
        _initial_inbox = response.get('inbox_initial_state') or response.get('user_events') or response.get('inbox_timeline')
        _conversations = _initial_inbox.get("conversations", {})

        for conservation in _conversations.values():
            _conversation = Conversation(conservation, _initial_inbox, self._client)
            this_page.append(_conversation)

            to_edit = None

            for conv_index, pre_conv in enumerate(self.conversations):
                if str(pre_conv.id) == str(_conversation.id):
                    to_edit = conv_index
                    break

            if to_edit:
                self.conversations.insert(to_edit, _conversation)
            else:
                self.conversations.append(_conversation)

        self._parse_messages(this_page)
        return this_page, _initial_inbox

    def get_page(self, min_entry_id=None, page_type=INBOX_PAGE_TYPE_TRUSTED):
        if not self._got_initial:
            if not self.cursor:
                response = self._client.http.get_initial_inbox()
            else:
                response = self._client.http.get_inbox_updates(cursor=self.cursor)

            page, inbox = self._parse_response(response)
            self.cursor = self['cursor'] = inbox.get('cursor')
            self.last_seen_event_id = self['last_seen_event_id'] = inbox.get('last_seen_event_id')
            self.trusted_last_seen_event_id = self['trusted_last_seen_event_id'] = inbox.get('trusted_last_seen_event_id')
            self.untrusted_last_seen_event_id = self['untrusted_last_seen_event_id'] = inbox.get('untrusted_last_seen_event_id')

            if inbox.get("inbox_timelines"):
                self._inbox_timelines = inbox.get("inbox_timelines", {})

            self._got_initial = True
            return page, self.cursor, None
        else:
            if page_type not in INBOX_PAGE_TYPES:
                page_type = INBOX_PAGE_TYPE_TRUSTED

            if not min_entry_id:
                raise ValueError("'min_entry_id' is required after initial request.")

            response = None

            for _ in range(self._retries):
                try:
                    if page_type == INBOX_PAGE_TYPE_UNTRUSTED:
                        response = self._client.http.get_untrusted_inbox(min_entry_id)
                    else:
                        response = self._client.http.get_trusted_inbox(min_entry_id)
                except TwitterError as inbox_fetch_error:
                    pass

            if response:
                page, inbox = self._parse_response(response)
            else:
                page, inbox = [], {}

            return page, inbox.get('min_entry_id', 0), inbox.get('status', self.AT_END_STATUS)

    def get_new_messages(self, cursor=None):
        if not cursor:
            cursor = self.cursor

        response = self._client.http.get_inbox_updates(cursor=cursor)
        page, inbox = self._parse_response(response)
        self.cursor = self['cursor'] = inbox.get('cursor')
        self.last_seen_event_id = self['last_seen_event_id'] = inbox.get('last_seen_event_id')
        self.trusted_last_seen_event_id = self['trusted_last_seen_event_id'] = inbox.get('trusted_last_seen_event_id')
        self.untrusted_last_seen_event_id = self['untrusted_last_seen_event_id'] = inbox.get('untrusted_last_seen_event_id')

        if inbox.get("inbox_timelines"):
            self._inbox_timelines = inbox.get("inbox_timelines", {})

        return page

    def get_next_page(self, page_type=None):
        if not self._got_initial:
            page, cursor, _ = self.get_page()
            self.cursor = self['cursor'] = cursor
            return page
        else:
            if not page_type or page_type not in INBOX_PAGE_TYPES:
                page_type = INBOX_PAGE_TYPE_TRUSTED

            if self._inbox_timelines[page_type]['status'] == self.AT_END_STATUS:
                page_type = INBOX_PAGE_TYPE_UNTRUSTED

            page_attrs = self._inbox_timelines.get(page_type, {})

            min_entry_id = page_attrs.get('min_entry_id', 0)
            status = page_attrs.get('status', self.AT_END_STATUS)

            if status == self.AT_END_STATUS:
                return []

            page, new_min_entry_id, new_status = self.get_page(min_entry_id=min_entry_id, page_type=page_type)
            self._inbox_timelines[page_type]["min_entry_id"] = new_min_entry_id
            self._inbox_timelines[page_type]["status"] = new_status
            return page

    def generator(self):
        this_page = 0
        page_type_index = 0
        page_type = self._types[page_type_index]

        while this_page != int(self.pages):
            results = self.get_next_page(page_type)

            if len(results) == 0:
                page_type_index = get_next_index(self._types, page_type_index)

                if not page_type_index:
                    break

                page_type = self._types[page_type_index]

            yield self, results
            this_page += 1

            if this_page != self.pages:
                time.sleep(parse_wait_time(self.wait_time))

        return self

    def _parse_messages(self, conversations):
        for conv in conversations:
            for message in conv.messages:
                self.messages.append(message)

        self['conversations'] = self.conversations
        self['messages'] = self.messages

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
        for _conversation_ in self.conversations:
            yield _conversation_

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
        self.admin = None
        self.id = self['id'] = self._get_key("conversation_id")
        self.last_read_event_id = self['last_read_event_id'] = self._get_key("last_read_event_id")
        self.low_quality = self['low_quality'] = self._get_key("low_quality")
        self.max_entry_id = self['max_entry_id'] = self._get_key("max_entry_id")
        self.min_entry_id = self['min_entry_id'] = self._get_key("min_entry_id")
        self.muted = self['muted'] = self._get_key("muted")
        self.notifications_disabled = self['notifications_disabled'] = self._get_key("notifications_disabled")
        self.nsfw = self['nsfw'] = self._get_key("nsfw")
        self.avatar_url = self['avatar_image_https'] = self._get_key("avatar_image_https")  # only for Group
        self.created_at = self['create_time'] = parse_time(self._get_key("create_time"))  # only for Group
        self.created_by_user_id = self['created_by_user_id'] = self._get_key("created_by_user_id")  # only for Group
        self.read_only = self['read_only'] = self._get_key("read_only")
        self.trusted = self['trusted'] = self._get_key("trusted")
        self.type = self['type'] = self._get_key("type")
        self.participants = self['participants'] = self.get_participants()
        self.name = self['name'] = self._get_key("name", self._get_one_to_one_name())
        self.messages = self['messages'] = self.parse_messages()
        self.is_group = self.type == self.TYPE_GROUP_DM
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
                    this_user = User(self._client, user)
                else:
                    this_user = str(participant["user_id"])
            except Exception as e:
                this_user = str(participant["user_id"])

            if participant.get("is_admin") is True:
                self.admin = this_user

            users.append(this_user)

        return users

    def _get_key(self, keyName, default=None):
        return self._raw.get(keyName, default)

    def _parse_message(self, entry):
        if entry.get('message') and str(entry['message']['conversation_id']) == str(self.id):
            return Message(entry['message'], self._inbox, self._client)
        elif entry.get('welcome_message_create') and str(entry['welcome_message_create']['conversation_id']) == str(self.id):
            return Message(entry['welcome_message_create'], self._inbox, self._client)
        elif entry.get('participants_join') and str(entry['participants_join']['conversation_id']) == str(self.id):
            return MessageParticipantUpdate(
                'participants_join',
                entry.get('participants_join'),
                self._inbox,
                self._client
            )
        elif entry.get('join_conversation') and str(entry['join_conversation']['conversation_id']) == str(self.id):
            return MessageParticipantUpdate(
                'participants_join',
                entry.get('join_conversation'),
                self._inbox,
                self._client
            )
        elif entry.get('participants_leave') and str(entry['participants_leave']['conversation_id']) == str(self.id):
            return MessageParticipantUpdate(
                'participants_leave',
                entry.get('participants_leave'),
                self._inbox,
                self._client
            )
        elif entry.get('conversation_name_update') and str(entry['conversation_name_update']['conversation_id']) == str(self.id):
            return MessageNameUpdate(entry['conversation_name_update'], self._inbox, self._client)
        elif entry.get('conversation_create') and str(entry['conversation_create']['conversation_id']) == str(self.id):
            return MessageConversationCreated(entry['conversation_create'], self._inbox, self._client)
        elif entry.get('conversation_avatar_update') and str(entry['conversation_avatar_update']['conversation_id']) == str(self.id):
            return MessageConversationAvatarUpdate(entry["conversation_avatar_update"], self._inbox, self._client)

        return None

    def parse_messages(self):
        messages = []
        if not self._get_all_messages:
            for entry in self._inbox.get('entries', []):
                _message = self._parse_message(entry)
                if _message:
                    messages.append(_message)
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
            _message = self._parse_message(entry)

            if _message:
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

    def send_message(self, text, file=None, reply_to_message_id=None, audio_only=False, quote_tweet_id=None):
        return self._client.send_message(self.id, text=text, file=file, in_group=self.type == self.TYPE_GROUP_DM, reply_to_message_id=reply_to_message_id, audio_only=audio_only, quote_tweet_id=quote_tweet_id)

    def __eq__(self, other):
        if isinstance(other, Conversation):
            return str(self.id) == str(other.id)

        return str(self.id) == str(other)

    def __repr__(self):
        return "Conversation(id={}, muted={}, nsfw={}, participants={})".format(
            self.id, self.muted, self.nsfw, self.participants
        )


class MessageParticipantUpdate(dict):
    def __init__(self, update_type, update, _inbox, client):
        super().__init__()
        self._update_type = update_type
        self._raw = update
        self._inbox = _inbox
        self._client = client
        self.id = self['id'] = self._raw['id']
        self.time = self['time'] = parse_time(self._raw.get('time'))
        self.participants = self['participants'] = self.get_recipients()
        self.type = self._update_type.replace("participants_", "").upper()
        self.sender_id = self['sender_id'] = self._raw.get('sender_id')
        self.sender = self['sender'] = self._get_sender()
        self.receiver = None

    def _get_sender(self):
        if self.type != "JOIN":
            return None

        this_user = self._inbox.get('users', {}).get(str(self.sender_id))
        if not this_user:
            return None

        this_user['__typename'] = "User"
        return User(self._client, this_user)

    def get_recipients(self):
        participants = []
        users = self._raw.get('participants', [])
        for user in users:
            this_user = self._inbox.get('users', {}).get(str(user['user_id']))

            if this_user:
                this_user['__typename'] = "User"
                participants.append(User(self._client, this_user))
            else:
                participants.append(str(user['user_id']))

        return participants

    def __repr__(self):
        return "MessageParticipantUpdate(id={}, type={}, time={}, participants={})".format(
            self.id, self.type, self.time, self.participants
        )


class MessageNameUpdate(dict):
    def __init__(self, update, _inbox, client):
        super().__init__()
        self._raw = update
        self._inbox = _inbox
        self._client = client
        self.id = self['id'] = self._raw['id']
        self.time = self['time'] = parse_time(self._raw.get('time'))
        self.name = self['name'] = self._raw['conversation_name']
        self.by_user_id = self['by_user_id'] = self._raw.get('by_user_id')
        self.by_user = self['by_user'] = self._get_by_user()
        self.receiver = None

    def _get_by_user(self):
        if not self.by_user_id:
            return None

        this_user = self._inbox.get('users', {}).get(str(self.by_user_id))
        if not this_user:
            return None

        this_user['__typename'] = "User"
        return User(self._client, this_user)

    def __repr__(self):
        return "MessageNameUpdate(id={}, time={}, name={}, by_user={})".format(
            self.id, self.time, self.name, self.by_user
        )


class MessageConversationCreated(dict):
    def __init__(self, update, _inbox, client):
        super().__init__()
        self._raw = update
        self._inbox = _inbox
        self._client = client
        self.id = self['id'] = self._raw['id']
        self.time = self['time'] = parse_time(self._raw.get('time'))

    def __repr__(self):
        return "MessageConversationCreated(id={}, time={})".format(
            self.id, self.time
        )


class MessageConversationAvatarUpdate(dict):
    def __init__(self, update, _inbox, client):
        super().__init__()
        self._raw = update
        self._inbox = _inbox
        self._client = client
        self.by_user_id = self["by_user_id"] = self._raw.get("by_user_id")
        self.id = self['id'] = self._raw['id']
        self.time = self['time'] = parse_time(self._raw.get('time'))
        self.conversation_id = self["conversation_id"] = self._raw.get("conversation_id")
        self.avatar_url = self["avatar_url"] = self._raw.get("conversation_avatar_image_https")

    def __repr__(self):
        return "MessageConversationAvatarUpdate(id={}, by_user_id={})".format(
            self.id, self.by_user_id
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
        self.receiver_id = self._client.user.id
        self.sender_id = self._get_message_data("sender_id")
        self.receiver = self['receiver'] = self._client.user
        self.sender = self['sender'] = self.get_recipient("sender_id")
        self.media = self['media'] = self._get_media()
        self.urls = self['urls'] = self._get_urls()
        self.symbols = self['symbols'] = self._get_symbols()
        self.hashtags = self['hashtags'] = self._get_hashtags()
        self.user_mentions = self['user_mentions'] = self._get_user_mentions()
        self.shared_tweet = self._get_shared_tweet()
        self.reply_to = self._get_reply_to()

    def _get_urls(self):
        return [URL(self._client, i) for i in self._entities.get('urls', [])]

    def _get_hashtags(self):
        return [Hashtag(self._client, i) for i in self._entities.get('hashtags', [])]

    def _get_symbols(self):
        return [Symbol(self._client, i) for i in self._entities.get('symbols', [])]

    def _get_user_mentions(self):
        return [ShortUser(self._client, i) for i in self._entities.get('user_mentions', [])]

    def _get_message_data(self, dataKey, default=None):
        message_data = self._raw.get("message_data")

        if not message_data:
            message_data = self._raw

        return message_data.get(dataKey, default)

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

    def _get_reply_to(self):
        reply_data = self._get_message_data("reply_data")
        if not reply_data:
            return None

        return Message(reply_data, self._raw, self._client)

    def _get_shared_tweet(self):
        attachment = self._get_message_data("attachment")

        if not attachment:
            return None

        this_tweet = attachment.get("tweet", {})
        this_status = this_tweet.get("status", {})
        this_user = this_status.get("user")
        rest_id = this_tweet.get("id")

        if not this_tweet:
            return None

        this_status["__typename"] = "Tweet"
        this_user["__typename"] = "User"
        this_status["core"] = this_user
        this_status["rest_id"] = rest_id

        return Tweet(self._client, this_status)

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
    def __init__(self, client, conversation_id, text, file=None, reply_to_message_id=None, audio_only=False, quote_tweet_id=None):
        self._conv = conversation_id
        self._text = text
        self._client = client
        self._file = file
        self._audio_only = audio_only
        self._reply_to_message_id = reply_to_message_id
        self._quote_tweet_id = quote_tweet_id

    def send(self):
        response = self._client.http.send_message(self._conv, self._text, self._file, self._reply_to_message_id, self._audio_only, self._quote_tweet_id)
        messages = [Message(i["message"], response, self._client) for i in response.get("entries", [])]
        return messages[0] if len(messages) == 1 else messages
