import getpass
from http.cookiejar import MozillaCookieJar
from typing import Union
from .exceptions import InvalidCredentials, DeniedLogin, ActionRequired, ArkoseLoginRequired
from .builder import FlowData
from .types.n_types import Cookies
from .utils import find_objects, get_url_parts
from . import constants


class AuthMethods:

    def connect(self):
        """
        This method will be used to connect to already saved session in disk
        """

        if not self.session.logged_in:
            return

        self.request.cookies = self.session.cookies_dict()
        self.request.verify_cookies()
        self.user = self.get_user_info(self.request.username)
        self.request.set_user(self.user)
        self.session.set_session_user(self.user)
        self._is_connected = True
        self.is_user_authorized = True
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
                self.request.cookies = None
                pass

        username = input('Please enter the Username: ') if not username else username
        password = getpass.getpass('Please enter your password: ') if not password else password

        _extra = extra
        _extra_once = False
        while not self.logged_in:
            try:
                return self.sign_in(username, password, extra=_extra)
            except ActionRequired as e:
                _extra = input(f"\rAction Required :> {str(e.message)} : ")
                _extra_once = True
            except InvalidCredentials as ask_info:
                if _extra_once:
                    _extra = input(f"\rAction Required :> {str(ask_info.message)} : ")
                else:
                    raise ask_info

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
                self.request.set_cookies("", False)
                pass

        self._username = username
        self._password = password
        self._extra = extra
        self._captcha_token = None

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

    def load_auth_token(self, auth_token):
        URL = "https://x.com/i/api/1.1/account/update_profile.json"
        temp_cookie = {"auth_token": auth_token}
        temp_headers = {'authorization': constants.DEFAULT_BEARER_TOKEN}
        res = self.request.session.post(URL, cookies=temp_cookie, headers=temp_headers)
        ct0 = res.cookies.get('ct0')

        if not ct0:
            raise DeniedLogin(response=res, message="Auth Token isn't Valid")

        temp_cookie['ct0'] = ct0
        return self.load_cookies(temp_cookie)

    @staticmethod
    def _get_action_text(response):
        primary_message = find_objects(response, 'primary_text', None, none_value={})
        secondary_message = find_objects(response, 'secondary_text', None, none_value={})
        if primary_message:
            if isinstance(primary_message, list):
                primary_message = primary_message[0]

            primary_message = primary_message.get('text', '')

        if secondary_message:
            if isinstance(secondary_message, list):
                secondary_message = secondary_message[0]
            secondary_message = secondary_message.get('text', '')
        return f"{primary_message}. {secondary_message}"

    def _login(self):
        _username, _password, _extra = self._username, self._password, self._extra

        while not self.logged_in:
            _login_payload = self._login_flow.get(
                self._login_flow_state,
                json_=self._last_json,
                username=_username,
                password=_password,
                extra=_extra,
                captcha_token=self._captcha_token
            )

            response = self.request.login(self._login_url, _payload=_login_payload)

            self._last_json = response.json()

            if response.cookies.get("att"):
                self.request.headers = {"att": response.cookies.get("att")}

            if self._last_json.get('status') != "success":
                raise DeniedLogin(response=response, message=response.text)

            self._login_url = self._login_url.split("?")[0]
            subtask = self._last_json["subtasks"][0].get("subtask_id")
            self._login_flow_state = subtask

            if subtask in ("LoginTwoFactorAuthChallenge", "LoginAcid", "LoginEnterAlternateIdentifierSubtask") and not _extra:
                message = self._get_action_text(self._last_json)
                raise ActionRequired(0, "ActionRequired", response, message)

            if subtask == "ArkoseLogin":
                if self._captcha_solver is None:
                    raise ArkoseLoginRequired(response=response)

                token = self.request.solve_captcha(websiteUrl="https://iframe.arkoselabs.com")
                # token = self.request.solve_captcha(websiteUrl="https://twitter.com/i/flow/login", blob_data=data[0])
                self._captcha_token = token

            if subtask == "DenyLoginSubtask":
                reason = self._get_action_text(self._last_json)
                raise DeniedLogin(response=response, message=reason)

            if subtask == "LoginSuccessSubtask":
                self.request.remove_header("att")
                self.logged_in = True
                self.cookies = Cookies(dict(response.cookies))
                self.session.save_session(self.cookies)
                return self.connect()

        raise DeniedLogin(response=response, message="Unknown Error Occurred")



