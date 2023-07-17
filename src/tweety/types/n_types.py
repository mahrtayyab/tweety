from ..exceptions_ import *

PROXY_TYPE_SOCKS4 = SOCKS4 = 1
PROXY_TYPE_SOCKS5 = SOCKS5 = 2
PROXY_TYPE_HTTP = HTTP = 3


class Proxy:
    def __init__(self, host: str, port: int, proxy_type: int, username: str = None, password: str = None):
        self.host = host
        self.password = password
        self.proxy_type = proxy_type
        self.username = username
        self.port = port
        self.proxy = self.__parse__()

    def __proxy_url__(self):
        if self.username and self.password:
            return "{}:{}@{}:{}".format(
                self.username, self.password, self.host, self.password
            )
        else:
            return "{}:{}".format(self.host, self.password)

    def __parse__(self):
        proxy_url = self.__proxy_url__()
        if self.proxy_type == HTTP:
            return dict(http=proxy_url, https=proxy_url)
        elif self.proxy_type == SOCKS4:
            socks_url = "socks4://{}".format(proxy_url)
            return dict(http=socks_url, https=socks_url)
        elif self.proxy_type == SOCKS5:
            socks_url = "socks5://{}".format(proxy_url)
            return dict(http=socks_url, https=socks_url)

        raise ProxyParseError()


class GenericError:
    EXCEPTIONS = {
        32: InvalidCredentials,
        144: InvalidTweetIdentifier,
        88: RateLimitReached,
        399: InvalidCredentials,
        220: InvalidCredentials
    }

    def __init__(self, response, error_code, message=None):
        self.response = response
        self.error_code = error_code
        self.message = message
        self._raise_exception()

    def _raise_exception(self):
        if self.EXCEPTIONS.get(self.error_code):
            raise self.EXCEPTIONS[self.error_code](
                error_code=self.error_code,
                error_name=TWITTER_ERRORS[self.error_code],
                response=self.response,
                message=self.message
            )

        raise UnknownError(
            error_code=self.error_code,
            error_name=TWITTER_ERRORS[self.error_code],
            response=self.response,
            message="[{}] {}".format(self.error_code, self.message)
        )


class Cookies:
    def __init__(self, cookies, is_http_response=False):
        self._raw_cookies = cookies
        self._is_http_response = is_http_response
        self.parse_cookies()

    def parse_cookies(self):
        if self._is_http_response:
            n = [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30]
            for k, p in enumerate(self._raw_cookies.split(",")):
                if k in n:
                    key, value = str(p.split(';')[0]).split("=", 1)
                    setattr(self, key.strip(), value.strip())
        else:
            true_cookies = dict()
            if isinstance(self._raw_cookies, str):
                cookie_list = self._raw_cookies.split(";")
                for cookie in cookie_list:
                    split_cookie = cookie.strip().split("=")

                    if len(split_cookie) >= 2:
                        cookie_key = split_cookie[0]
                        cookie_value = split_cookie[1]
                        true_cookies[cookie_key] = cookie_value
            elif isinstance(self._raw_cookies, dict):
                true_cookies = self._raw_cookies
            else:
                raise TypeError("cookies should be of class 'str' or 'dict' not {}".format(self._raw_cookies.__class__))

            for key, value in true_cookies.items():
                setattr(self, key.strip(), value.strip())

    def __str__(self):
        string = ""
        for k, v in vars(self).items():

            if not k.startswith("_"):
                string += f"{k}={v};"

        return string
