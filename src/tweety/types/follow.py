from .twDataTypes import User
from .base import BaseGeneratorClass


class UserFollowers(BaseGeneratorClass):
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

    def get_next_page(self):
        _users = []
        if self.is_next_page:
            response = self.client.http.get_user_followers(self.user_id, cursor=self.cursor)

            entries = self._get_entries(response)

            for entry in entries:
                try:

                    parsed = User(self.client, entry, None)
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


class UserFollowings(BaseGeneratorClass):
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

    def get_next_page(self):
        _users = []
        if self.is_next_page:
            response = self.client.http.get_user_followings(self.user_id, cursor=self.cursor)

            entries = self._get_entries(response)

            for entry in entries:
                try:

                    parsed = User(self.client, entry, None)
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
