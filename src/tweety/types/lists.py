from . import User, List, Tweet, SelfThread
from .base import BaseGeneratorClass
from ..utils import find_objects


class Lists(BaseGeneratorClass):
    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.lists = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    @staticmethod
    def _get_user_owned_lists(entries):
        for entry in entries:
            entry_type = str(entry['entryId']).split("-")[0]
            if entry_type == "owned":
                return entry

        return {}

    def get_next_page(self):
        _lists = []
        if self.is_next_page:
            response = self.client.http.get_lists(cursor=self.cursor)
            entries = self._get_entries(response)
            item = self._get_user_owned_lists(entries)
            lists = find_objects(item, "__typename", "TimelineTwitterList", none_value=[])

            for item in lists:
                try:
                    parsed = List(self.client, item)
                    if parsed:
                        _lists.append(parsed)
                except:
                    pass

            self.is_next_page = self._get_cursor(response)
            self.lists.extend(_lists)

            self['tweets'] = self.lists
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

        return _lists

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.lists[index]

    def __iter__(self):
        for __list in self.lists:
            yield __list

    def __len__(self):
        return len(self.lists)


class ListTweets(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread,
        "list": SelfThread,
    }

    def __init__(self, list_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.list_id = list_id
        self.pages = pages
        self.wait_time = wait_time

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:
            response = self.client.http.get_list_tweets(self.list_id, cursor=self.cursor)
            entries = self._get_entries(response)

            for entry in entries:
                object_type = self._get_target_object(entry)

                try:
                    if object_type is None:
                        continue

                    parsed = object_type(self.client, entry, None)
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

    def __repr__(self):
        return "ListTweets(id={}, count={})".format(
            self.list_id, self.__len__()
        )


class ListMembers(BaseGeneratorClass):

    def __init__(self, list_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.users = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.list_id = list_id
        self.pages = pages
        self.wait_time = wait_time

    @staticmethod
    def _get_users(response):
        all_users = find_objects(response, "__typename", "User", none_value=[])
        return all_users

    def get_next_page(self):
        _users = []
        if self.is_next_page:
            response = self.client.http.get_list_members(self.list_id, cursor=self.cursor)

            response_users = self._get_users(response)

            for response_user in response_users:
                try:
                    parsed = User(self.client, response_user, None)
                    if parsed:
                        _users.append(parsed)
                except:
                    pass
            self.is_next_page = self._get_cursor(response)
            self._get_cursor_top(response)
            self.users.extend(_users)

            self['users'] = self.users
            self['is_next_page'] = self.is_next_page
            self['cursor'] = self.cursor

        return _users

    def __getitem__(self, index):
        if isinstance(index, str):
            return getattr(self, index)

        return self.users[index]

    def __iter__(self):
        for __user in self.users:
            yield __user

    def __len__(self):
        return len(self.users)

    def __repr__(self):
        return "ListMembers(id={}, count={})".format(
            self.list_id, self.__len__()
        )
