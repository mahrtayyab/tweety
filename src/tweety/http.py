import os
import httpx as s
from tqdm import tqdm

from .exceptions_ import GuestTokenNotFound, UnknownError, UserNotFound, InvalidCredentials
from .types.n_types import GenericError
from .utils import custom_json
from .builder import UrlBuilder

s.Response.json_ = custom_json


class Request:
    def __init__(self, max_retries=10, proxy=None, cookies=None):
        self.username = None
        self.__is_client = True if cookies else False
        self.__session = s.Client(proxies=proxy, cookies=self._parse_cookies(cookies), timeout=60)
        self.__builder = UrlBuilder(self.__session.cookies)
        self.__guest_token = self._get_guest_token(max_retries)
        self._init_api()
        self._verify_cookies()

    def __get_response__(self, **request_data):
        response = self.__session.request(**request_data)
        response_json = response.json_() # noqa

        if not response_json:
            raise UnknownError(
                error_code=500,
                error_name="Server Error",
                response=response,
                message="Unknown Error Occurs on Twitter"
            )

        if response_json.get("errors") and not response_json.get("data"):
            error = response_json['errors'][0]
            return GenericError(
                response, error.get("code"), error.get("message")
            )

        return response_json

    @staticmethod
    def _parse_cookies(cookies):
        if not cookies:
            return None

        true_cookies = dict()
        if isinstance(cookies, str):
            cookie_list = cookies.split(";")
            for cookie in cookie_list:
                split_cookie = cookie.strip().split("=")

                if len(split_cookie) >= 2:
                    cookie_key = split_cookie[0]
                    cookie_value = split_cookie[1]
                    true_cookies[cookie_key] = cookie_value
        elif isinstance(cookies, dict):
            true_cookies = cookies
        else:
            raise TypeError("cookies should be of class 'str' or 'dict' not {}".format(cookies.__class__))

        if not true_cookies.get("ct0"):
            raise InvalidCredentials(None, None, None, "'ct0' key in cookies isn't available")

        return true_cookies

    def _get_guest_token(self, max_retries=10):
        if self.__is_client:
            return

        for retry in range(max_retries):
            response = self.__get_response__(**self.__builder.get_guest_token())

            token = self.__builder.guest_token = response['guest_token'] # noqa
            return token

        raise GuestTokenNotFound(None, None, None, f"Guest Token couldn't be found after {max_retries} retires.")

    def _init_api(self):
        data = self.__builder.init_api()
        data['json'] = {}
        self.__get_response__(**data)

    def _verify_cookies(self):
        if not self.__is_client:
            return

        data = self.__builder.aUser_settings()
        response = self.__get_response__(**data)

        if not response.get("screen_name"):
            raise InvalidCredentials(None, None, None)

        self.username = response.get("screen_name")

    def get_user(self, username=None):
        if not username:

            if not self.username:
                raise ValueError("'username' is required")

            username = self.username

        response = self.__get_response__(**self.__builder.user_by_screen_name(username))

        if response.get("data"): # noqa
            return response

        raise UserNotFound(error_code=50, error_name="GenericUserNotFound", response=response)

    def get_tweets(self, user_id, replies=False, cursor=None):
        request_data = self.__builder.user_tweets(user_id=user_id, replies=replies, cursor=cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_trends(self):
        response = self.__get_response__(**self.__builder.trends())
        return response

    def perform_search(self, keyword, cursor, filter_):
        if keyword.startswith("#"):
            keyword = f"%23{keyword[1:]}"

        request_data = self.__builder.search(keyword, cursor, filter_)
        # del request_data['headers']['content-type']
        request_data['headers']['referer'] = f"https://twitter.com/search?q={keyword}"

        response = self.__get_response__(**request_data)
        return response

    def get_tweet_detail(self, tweetId):
        response = self.__get_response__(**self.__builder.tweet_detail(tweetId))
        return response

    def download_media(self, media_url, filename=None, show_progress=True):
        filename = os.path.basename(media_url).split("?")[0] if not filename else filename

        with self.__session.stream('GET', media_url) as response:
            response.raise_for_status()
            content_length = int(response.headers['Content-Length'])
            f = open(filename, 'wb')
            if show_progress:
                with tqdm(total=content_length, unit='B', unit_scale=True, desc=f"[{filename}]") as pbar:
                    for chunk in response.iter_bytes(chunk_size=8192):
                        f.write(chunk)
                        pbar.update(len(chunk))
            else:
                for chunk in response.iter_bytes(chunk_size=8192):
                    f.write(chunk)
            f.close()

        return filename
