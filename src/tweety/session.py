import json
import os.path


class Session:
    def __init__(self, session_name):
        self.user = None
        self.session_name = session_name
        self.session_file_path = os.path.join(os.getcwd(), f"{self.session_name}.json")
        self.logged_in = False
        self.cookies = ""
        self._load_session()

    def _load_session(self):
        if os.path.exists(self.session_file_path):
            with open(self.session_file_path, "r") as f:
                session_data = json.load(f)
                self.cookies = session_data['cookies']
                self.user = session_data['user']

            self.logged_in = True

    def set_session_user(self, user):
        self.user = dict(user)

        with open(self.session_file_path, "w") as f:
            session_data = dict(cookies=str(self.cookies), user=dict(user))
            json.dump(session_data, f, indent=4, default=str)

    def save_session(self, cookies):
        self.cookies = str(cookies)
        self.logged_in = True
        with open(self.session_file_path, "w") as f:
            session_data = dict(cookies=str(cookies))
            json.dump(session_data, f, indent=4)

    def __str__(self):
        return self.cookies

