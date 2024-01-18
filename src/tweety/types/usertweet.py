from .twDataTypes import SelfThread, ConversationThread
from ..exceptions_ import UserProtected, UserNotFound
from . import Tweet, Excel
from .base import BaseGeneratorClass, find_objects


class UserTweets(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread
    }

    def __init__(self, user_id, client, pages=1, get_replies: bool = True, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.get_replies = get_replies
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time
        self.pinned = None

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    def _get_pinned_tweet(self, response):
        pinned = find_objects(response, "type", "TimelinePinEntry", recursive=False, none_value={})
        pinned_tweet = Tweet(self.client, pinned, None)
        return pinned_tweet

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:

            response = self.client.http.get_tweets(self.user_id, replies=self.get_replies, cursor=self.cursor)

            if not response['data']['user'].get("result"):
                raise UserNotFound(response=response)

            if response['data']['user']['result']['__typename'] == "UserUnavailable":
                raise UserProtected(403, "UserUnavailable", response)

            entries = self._get_entries(response)
            if not self.pinned:
                self.pinned = self._get_pinned_tweet(response)

            for entry in entries:
                object_type = self._get_target_object(entry)

                try:
                    if object_type is None:
                        continue

                    parsed = object_type(self.client, entry, None)
                    if parsed:
                        _tweets.append(parsed)
                except:
                    pass

            self.is_next_page = self._get_cursor(response)
            self._get_cursor_top(response)
            self.tweets.extend(_tweets)

            self['tweets'] = self.tweets
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

        return _tweets

    def to_xlsx(self, filename=None):
        return Excel(self, filename)

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)


class UserMedia(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": Tweet
    }

    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:

            response = self.client.http.get_medias(self.user_id, cursor=self.cursor)
            if not response['data']['user'].get("result"):
                raise UserNotFound(response=response)

            if response['data']['user']['result']['__typename'] == "UserUnavailable":
                raise UserProtected(403, "UserUnavailable", response)

            entries = self._get_entries(response)
            _entry_ = [i for i in entries if "profile-grid" in i.get('entryId', '')]

            if _entry_:
                _entry_ = _entry_[0]
                entries = find_objects(_entry_, "items", None, recursive=False, none_value=[])
            else:
                entries = []

            for entry in entries:
                object_type = self._get_target_object(entry)

                try:
                    if object_type is None:
                        continue

                    parsed = object_type(self.client, entry, None)
                    if parsed:
                        _tweets.append(parsed)
                except:
                    pass

            self.is_next_page = self._get_cursor(response)
            self._get_cursor_top(response)
            self.tweets.extend(_tweets)

            self['tweets'] = self.tweets
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

        return _tweets

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)


class SelfTimeline(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread
    }

    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:
            response = self.client.http.get_home_timeline(cursor=self.cursor)

            entries = self._get_entries(response)

            for entry in entries:
                object_type = self._get_target_object(entry)

                try:
                    if object_type is None:
                        continue

                    parsed = object_type(self.client, entry, None)
                    if parsed:
                        _tweets.append(parsed)
                except:
                    pass

            self.is_next_page = self._get_cursor(response)
            self.tweets.extend(_tweets)

            self['tweets'] = self.tweets
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

        return _tweets

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)


class TweetComments(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "conversationthread": ConversationThread,
    }

    def __init__(self, tweet_id, client, get_hidden=False, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.is_next_page = True
        self.get_hidden = get_hidden
        self.client = client
        self.tweet_id = tweet_id
        self.pages = pages
        self.wait_time = wait_time
        self.parent = self._get_parent()

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    def _get_parent(self):
        return self.tweet_id if isinstance(self.tweet_id, Tweet) else self.client.tweet_detail(self.tweet_id)

    def get_next_page(self):
        _comments = []
        if self.is_next_page:
            response = self.client.http.get_tweet_detail(self.tweet_id, self.cursor)

            entries = self._get_entries(response)

            for entry in entries:
                object_type = self._get_target_object(entry)

                try:
                    if object_type is None:
                        continue

                    entry = [i for i in entry['content']['items']]
                    if len(entry) > 0:
                        parsed = object_type(self.client, self.parent, entry)
                        _comments.append(parsed)
                except:
                    pass

            self.is_next_page = self._get_cursor(response)
            self.tweets.extend(_comments)

            self['tweets'] = self.tweets
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

        return _comments

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)

    def __repr__(self):
        return "TweetComments(tweet_id={}, count={}, parent={})".format(
            self.tweet_id,
            len(self.tweets), self.parent
        )


class TweetHistory(BaseGeneratorClass):
    LATEST_TWEET_ENTRY_ID = "latestTweet"

    def __init__(self, tweet_id, client):
        super().__init__()
        self.client = client
        self._tweet_id = tweet_id
        self.latest = None
        self.tweets = self['tweets'] = self._get_history()

    def _get_history(self):
        results = []
        response = self.client.http.get_tweet_edit_history(self._tweet_id)
        entries = find_objects(response, "type", "TimelineAddEntries", recursive=False, none_value={})
        entries = entries.get('entries', [])
        if not entries:
            _tweet = self.client.tweet_detail(self._tweet_id)
            self.latest = self['latest'] = _tweet
            results.append(_tweet)
        else:
            for entry in entries:
                _tweet = Tweet(self.client, entry, None)

                if entry['entryId'] == self.LATEST_TWEET_ENTRY_ID:
                    self.latest = self['latest'] = _tweet

                results.append(_tweet)
        return results

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.tweets[index]

    def __iter__(self):
        for __tweet in self.tweets:
            yield __tweet

    def __len__(self):
        return len(self.tweets)

    def __repr__(self):
        return "TweetHistory(tweets={}, author={})".format(
            len(self.tweets), self.tweets[0].author
        )

