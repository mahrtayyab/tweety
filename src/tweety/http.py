import inspect
import os
import re
import warnings
from typing import Callable
from urllib.parse import quote
import httpx as s
from .exceptions_ import GuestTokenNotFound, UnknownError, UserNotFound, InvalidCredentials
from .types.n_types import GenericError
from .utils import custom_json, GUEST_TOKEN_REGEX
from .builder import UrlBuilder

s.Response.json_ = custom_json


class Request:
    def __init__(self, client, max_retries=10, proxy=None, **kwargs):
        self.user = None
        self.username = None
        self._client = client
        self._limits = {}
        self.__session = s.Client(proxies=proxy, timeout=60, **kwargs)
        self.__builder = UrlBuilder()
        self.__guest_token = self._get_guest_token(max_retries)
        self.__builder.guest_token = self.__guest_token

    @property
    def session(self):
        return self.__session

    def add_header(self, key, value):
        self.__session.headers[key] = value
        self.__builder.custom_headers.update({key: value})

    def remove_header(self, key):
        if self.__session.headers.get(key):
            del self.__session.headers[key]

        if self.__builder.custom_headers.get(key):
            del self.__builder.custom_headers[key]

    def set_cookies(self, cookies, verify=True):
        self.__session.headers['Cookie'] = cookies
        self.__builder.set_cookies(cookies)

        if verify:
            self._verify_cookies()

    def set_user(self, user):
        self.user = user

    def _wait_for_rate_limit(self, url):
        raise NotImplemented

    def _update_rate_limit(self, response, func):
        url = response.url
        headers = response.headers

        if all(key in headers for key in ['x-rate-limit-reset', 'x-rate-limit-remaining']):
            self._limits[func] = dict(
                path=url.path,
                func=func,
                limit_reset=int(headers['x-rate-limit-reset']),
                limit_remaining=int(headers['x-rate-limit-remaining'])
            )

    def __get_response__(self, return_raw=False, ignore_none_data=False, is_document=False, **request_data):

        response = self.__session.request(**request_data)
        self._update_rate_limit(response, inspect.stack()[1][3])
        if is_document:
            return response

        response_json = response.json_()  # noqa
        if ignore_none_data and len(response.text) == 0:
            return None

        if response.text and response.text.lower() == "rate limit exceeded":
            response_json = {"errors": [{"code": 88, "message": "Rate limit exceeded."}]}

        if not response_json:
            raise UnknownError(
                error_code=response.status_code,
                error_name="Server Error",
                response=response,
                message="Unknown Error Occurs on Twitter"
            )

        if response_json.get("errors") and not response_json.get('data'):
            error = response_json['errors'][0]
            return GenericError(
                response, error.get("code"), error.get("message")
            )

        if return_raw:
            return response

        return response_json

    def _get_guest_token(self, max_retries=10):
        last_response = None
        for retry in range(max_retries):
            last_response = self.__get_response__(**self.__builder.get_guest_token())
            token = self.__builder.guest_token = last_response.get('guest_token')  # noqa

            if token:
                return token

            request_data = self.__builder.get_guest_token_fallback()
            del request_data['headers']['Authorization']
            del request_data['headers']['Content-Type']
            del request_data['headers']['X-Csrf-Token']
            response = self.__get_response__(is_document=True, **request_data)
            guest_token = re.findall(GUEST_TOKEN_REGEX, response.text)

            if guest_token:
                return guest_token[0]

        raise GuestTokenNotFound(None, None, last_response,
                                 f"Guest Token couldn't be found after {max_retries} retires.")

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

        if response.get("data"):  # noqa
            return response

        raise UserNotFound(error_code=50, error_name="GenericUserNotFound", response=response)

    def get_users_by_rest_id(self, user_ids):
        request_data = self.__builder.users_by_rest_id([str(i) for i in user_ids])
        response = self.__get_response__(**request_data)
        return response

    def login(self, _url, _payload):
        request_data = self.__builder.build_flow(_url)
        request_data['json'] = _payload
        request_data['headers']['Content-Type'] = "application/json"
        response = self.__get_response__(True, **request_data)
        return response

    def get_tweets(self, user_id, replies=False, cursor=None):
        request_data = self.__builder.user_tweets(user_id=user_id, replies=replies, cursor=cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_medias(self, user_id, cursor=None):
        request_data = self.__builder.user_media(user_id=user_id, cursor=cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_trends(self):
        response = self.__get_response__(**self.__builder.trends())
        return response

    def perform_search(self, keyword, cursor, filter_):
        if keyword.startswith("#"):
            keyword = f"%23{keyword[1:]}"

        keyword = quote(keyword, safe="()%")
        request_data = self.__builder.search(keyword, cursor, filter_)
        response = self.__get_response__(**request_data)
        return response

    def search_typehead(self, q, result_type='events,users,topics,lists'):
        request = self.__builder.search_typehead(q, result_type)
        response = self.__get_response__(**request)
        return response

    def get_tweet_detail(self, tweetId, cursor=None):
        if self.user:
            response = self.__get_response__(**self.__builder.tweet_detail(tweetId, cursor))
        else:
            response = self.__get_response__(**self.__builder.tweet_detail_as_guest(tweetId))
        return response

    def get_tweet_analytics(self, tweet_id):
        request = self.__builder.get_tweet_analytics(tweet_id)
        response = self.__get_response__(**request)
        return response

    def get_blocked_users(self, cursor):
        request = self.__builder.get_blocked_users(cursor)
        response = self.__get_response__(**request)
        return response

    def get_tweet_translation(self, tweet_id, target_language):
        request = self.__builder.tweet_translate(tweet_id, target_language)
        response = self.__get_response__(**request)
        return response

    def get_tweet_edit_history(self, tweet_id):
        response = self.__get_response__(**self.__builder.tweet_edit_history(tweet_id))
        return response

    def get_mentions(self, user_id, cursor=None):
        response = self.__get_response__(**self.__builder.get_mentions(cursor))
        return response

    def get_bookmarks(self, cursor=None):
        response = self.__get_response__(**self.__builder.get_bookmarks(cursor))
        return response

    def get_inbox(self, user_id, cursor=None):
        request = self.__builder.get_inbox(cursor)
        response = self.__get_response__(**request)
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
        request_data = self.__builder.create_pool(pool)
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

    def create_tweet(self, text, files, filter_, reply_to, quote_tweet_url, pool):
        if pool:
            response = self.create_pool(pool)
            pool = response.get('card_uri')

        request_data = self.__builder.create_tweet(text, files, filter_, reply_to, quote_tweet_url, pool)
        response = self.__get_response__(**request_data)
        return response

    def set_media_set_metadata(self, media_id, alt_text, sensitive_tags):
        request_data = self.__builder.set_media_metadata(media_id, alt_text, sensitive_tags)
        response = self.__get_response__(ignore_none_data=True, **request_data)
        return response

    def upload_media_init(self, size, mime_type, media_category, source_url):
        request_data = self.__builder.upload_media_init(size, mime_type, media_category, source_url)
        response = self.__get_response__(**request_data)
        return response

    def upload_media_append(self, media_id, payload, headers, segment_index):
        request_data = self.__builder.upload_media_append(media_id, segment_index)
        request_data['headers'].update(headers)
        request_data['data'] = payload

        response = self.__get_response__(ignore_none_data=True, **request_data)
        return response

    def upload_media_finalize(self, media_id, md5_hash):
        request_data = self.__builder.upload_media_finalize(media_id, md5_hash)
        response = self.__get_response__(**request_data)
        return response

    def upload_media_status(self, media_id):
        request_data = self.__builder.upload_media_status(media_id)
        response = self.__get_response__(**request_data)
        return response

    def get_home_timeline(self, timeline_type, cursor=None):
        request_data = self.__builder.home_timeline(timeline_type, cursor)
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

    def unlike_tweet(self, tweet_id):
        request_data = self.__builder.unlike_tweet(tweet_id)
        response = self.__get_response__(**request_data)
        return response

    def retweet_tweet(self, tweet_id):
        request_data = self.__builder.retweet_tweet(tweet_id)
        response = self.__get_response__(**request_data)
        return response

    def delete_retweet(self, tweet_id):
        request_data = self.__builder.delete_retweet(tweet_id)
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
    
    def block_user(self, user_id):
        request_data = self.__builder.block_user(user_id)
        request_data['headers']['Content-Type'] = f"application/x-www-form-urlencoded"
        response = self.__get_response__(**request_data)
        return response

    def unblock_user(self, user_id):
        request_data = self.__builder.unblock_user(user_id)
        request_data['headers']['Content-Type'] = f"application/x-www-form-urlencoded"
        response = self.__get_response__(**request_data)
        return response

    def get_user_followers(self, user_id, cursor=None):
        request_data = self.__builder.get_user_followers(user_id, cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_user_followings(self, user_id, cursor=None):
        request_data = self.__builder.get_user_followings(user_id, cursor)
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

    def remove_list_member(self, list_id, user_id):
        request_data = self.__builder.remove_member_from_list(list_id, user_id)
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

    def gif_search(self, search_term, cursor):
        request_data = self.__builder.search_gifs(search_term, cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_mutual_friends(self, user_id, cursor):
        request_data = self.__builder.get_mutual_friend(user_id, cursor)
        response = self.__get_response__(**request_data)
        return response

    def get_topic_landing_page(self, topic_id, cursor=None):
        request_data = self.__builder.get_topic_landing_page(topic_id, cursor)
        response = self.__get_response__(**request_data)
        return response

    def download_media(self, media_url, filename: str = None,
                       progress_callback: Callable[[str, int, int], None] = None):
        filename = os.path.basename(media_url).split("?")[0] if not filename else filename
        headers = self.__builder._get_headers()
        oldReferer = headers.get('Referer')

        if media_url.startswith("https://ton.twitter.com"):
            headers['Referer'] = "https://twitter.com/"
            self.__session.header = headers

        with self.__session.stream('GET', media_url, follow_redirects=True, headers=headers, timeout=600) as response:
            response.raise_for_status()
            try:
                total_size = int(response.headers['Content-Length'])
            except:
                warnings.warn("Unable to get 'Content-Length', it will be set to zero")
                total_size = 0

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
