import getpass
from http.cookiejar import MozillaCookieJar
from typing import Union
from .exceptions_ import InvalidCredentials, DeniedLogin, ActionRequired
from .builder import FlowData
from .types.n_types import Cookies


class AuthMethods:

    def connect(self):
        """
        This method will be used to connect to already saved session in disk
        """

        if not self.session.logged_in:
            return

        self.request.set_cookies(str(self.session))
        self.user = self.get_user_info(self.request.username)
        self.request.set_user(self.user)
        self.session.set_session_user(self.user)
        self._is_connected = True
        return self.user

    def start(
            self,
            username=None,
            password=None,
            *,
            extra=None
    ):
        """
        Interactive Version of `sign_in` which will ask user for inputs
        Most of the time , this would be the only method you will be working with,
        it will check for existing sessions and login to it if available

        :param username: (`str`) Username of the user
        :param password: (`str`) Password of the user
        :param extra: (`str`) If you have 2-Factor authentication enabled and already have a code ,
                                or any other action required for completing the login process
                                it will be passed to this parameter
        :return: .types.twDataTypes.User (the user which is authenticated)
        """

        if self.session.logged_in:
            try:
                return self.connect()
            except InvalidCredentials:
                pass

        username = input('Please enter the Username: ') if not username else username
        password = getpass.getpass('Please enter your password: ') if not password else password
        try:
            return self.sign_in(username, password, extra=extra)
        except ActionRequired as e:
            action = input(f"Action Required :> {str(e.message)} : ")
            return self.sign_in(username, password, extra=action)

    def sign_in(
            self,
            username,
            password,
            *,
            extra=None
    ):
        """
        - This method can be used to sign in to Twitter using username and password
        - It will also check for the saved session for the username in the disk

        :param username: (`str`) Username of the user
        :param password: (`str`) Password of the user
        :param extra: (`str`) If you have 2-Factor authentication enabled and already have a code ,
                                or any other action required for completing the login process
                                it will be passed to this parameter
        :return: .types.twDataTypes.User (the user which is authenticated)
        """

        if self.session.logged_in and self.session.user['username'].lower() == username.lower():
            try:
                return self.connect()
            except InvalidCredentials:
                pass

        self._username = username
        self._password = password
        self._extra = extra

        if not self._login_flow:
            self._login_flow = FlowData()

        if not self._login_flow_state:
            self._login_flow_state = self._login_flow.initial_state

        return self._login()

    def load_cookies(
            self,
            cookies: Union[str, dict, MozillaCookieJar]
    ):
        """
        This method can be used to load the already authenticated cookies from Twitter

        :param cookies:  (`str`, `dict`, `MozillaCookieJar`) The Cookies to load
        :return: .types.twDataTypes.User (the user which is authenticated)
        """
        self.cookies = Cookies(cookies, False)
        self.logged_in = True
        self.session.save_session(self.cookies)
        return self.connect()

    def _login(self):
        _username, _password, _extra = self._username, self._password, self._extra

        while not self.logged_in:
            _login_payload = self._login_flow.get(self._login_flow_state, json_=self._last_json, username=_username, password=_password, extra=_extra)
            response = self.request.login(self._login_url, _payload=_login_payload)
            self._last_json = response.json()

            if self._last_json.get('status') != "success":
                raise DeniedLogin(response=response, message=response.text)

            self._login_url = self._login_url.split("?")[0]
            subtask = self._last_json["subtasks"][0].get("subtask_id")
            self._login_flow_state = subtask

            if subtask in ("LoginTwoFactorAuthChallenge", "LoginAcid", "LoginEnterAlternateIdentifierSubtask") and not _extra:
                message = self._last_json['subtasks'][0]['enter_text']['header']['secondary_text']['text']
                raise ActionRequired(0, "ActionRequired", response, message)

            if subtask == "DenyLoginSubtask":
                reason = self._last_json['subtasks'][0]['cta']['primary_text']['text']
                raise DeniedLogin(response=response, message=reason)

            if subtask == "LoginSuccessSubtask":
                self.logged_in = True
                self.cookies = Cookies(response.headers['set-cookie'], True)
                self.session.save_session(self.cookies)
                return self.connect()

        raise DeniedLogin(response=response, message="Unknown Error Occurred")



