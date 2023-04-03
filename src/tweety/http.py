import httpx as s
from .exceptions_ import GuestTokenNotFound, UnknownError
from .utils import custom_json
from .builder import UrlBuilder

s.Response.json_ = custom_json


class Request:
    def __init__(self, profile_url, max_retries=10, proxy=None):
        self.__builder = UrlBuilder(profile_url)
        self.__session = s.Client()
        self.__session.proxies = proxy
        self.__guest_token = self._get_guest_token(max_retries)
        self._init_api()

    def _get_guest_token(self, max_retries=10):
        for retry in range(max_retries):
            response = self.__session.post(**self.__builder.get_guest_token())

            if response.json_(): # noqa
                token = self.__builder.guest_token = response.json_()['guest_token'] # noqa
                return token

        raise GuestTokenNotFound(f"Guest Token couldn't be found after {max_retries} retires.")

    def _init_api(self):
        data = self.__builder.init_api()
        data['json'] = {}
        self.__session.post(**data)

    def verify_user(self, username):
        response = self.__session.get(**self.__builder.user_by_screen_name(username))

        if response.json_() and response.json().get("data"): # noqa
            return response.json()

        return False

    def get_tweets(self, user_id, replies=False, cursor=None):
        request_data = self.__builder.user_tweets(user_id=user_id, replies=replies, cursor=cursor)
        response = self.__session.get(**request_data)
        return response

    def get_trends(self):
        response = self.__session.get(**self.__builder.trends())
        return response

    def perform_search(self, keyword, cursor, filter_):
        if keyword.startswith("#"):
            keyword = f"%23{keyword[1:]}"

        request_data = self.__builder.search(keyword, cursor, filter_)
        del request_data['headers']['content-type']
        request_data['headers']['referer'] = f"https://twitter.com/search?q={keyword}"

        response = self.__session.get(**request_data)
        return response

    def get_tweet_detail(self, tweetId):
        response = self.__session.get(**self.__builder.tweet_detail(tweetId))
        return response
