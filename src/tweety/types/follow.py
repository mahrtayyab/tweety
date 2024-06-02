from .twDataTypes import User
from .base import BaseGeneratorClass


class UserFollowers(BaseGeneratorClass):
    _RESULT_ATTR = "users"

    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.users = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def get_page(self, cursor):
        _users = []
        response = self.client.http.get_user_followers(self.user_id, cursor=cursor)

        entries = self._get_entries(response)

        for entry in entries:
            try:

                parsed = User(self.client, entry, None)
                if parsed:
                    _users.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _users, cursor, cursor_top


class UserFollowings(BaseGeneratorClass):
    _RESULT_ATTR = "users"

    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.users = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def get_page(self, cursor):
        _users = []
        response = self.client.http.get_user_followings(self.user_id, cursor=cursor)

        entries = self._get_entries(response)

        for entry in entries:
            try:

                parsed = User(self.client, entry, None)
                if parsed:
                    _users.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _users, cursor, cursor_top


class UserSubscribers(BaseGeneratorClass):
    _RESULT_ATTR = "users"

    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.users = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def get_page(self, cursor):
        _users = []
        response = self.client.http.get_user_subscribers(self.user_id, cursor=cursor)

        entries = self._get_entries(response)

        for entry in entries:
            try:

                parsed = User(self.client, entry, None)
                if parsed:
                    _users.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _users, cursor, cursor_top


class MutualFollowers(BaseGeneratorClass):
    _RESULT_ATTR = "users"

    def __init__(self, user_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.users = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.user_id = user_id
        self.pages = pages
        self.wait_time = wait_time

    def get_page(self, cursor):
        _users = []
        response = self.client.http.get_mutual_friends(self.user_id, cursor=cursor)

        entries = self._get_entries(response)

        for entry in entries:
            try:

                parsed = User(self.client, entry, None)
                if parsed:
                    _users.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _users, cursor, cursor_top


class BlockedUsers(BaseGeneratorClass):
    _RESULT_ATTR = "users"

    def __init__(self, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.users = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.pages = pages
        self.user_id = self.client.me.id
        self.wait_time = wait_time

    def get_page(self, cursor):
        _users = []
        response = self.client.http.get_blocked_users(cursor=cursor)

        entries = self._get_entries(response)

        for entry in entries:
            try:

                parsed = User(self.client, entry, None)
                if parsed:
                    _users.append(parsed)
            except:
                pass

        cursor = self._get_cursor_(response)
        cursor_top = self._get_cursor_(response, "Top")

        return _users, cursor, cursor_top
