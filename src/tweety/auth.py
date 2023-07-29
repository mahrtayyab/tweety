from http.cookiejar import MozillaCookieJar
from .exceptions_ import InvalidCredentials, DeniedLogin
from .builder import FlowData
from .types.n_types import Cookies


class AuthMethods:

    def connect(self):
        """
        This method will be used to connect to already saved session in disk
        """
        if self.session.logged_in:
            self.request.set_cookies(str(self.session))
            self.user = self.get_user_info(self.request.username)
            self.session.set_session_user(self.user)
            self._is_connected = True
            return

    def sign_in(self, username, password, *, extra=None):
        """
        - This method can be used to sign in to Twitter using username and password
        - It will also check for the saved session for the username in the disk

        :param username: (`str`) Username of the user
        :param password: (`str`) Password of the user
        :param extra: ## NotImplemented
        :return:
        """
        if self.session.logged_in and self.session.user['username'] == username:
            try:
                return self.connect()
            except InvalidCredentials:
                pass

        _username = username
        _password = password
        _extra = extra
        self._login(_username, _password, _extra)

    def load_cookies(self, cookies: [str, dict, MozillaCookieJar]):
        """
        This method can be used to load the already authenticated cookies from Twitter

        :param cookies:  (`str`, `dict`, `MozillaCookieJar`) The Cookies to load
        :return:
        """
        self.cookies = Cookies(cookies, False)
        self.logged_in = True
        self.session.save_session(self.cookies)
        self.connect()

    def _login(self, _username, _password, _extra):
        __login_url = "https://api.twitter.com/1.1/onboarding/task.json?flow_name=login"
        __login_flow = FlowData(_username, _password, _extra)
        __login_flow_state = __login_flow.initial_state
        __login_payload = __login_flow.get(__login_flow_state, json_={}, username=_username, password=_password)
        while not self.logged_in:
            response = self.request.login(__login_url, _payload=__login_payload)
            json_ = response.json()
            if response.json().get('status') == 'success':
                __login_url = __login_url.split("?")[0]
                subtask = response.json()["subtasks"][0].get("subtask_id")
                __login_flow_state = subtask
                if subtask == "LoginSuccessSubtask":
                    self.logged_in = True
                    self.cookies = Cookies(response.headers['set-cookie'], True)
                    self.session.save_session(self.cookies)
                    self.connect()
                    return
                __login_payload = __login_flow.get(__login_flow_state, json_=json_, username=_username, password=_password)
            else:
                raise DeniedLogin(
                    error_code=37,
                    error_name="GenericAccessDenied",
                    response=None,
                    message=response.text
                )




