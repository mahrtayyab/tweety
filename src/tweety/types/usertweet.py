import sys
import traceback
from .twDataTypes import SelfThread, ConversationThread
from ..exceptions_ import UserProtected, UserNotFound
from ..utils import find_objects
from . import Tweet, Excel, deprecated
from .base import BaseGeneratorClass


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

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:

            response = self.client.http.get_tweets(self.user_id, replies=self.get_replies, cursor=self.cursor)

            if not response['data']['user'].get("result"):
                raise UserNotFound(response=response)

            if response['data']['user']['result']['__typename'] == "UserUnavailable":
                raise UserProtected(403, "UserUnavailable", response)

            entries = self._get_entries(response)

            for entry in entries:
                object_type = self._get_target_object(entry)

                try:
                    if object_type is None:
                        continue

                    parsed = object_type(entry, self.client, None)
                    _tweets.append(parsed)
                except:
                    pass
            self.is_next_page = self._get_cursor(response)
            self._get_cursor_top(response)

            for tweet in _tweets:
                self.tweets.append(tweet)

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

                    parsed = object_type(entry, self.client, None)
                    _tweets.append(parsed)
                except:
                    pass

            self.is_next_page = self._get_cursor(response)

            for tweet in _tweets:
                self.tweets.append(tweet)

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
                        parsed = object_type(self.parent, entry, self.client)
                        _comments.append(parsed)
                except:
                    pass

            self.is_next_page = self._get_cursor(response)

            for comment in _comments:
                self.tweets.append(comment)

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