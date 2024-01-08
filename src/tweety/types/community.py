from . import SelfThread, Tweet, Excel, User
from .base import BaseGeneratorClass
from ..utils import find_objects


class CommunityTweets(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread
    }

    def __init__(self, community_id, client, pages=1, filter_=None, wait_time=2, cursor=None):
        super().__init__()
        self.tweets = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.filter = filter_
        self.client = client
        self.community_id = community_id
        self.pages = pages
        self.wait_time = wait_time

    def _get_target_object(self, tweet):
        entry_type = str(tweet['entryId']).split("-")[0]
        return self.OBJECTS_TYPES.get(entry_type)

    def get_next_page(self):
        _tweets = []
        if self.is_next_page:
            response = self.client.http.get_community_tweets(self.community_id, self.filter, cursor=self.cursor)

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

    def __repr__(self):
        return "CommunityTweets(id={}, count={})".format(
            self.community_id, self.__len__()
        )


class CommunityMembers(BaseGeneratorClass):

    def __init__(self, community_id, client, pages=1, filter_=None, wait_time=2, cursor=None):
        super().__init__()
        self.users = []
        self.cursor = cursor
        self.is_next_page = True
        self.filter = filter_
        self.client = client
        self.community_id = community_id
        self.pages = pages
        self.wait_time = wait_time

    @staticmethod
    def _get_users(response):
        all_users = find_objects(response, "__typename", "User", none_value=[])
        return all_users

    def _get_cursor(self, response):
        newCursor = find_objects(response, "next_cursor", value=None)

        if not newCursor or newCursor == self.cursor:
            return False

        self.cursor = newCursor
        return True

    def get_next_page(self):
        _users = []
        if self.is_next_page:
            response = self.client.http.get_community_members(self.community_id, self.filter, cursor=self.cursor)

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
        return "CommunityMembers(id={}, count={})".format(
            self.community_id, self.__len__()
        )
