import json
import os
import httpx as s
from tqdm import tqdm
from .exceptions_ import GuestTokenNotFound, UnknownError, UserNotFound, InvalidCredentials
from .types.n_types import GenericError
from .utils import custom_json, create_request_id
from .builder import UrlBuilder


s.Response.json_ = custom_json


class Request:
    def __init__(self, max_retries=10, proxy=None):
        self.user = None
        self.username = None
        self.__session = s.Client(proxies=proxy, timeout=60)
        self.__builder = UrlBuilder()
        self.__guest_token = self._get_guest_token(max_retries)

    def set_cookies(self, cookies):
        self.__session.headers['Cookie'] = cookies
        self.__builder.set_cookies(cookies)
        self._verify_cookies()

    def set_user(self, user):
        self.user = user
        self.__builder.set_cookies(self.__session.cookies)

    def __get_response__(self, return_raw=False, **request_data):
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
        if return_raw:
            return response

        return response_json

    def _get_guest_token(self, max_retries=10):
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

    def login(self, _url, _payload):
        request_data = self.__builder.build_flow(_url)
        request_data['json'] = _payload
        response = self.__get_response__(True, **request_data)
        return response

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

    def get_tweet_detail(self, tweetId, cursor=None):
        response = self.__get_response__(**self.__builder.tweet_detail(tweetId, cursor))
        return response

    def get_mentions(self, user_id, cursor=None):
        response = self.__get_response__(**self.__builder.get_mentions(cursor))
        return response

    def get_inbox(self, user_id, cursor=None):
        response = self.__get_response__(**self.__builder.get_inbox(cursor))
        return response

    def get_trusted_inbox(self, max_id):
        response = self.__get_response__(**self.__builder.get_trusted_inbox(max_id))
        return response

    def get_untrusted_inbox(self, max_id, low_quality=False):
        response = self.__get_response__(**self.__builder.get_untrusted_inbox(max_id, low_quality))
        return response

    def get_conversation(self, conversation_id, max_id=None):
        response = self.__get_response__(**self.__builder.get_conversation_with_messages(conversation_id, max_id))
        return response

    def send_message(self, conversation_id, text):
        request_id = create_request_id()
        json_data = {
            'conversation_id': conversation_id,
            'recipient_ids': False,
            'request_id': request_id,
            'text': text,
            'cards_platform': 'Web-12',
            'include_cards': 1,
            'include_quote_count': True,
            'dm_users': False,
        }
        request_data = self.__builder.send_message()
        request_data['json'] = json_data
        response = self.__get_response__(**request_data)
        return response

    def download_media(self, media_url, filename=None, show_progress=True):
        filename = os.path.basename(media_url).split("?")[0] if not filename else filename
        headers = self.__session.headers
        oldReferer = headers.get('Referer')

        if media_url.startswith("https://ton.twitter.com"):
            headers['Referer'] = "https://twitter.com/"
            self.__session.header = headers

        with self.__session.stream('GET', media_url, follow_redirects=True) as response:
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

        self.__session.header['Referer'] = oldReferer
        return filename
