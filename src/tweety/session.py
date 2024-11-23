import json
import os.path
from .utils import dict_to_string

class Session:
    def __init__(self, client):
        self._client = client
        self.user = None
        self.logged_in = False
        self.cookies = {}

    def cookies_dict(self):

        if isinstance(self.cookies, dict):
            return self.cookies

        result = {}
        split = str(self.cookies).split(";")
        for i in split:
            try:
                key, value = i.split("=")
                result[key] = value
            except:
                pass

        return result

    async def save_session(self, cookies, user):
        self.logged_in = True

        if hasattr(cookies, "to_dict"):
            cookies = cookies.to_dict()

        self.cookies = cookies or self.cookies
        self.user = user or self.user

    def __str__(self):
        if isinstance(self.cookies, dict):
            return dict_to_string(self.cookies)
        return str(self.cookies)


class MemorySession(Session):

    def __init__(self):
        super().__init__(None)

    def __call__(self, client):
        self._client = client
        return self

    async def save_session(self, cookies, user):
        self.logged_in = True

        if hasattr(cookies, "to_dict"):
            cookies = cookies.to_dict()

        self.cookies = cookies or self.cookies
        self.user = user or self.user


class FileSession(Session):
    def __init__(self, client, session_name):
        super().__init__(client)
        self.session_name = os.path.basename(session_name)
        self.session_file_path = self._get_session_file_path(session_name, self.session_name)
        self._load_session()

    @staticmethod
    def _get_session_file_path(session_path, session_name):
        _session = session_name.replace(".tw_session", "")
        directory = os.path.dirname(session_path) or os.getcwd()
        return os.path.abspath(os.path.join(directory, f"{_session}.tw_session"))

    async def save_session(self, cookies, user):
        await super().save_session(cookies, user)
        session_data = {"cookies": self.cookies, "user": self.user}

        with open(self.session_file_path, "w") as f:
            json.dump(session_data, f, default=str)

    def _load_session(self):
        if os.path.exists(self.session_file_path):
            with open(self.session_file_path, "r") as f:
                session_data = json.load(f)
                self.cookies = session_data['cookies']
                self.user = session_data.get('user', {})

            self.logged_in = True

