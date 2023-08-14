import json
import os
from typing import Callable

import httpx as s
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

    def __get_response__(self, return_raw=False, ignoreNoneData=False, **request_data):
        response = self.__session.request(**request_data)
        response_json = response.json_() # noqa

        if ignoreNoneData and len(response.text) == 0:
            return None

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

    def get_bookmarks(self, cursor=None):
        response = self.__get_response__(**self.__builder.get_bookmarks(cursor))
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

    def send_message(self, conversation_id, text, media_id):
        request_data = self.__builder.send_message(conversation_id, text, media_id)
        response = self.__get_response__(**request_data)
        return response

    def create_tweet(self, text, files, filter_, reply):
        request_data = self.__builder.create_tweet(text, files, filter_, reply)
        response = self.__get_response__(**request_data)
        return response

    def set_media_set_metadata(self, media_id, alt_text, sensitive_tags):
        request_data = self.__builder.set_media_metadata(media_id, alt_text, sensitive_tags)
        response = self.__get_response__(ignoreNoneData=True, **request_data)
        print(response)
        return response

    def upload_media_init(self, size, mime_type, media_category):
        request_data = self.__builder.upload_media_init(size, mime_type, media_category)
        response = self.__get_response__(**request_data)
        return response

    def upload_media_append(self, media_id, payload, headers, segment_index):
        request_data = self.__builder.upload_media_append(media_id, segment_index)
        request_data['headers'].update(headers)
        request_data['data'] = payload

        response = self.__get_response__(ignoreNoneData=True, **request_data)
        return response

    def upload_media_finalize(self, media_id, md5_hash):
        request_data = self.__builder.upload_media_finalize(media_id, md5_hash)
        response = self.__get_response__(**request_data)
        return response

    def download_media(self, media_url, filename: str = None, progress_callback: Callable[[str, int, int], None] = None):
        filename = os.path.basename(media_url).split("?")[0] if not filename else filename
        headers = self.__builder._get_headers()
        oldReferer = headers.get('Referer')

        if media_url.startswith("https://ton.twitter.com"):
            headers['Referer'] = "https://twitter.com/"
            self.__session.header = headers

        with self.__session.stream('GET', media_url, follow_redirects=True, headers=headers) as response:
            response.raise_for_status()
            total_size = int(response.headers['Content-Length'])
            downloaded = 0
            f = open(filename, 'wb')
            for chunk in response.iter_bytes(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)

                if progress_callback:
                    progress_callback(filename, total_size, downloaded)

            f.close()

        if oldReferer:
            self.__session.headers['Referer'] = oldReferer

        return filename
