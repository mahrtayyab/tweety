from .twDataTypes import User, List, Tweet, SelfThread
from .base import BaseGeneratorClass
from ..utils import find_objects


class Lists(BaseGeneratorClass):
    _RESULT_ATTR = "lists"

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

    def get_page(self, cursor):
        _lists = []
        response = self.client.http.get_lists(cursor=cursor)
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

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _lists, cursor, cursor_top


class ListTweets(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread,
        "list": SelfThread,
    }
    _RESULT_ATTR = "tweets"

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

    def get_page(self, cursor):
        _tweets = []
        response = self.client.http.get_list_tweets(self.list_id, cursor=cursor)
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

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _tweets, cursor, cursor_top

    def __repr__(self):
        return "ListTweets(id={}, count={})".format(
            self.list_id, self.__len__()
        )


class ListMembers(BaseGeneratorClass):
    _RESULT_ATTR = "users"

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

    def get_page(self, cursor):
        _users = []
        response = self.client.http.get_list_members(self.list_id, cursor=cursor)

        response_users = self._get_users(response)

        for response_user in response_users:
            try:
                parsed = User(self.client, response_user, None)
                if parsed:
                    _users.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _users, cursor, cursor_top

    def __repr__(self):
        return "ListMembers(id={}, count={})".format(
            self.list_id, self.__len__()
        )
