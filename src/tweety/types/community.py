from .twDataTypes import SelfThread, Tweet, Excel, User, Community
from .base import BaseGeneratorClass
from ..utils import find_objects


class UserCommunities(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "community": Community
    }
    _RESULT_ATTR = "communities"

    def __init__(self, client, user_id):
        super().__init__()
        self.communities = []
        self.cursor = None
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = 1
        self.wait_time = None

    @staticmethod
    def _get_users(response):
        all_users = find_objects(response, "__typename", "User", none_value=[])
        return all_users

    def get_page(self, cursor=None):
        _communities = []
        response = self.client.http.get_user_communities(self.user_id)
        entries = self._get_entries(response)

        for entry in entries:
            try:
                parsed = Community(self.client, entry, None)
                if parsed:
                    _communities.append(parsed)
            except:
                pass

        cursor = find_objects(response, "next_cursor", value=None)
        cursor_top = self._get_cursor_(response, "Top")

        return _communities, cursor, cursor_top

    def __repr__(self):
        return "UserCommunities(user_id={}, count={})".format(
            self.user_id, self.__len__()
        )


class CommunityTweets(BaseGeneratorClass):
    OBJECTS_TYPES = {
        "tweet": Tweet,
        "homeConversation": SelfThread,
        "profile": SelfThread
    }
    _RESULT_ATTR = "tweets"

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

    def get_page(self, cursor):
        _tweets = []
        response = self.client.http.get_community_tweets(self.community_id, self.filter, cursor=cursor)

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

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _tweets, cursor, cursor_top

    def to_xlsx(self, filename=None):
        return Excel(self, filename)

    def __repr__(self):
        return "CommunityTweets(id={}, count={})".format(
            self.community_id, self.__len__()
        )


class CommunityMembers(BaseGeneratorClass):
    _RESULT_ATTR = "users"

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

    def get_page(self, cursor):
        _users = []
        response = self.client.http.get_community_members(self.community_id, self.filter, cursor=cursor)

        response_users = self._get_users(response)

        for response_user in response_users:
            try:
                parsed = User(self.client, response_user, None)
                if parsed:
                    _users.append(parsed)
            except:
                pass

        cursor = find_objects(response, "next_cursor", value=None)
        cursor_top = self._get_cursor_(response, "Top")

        return _users, cursor, cursor_top

    def __repr__(self):
        return "CommunityMembers(id={}, count={})".format(
            self.community_id, self.__len__()
        )
