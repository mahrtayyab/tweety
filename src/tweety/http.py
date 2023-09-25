import datetime
import inspect
import json
import os
import time
from typing import Callable
from urllib.parse import urlparse
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
        self._limits = []
        self.__session = s.Client(proxies=proxy, timeout=60)
        self.__builder = UrlBuilder()
        self.__guest_token = self._get_guest_token(max_retries)

    @property
    def session(self):
        return self.__session

    def set_cookies(self, cookies):
        self.__session.headers['Cookie'] = cookies
        self.__builder.set_cookies(cookies)
        self._verify_cookies()

    def set_user(self, user):
        self.user = user

    def _wait_for_rate_limit(self, url):
        raise NotImplemented

    def _update_rate_limit(self, response, func):
        url = response.url
        headers = response.headers

        if all(key in headers for key in ['x-rate-limit-reset', 'x-rate-limit-remaining']):
            self._limits.append(dict(
                path=url.path,
                func=func,
                limit_reset=int(headers['x-rate-limit-reset']),
                limit_remaining=int(headers['x-rate-limit-remaining'])
            ))

    def __get_response__(self, return_raw=False, ignoreNoneData=False, **request_data):

        response = self.__session.request(**request_data)
        self._update_rate_limit(response, inspect.stack()[1][3])

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

        if response_json.get("errors"):
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

    def create_pool(self, pool):
        request_data = self.__builder.create_tweet(pool)
        response = self.__get_response__(**request_data)
        return response

    def poll_vote(self, poll_id, poll_name, tweet_id, choice):
        request_data = self.__builder.poll_vote(poll_id, poll_name, tweet_id, choice)
        response = self.__get_response__(**request_data)
        return response

    def delete_tweet(self, tweet_id):
        request_data = self.__builder.delete_tweet(tweet_id)
        response = self.__get_response__(**request_data)
        return response

    def create_tweet(self, text, files, filter_, reply_to, pool):
        if pool:
            response = self.create_pool(pool)
            pool = response.get('card_uri')

        request_data = self.__builder.create_tweet(text, files, filter_, reply_to, pool)
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

    def upload_media_status(self, media_id):
        request_data = self.__builder.upload_media_status(media_id)
        response = self.__get_response__(**request_data)
        return response

    def get_home_timeline(self, cursor=None):
        request_data = self.__builder.home_timeline(cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_tweet_likes(self, tweet_id, cursor=None):
        request_data = self.__builder.get_tweet_likes(tweet_id, cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_tweet_retweets(self, tweet_id, cursor=None):
        request_data = self.__builder.get_tweet_retweets(tweet_id, cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_audio_space(self, audio_space_id):
        request_data = self.__builder.get_audio_space(audio_space_id)
        response = self.__get_response__(**request_data)
        return response

    def get_audio_stream(self, media_key):
        request_data = self.__builder.get_audio_stream(media_key)
        response = self.__get_response__(**request_data)
        return response

    def like_tweet(self, tweet_id):
        request_data = self.__builder.like_tweet(tweet_id)
        response = self.__get_response__(**request_data)
        return response

    def retweet_tweet(self, tweet_id):
        request_data = self.__builder.retweet_tweet(tweet_id)
        response = self.__get_response__(**request_data)
        return response

    def get_community(self, community_id):
        request_data = self.__builder.get_community(community_id)
        response = self.__get_response__(**request_data)
        return response

    def get_community_tweets(self, community_id, filter_, cursor):
        request_data = self.__builder.get_community_tweets(community_id, filter_, cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_community_members(self, community_id, filter_, cursor):
        request_data = self.__builder.get_community_members(community_id, filter_, cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_tweet_notifications(self, cursor):
        request_data = self.__builder.get_new_user_tweet_notification(cursor)
        response = self.__get_response__(**request_data)
        return response

    def follow_user(self, user_id):
        request_data = self.__builder.follow_user(user_id)
        request_data['headers']['Content-Type'] = f"application/x-www-form-urlencoded"
        response = self.__get_response__(**request_data)
        return response

    def unfollow_user(self, user_id):
        request_data = self.__builder.unfollow_user(user_id)
        request_data['headers']['Content-Type'] = f"application/x-www-form-urlencoded"
        response = self.__get_response__(**request_data)
        return response

    def toggle_user_notifications(self, user_id, action):
        request_data = self.__builder.toggle_user_notifications(user_id, action)
        response = self.__get_response__(**request_data)
        return response

    def get_lists(self, cursor=None):
        request_data = self.__builder.get_lists(cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_list(self, list_id):
        request_data = self.__builder.get_list(list_id)
        response = self.__get_response__(**request_data)
        return response

    def get_list_members(self, list_id, cursor):
        request_data = self.__builder.get_list_member(list_id, cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_list_tweets(self, list_id, cursor):
        request_data = self.__builder.get_list_tweets(list_id, cursor)
        response = self.__get_response__(**request_data)
        return response

    def add_list_member(self, list_id, user_id):
        request_data = self.__builder.add_member_to_list(list_id, user_id)
        response = self.__get_response__(**request_data)
        return response

    def create_list(self, name, description, is_private):
        request_data = self.__builder.create_list(name, description, is_private)
        response = self.__get_response__(**request_data)
        return response

    def delete_list(self, list_id):
        request_data = self.__builder.delete_list(list_id)
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
