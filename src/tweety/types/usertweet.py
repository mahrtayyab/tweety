import sys
import traceback
from .twDataTypes import SelfThread
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
                raise UserNotFound(error_code=50, error_name="GenericUserNotFound", response=response)

            if response['data']['user']['result']['__typename'] == "UserUnavailable":
                raise UserProtected(403, "UserUnavailable", None)

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
