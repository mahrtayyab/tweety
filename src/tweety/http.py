import asyncio
import inspect
import os
import random
import re
import traceback
import warnings
from typing import Callable
from urllib.parse import quote, urlparse
import bs4
import httpx
from .exceptions import GuestTokenNotFound, TwitterError, UserNotFound, InvalidCredentials
from .types import User
from .types.n_types import GenericError
from .utils import custom_json, GUEST_TOKEN_REGEX, get_random_string, MIGRATION_REGEX
from .builder import UrlBuilder
from .transaction import TransactionGenerator
from . import constants

httpx.Response.json = custom_json


class Request:

    def __init__(self, client, max_retries=3, proxy=None, captcha_solver=None, **kwargs):

        timeout = kwargs.pop("timeout", 60)

        self.user = None
        self.username = None
        self._retries = max_retries
        self._cookie = None
        self._client = client
        self._captcha_solver = captcha_solver
        self._limits = {}
        self._guest_token = None
        self._session = httpx.AsyncClient(
            headers={
                'user-agent': constants.REQUEST_USER_AGENT,
                'sec-ch-ua-platform': f'"{random.choice(constants.REQUEST_PLATFORMS)}"',
                'x-twitter-client-language': 'en',
                'origin': 'https://x.com'
            },
            http2=True,
            proxies=proxy,
            timeout=timeout,
            follow_redirects=True,
            **kwargs
        )
        self._builder = UrlBuilder()
        self._transaction = None
        self._guest_token = None

    @property
    def session(self):
        return self._session

    @property
    def headers(self):
        return self._session.headers

    @headers.setter
    def headers(self, value: dict):
        self._session.headers.update({k.lower(): v for k, v in value.items()})

    def remove_header(self, key):
        lower_key = key.lower()
        if self._session.headers.get(lower_key):
            del self._session.headers[lower_key]

    @property
    def cookies(self):
        return self._session.cookies

    @cookies.setter
    def cookies(self, value: dict):
        self._session.cookies = value
        self._cookie = value

    def _get_request_headers(self, custom_headers=None):
        if not custom_headers:
            custom_headers = {}

        default_headers = {
            'accept': '*/*',
            'accept-language': 'en-PK,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://x.com/',
            'authorization': constants.DEFAULT_BEARER_TOKEN,
            'sec-ch-ua': constants.REQUEST_USER_AGENT_CH,
            'sec-ch-ua-mobile': '?0',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'x-csrf-token': self._get_csrf(),
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'en',
            'priority': 'u=1, i'
        }

        session_headers = self._session.headers
        default_headers.update(session_headers)

        if self._guest_token or self._cookie:
            default_headers['content-type'] = 'application/json'
            default_headers['sec-fetch-site'] = 'same-origin'

            if self._cookie:
                default_headers['x-twitter-auth-type'] = 'OAuth2Session'

            if self._guest_token and not self._cookie:
                default_headers['x-guest-token'] = self._guest_token

        default_headers.update(custom_headers)

        headers = {}
        for header_key, header_value in default_headers.items():
            if header_value is not None:
                headers[header_key] = header_value

        return headers

    def _get_csrf(self):
        if self._cookie and self._cookie.get("ct0"):
            return self._cookie.get("ct0")

        return get_random_string(32)

    def set_user(self, user):
        self.user = user

    def _wait_for_rate_limit(self, url):
        raise NotImplemented

    async def _update_rate_limit(self, response, func):
        url = response.url
        headers = response.headers

        if all(key in headers for key in ['x-rate-limit-reset', 'x-rate-limit-remaining']):
            self._limits[func] = dict(
                path=url.path if not isinstance(url, str) else url,
                func=func,
                limit_reset=int(headers['x-rate-limit-reset']),
                limit_remaining=int(headers['x-rate-limit-remaining'])
            )

    async def _update_cookies(self, response):
        updated_required = False

        if not response.cookies or response.cookies is None or self._client.cookies is None:
            return

        if response.cookies.get("ct0"):
            updated_required = True
            setattr(self._client.cookies, "ct0", response.cookies.get("ct0"))
        if response.cookies.get("auth_token"):
            updated_required = True
            setattr(self._client.cookies, "auth_token", response.cookies.get("auth_token"))

        if updated_required:
            await self._client.session.save_session(self._client.cookies, None)

    async def remove_cookies(self):
        cookies_value = self.cookies
        self.cookies = self.session.cookies = None
        return cookies_value

    async def _init_local_api(self):
        cookies = await self.remove_cookies()
        if not self._transaction:
            home_page_html = await self.get_home_html()
            self._transaction = TransactionGenerator(home_page_html)

        if not self._guest_token:
            self._guest_token = await self._get_guest_token()

        self.cookies = cookies

    async def __get_response__(self, return_raw=False, ignore_none_data=False, is_document=False, **request_data):
        if not self._transaction or not self._guest_token:
            await self._init_local_api()

        new_request = request_data
        new_request["headers"] = self._get_request_headers(request_data.get("headers", {}))
        new_request["cookies"] = self._cookie

        transaction_id = self._transaction.generate_transaction_id(
            new_request["method"],
            urlparse(new_request["url"]).path,
        )
        new_request["headers"]["x-client-transaction-id"] = transaction_id

        response = None
        last_error = None

        for retry in range(self._retries):
            try:
                response = await self._session.request(**new_request)
                break
            except Exception as request_failed:
                last_error = request_failed
                pass

        if not response:
            raise last_error

        await self._update_rate_limit(response, inspect.stack()[1][3])
        await self._update_cookies(response)

        if is_document:
            return response

        response_json = response.json()  # noqa
        if ignore_none_data and len(response.text) == 0:
            return None

        if (not response_json and response.text and response.text.lower() == "rate limit exceeded") or response.status_code == 429:
            response_json = {"errors": [{"code": 88, "message": "Rate limit exceeded."}]}
        elif not response_json and response.status_code in [403, 401]:
            response_json = {"errors": [{"code": 32, "message": "Couldn't authenticate you"}]}

        if not response_json:
            raise TwitterError(
                error_code=response.status_code,
                error_name="Server Error",
                response=response,
                message="Unknown Error Occurs on Twitter"
            )

        if response_json.get("errors") and not response_json.get('data'):
            error = response_json['errors'][0]

            error_code = error.get("code", 0)
            error_message = error.get("message")
            
            # Twitter Captcha solving is a bit unstable , removing it till fixed 
            
            # if int(error_code) in [326] and self._captcha_solver:
            #    self.solve_captcha()
            #    return self.__get_response__(return_raw, ignore_none_data, is_document, **request_data)

            return GenericError(response, error_code, error_message)

        if return_raw:
            return response

        return response_json

    def solve_captcha(self, websiteUrl="https://twitter.com/", blob_data=None):
        if self.user is None:
            token = self._captcha_solver.unlock(constants.LOGIN_SITE_KEY, websiteUrl, blob_data)
        else:
            token = self._captcha_solver.unlock(constants.GENERAL_SITE_KEY, websiteUrl, blob_data)
        return token

    async def get_home_html(self):
        home_page = None
        headers = self._get_request_headers()
        if headers.get("authorization"):
            del headers["authorization"]
        try:
            response = await self._session.request(method="GET", url="https://x.com/?mx=2", headers=headers)

            if response.status_code not in range(200, 300):
                response = await self._session.request(method="GET", url=self._builder.URL_HOME_PAGE, headers=headers)

            home_page = bs4.BeautifulSoup(response.content, 'lxml')
            migration_url = home_page.select_one("meta[http-equiv='refresh']")
            migration_redirection_url = re.search(MIGRATION_REGEX, str(migration_url)) or re.search(MIGRATION_REGEX, str(response.content))

            if migration_redirection_url:
                response = await self._session.request(method="GET", url=migration_redirection_url.group(0), headers=headers)
                home_page = bs4.BeautifulSoup(response.content, 'lxml')
            migration_form = home_page.select_one("form[name='f']") or home_page.select_one(f"form[action='https://x.com/x/migrate']")

            if migration_form:
                url = migration_form.attrs.get("action", 'https://x.com/x/migrate')
                method = migration_form.attrs.get("method", "POST")
                request_payload = {input_field.get("name"): input_field.get("value") for input_field in migration_form.select("input")}
                response = await self._session.request(method=method, url=url, data=request_payload, headers=headers)
                home_page = bs4.BeautifulSoup(response.content, 'lxml')
        except:
            pass
        return home_page

    async def _get_guest_token(self):
        token = None
        this_response = None
        headers = self._get_request_headers()
        try:
            this_response = await self._session.request(**self._builder.get_guest_token(), headers=headers)
            this_response = this_response.json()
            token = this_response.get('guest_token')  # noqa
        except:
            pass

        try:
            if not token:
                request_data = self._builder.get_guest_token_fallback()
                request_data["headers"] = headers
                request_data["headers"] = {"authorization": None, "content-type": None, "x-csrf-token": None}
                this_response = await self._session.request(**request_data, cookies=None)
                guest_token = re.findall(GUEST_TOKEN_REGEX, this_response.text)
                if guest_token:
                    token = guest_token[0]
        except:
            pass

        if not token:
            raise GuestTokenNotFound(response=this_response, message=f"Guest Token couldn't be found")
        return token

    async def verify_cookies(self):
        data = self._builder.get_self_user()
        response = {}
        for i in range(self._retries):
            try:
                response = await self.__get_response__(**data)
                break
            except:
                await asyncio.sleep(0.5)

        user = User(self._client, response)
        if user is None:
            raise InvalidCredentials(None, None, None)

        self.username = user.username
        self.set_user(user)
        return user

    async def get_user_state(self):
        request = self._builder.get_user_state()
        response = await self.__get_response__(**request)
        return response

    async def get_user(self, username=None):
        if not username:
            username = self.username

        request = self._builder.user_by_screen_name(username)
        response = await self.__get_response__(**request)

        if response.get("data"):  # noqa
            return response

        raise UserNotFound(error_code=50, error_name="GenericUserNotFound", response=response)

    async def get_users_by_rest_id(self, user_ids):
        request_data = self._builder.users_by_rest_id([str(i) for i in user_ids])
        response = await self.__get_response__(**request_data)
        return response

    async def login(self, _url, _payload):
        request_data = self._builder.build_flow(_url)
        request_data['json'] = _payload
        request_data["headers"] = {"content-type": "application/json", "x-csrf-token": None}
        response = await self.__get_response__(True, **request_data)
        return response

    async def get_tweets(self, user_id, replies=False, cursor=None):
        request_data = self._builder.user_tweets(user_id=user_id, replies=replies, cursor=cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_medias(self, user_id, cursor=None):
        request_data = self._builder.user_media(user_id=user_id, cursor=cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_highlights(self, user_id, cursor=None):
        request_data = self._builder.user_highlights(user_id=user_id, cursor=cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_likes(self, user_id, cursor=None):
        request_data = self._builder.user_likes(user_id=user_id, cursor=cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_trends(self):
        response = await self.__get_response__(**self._builder.trends())
        return response

    async def perform_search(self, keyword, cursor, filter_):
        if keyword.startswith("#"):
            keyword = f"%23{keyword[1:]}"

        keyword = quote(keyword, safe='"()%')
        request_data = self._builder.search(keyword, cursor, filter_)
        response = await self.__get_response__(**request_data)
        return response

    async def search_typehead(self, q, result_type='events,users,topics,lists'):
        request = self._builder.search_typehead(q, result_type)
        response = await self.__get_response__(**request)
        return response

    async def search_place(self, lat, long, search_term):
        request = self._builder.search_place(lat, long, search_term)
        response = await self.__get_response__(**request)
        return response

    async def get_tweet_detail(self, tweetId, cursor=None):
        if self.user:
            response = await self.__get_response__(**self._builder.tweet_detail(tweetId, cursor))
        else:
            response = await self.__get_response__(**self._builder.tweet_detail_as_guest(tweetId))
        return response

    async def get_tweet_analytics(self, tweet_id):
        request = self._builder.get_tweet_analytics(tweet_id)
        response = await self.__get_response__(**request)
        return response

    async def get_blocked_users(self, cursor):
        request = self._builder.get_blocked_users(cursor)
        response = await self.__get_response__(**request)
        return response

    async def get_tweet_translation(self, tweet_id, target_language):
        request = self._builder.tweet_translate(tweet_id, target_language)
        response = await self.__get_response__(**request)
        return response

    async def get_tweet_edit_history(self, tweet_id):
        response = await self.__get_response__(**self._builder.tweet_edit_history(tweet_id))
        return response

    async def get_mentions(self, user_id, cursor=None):
        response = await self.__get_response__(**self._builder.get_mentions(cursor))
        return response

    async def get_bookmarks(self, cursor=None):
        response = await self.__get_response__(**self._builder.get_bookmarks(cursor))
        return response

    async def bookmark_tweet(self, tweet_id):
        response = await self.__get_response__(**self._builder.bookmark_tweet(tweet_id))
        return response

    async def delete_bookmark_tweet(self, tweet_id):
        response = await self.__get_response__(**self._builder.delete_tweet_bookmark(tweet_id))
        return response

    async def get_initial_inbox(self):
        request = self._builder.get_initial_inbox()
        response = await self.__get_response__(**request)
        return response

    async def get_inbox_updates(self, cursor, active_conversation=None):
        request = self._builder.get_inbox_updates(cursor, active_conversation)
        response = await self.__get_response__(**request)
        return response

    async def get_trusted_inbox(self, max_id):
        response = await self.__get_response__(**self._builder.get_trusted_inbox(max_id))
        return response

    async def get_untrusted_inbox(self, max_id, low_quality=False):
        response = await self.__get_response__(**self._builder.get_untrusted_inbox(max_id, low_quality))
        return response

    async def get_conversation(self, conversation_id, max_id=None):
        response = await self.__get_response__(**self._builder.get_conversation_with_messages(conversation_id, max_id))
        return response

    async def create_conversation_group(self, participants, first_message):
        request_data = self._builder.create_group(participants, first_message)
        response = await self.__get_response__(**request_data)
        return response

    async def update_conversation_name(self, conversation_id, name):
        request_data = self._builder.update_conversation_group_name(conversation_id, name)
        request_data['headers']['content-type'] = f"application/x-www-form-urlencoded"
        response = await self.__get_response__(ignore_none_data=True, **request_data)
        return response

    async def update_conversation_avatar(self, conversation_id, avatar_id):
        request_data = self._builder.update_conversation_group_avatar(conversation_id, avatar_id)
        request_data['headers']['content-type'] = f"application/x-www-form-urlencoded"
        response = await self.__get_response__(ignore_none_data=True, **request_data)
        return response

    async def send_message(self, conversation_id, text, media_id, reply_to_message_id=None, audio_only=False, quote_tweet_id=None):
        request_data = self._builder.send_message(conversation_id, text, media_id, reply_to_message_id, audio_only, quote_tweet_id)
        response = await self.__get_response__(**request_data)
        return response

    async def create_pool(self, pool):
        request_data = self._builder.create_pool(pool)
        response = await self.__get_response__(**request_data)
        return response

    async def poll_vote(self, poll_id, poll_name, tweet_id, choice):
        request_data = self._builder.poll_vote(poll_id, poll_name, tweet_id, choice)
        response = await self.__get_response__(**request_data)
        return response

    async def delete_tweet(self, tweet_id):
        request_data = self._builder.delete_tweet(tweet_id)
        response = await self.__get_response__(**request_data)
        return response

    async def create_tweet(self, text, files, filter_, reply_to, quote_tweet_url, pool, geo, batch_composed):
        if pool:
            response = await self.create_pool(pool)
            pool = response.get('card_uri')

        if len(text) > 280:
            request_data = self._builder.create_note_tweet(text, files, filter_, reply_to, quote_tweet_url, pool, geo)
        else:
            request_data = self._builder.create_tweet(text, files, filter_, reply_to, quote_tweet_url, pool, geo, batch_composed)
        response = await self.__get_response__(**request_data)
        return response

    async def schedule_tweet(self, date, text, files, filter_, reply_to, geo):
        request_data = self._builder.schedule_tweet(date, text, files, filter_, reply_to, geo)
        response = await self.__get_response__(**request_data)
        return response

    async def set_media_set_metadata(self, media_id, alt_text, sensitive_tags):
        request_data = self._builder.set_media_metadata(media_id, alt_text, sensitive_tags)
        response = await self.__get_response__(ignore_none_data=True, **request_data)
        return response

    async def upload_media_init(self, size, mime_type, media_category, source_url):
        request_data = self._builder.upload_media_init(size, mime_type, media_category, source_url)
        response = await self.__get_response__(**request_data)
        return response

    async def upload_media_append(self, media_id, payload, headers, segment_index):
        request_data = self._builder.upload_media_append(media_id, segment_index)
        request_data['headers'] = headers
        request_data['data'] = payload

        response = await self.__get_response__(ignore_none_data=True, **request_data)
        return response

    async def upload_media_finalize(self, media_id, md5_hash):
        request_data = self._builder.upload_media_finalize(media_id, md5_hash)
        response = await self.__get_response__(**request_data)
        return response

    async def upload_media_status(self, media_id):
        request_data = self._builder.upload_media_status(media_id)
        response = await self.__get_response__(**request_data)
        return response

    async def get_home_timeline(self, timeline_type, cursor=None):
        request_data = self._builder.home_timeline(timeline_type, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_tweet_likes(self, tweet_id, cursor=None):
        request_data = self._builder.get_tweet_likes(tweet_id, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_tweet_retweets(self, tweet_id, cursor=None):
        request_data = self._builder.get_tweet_retweets(tweet_id, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_audio_space(self, audio_space_id):
        request_data = self._builder.get_audio_space(audio_space_id)
        response = await self.__get_response__(**request_data)
        return response

    async def get_audio_stream(self, media_key):
        request_data = self._builder.get_audio_stream(media_key)
        response = await self.__get_response__(**request_data)
        return response

    async def like_tweet(self, tweet_id):
        request_data = self._builder.like_tweet(tweet_id)
        response = await self.__get_response__(**request_data)
        return response

    async def unlike_tweet(self, tweet_id):
        request_data = self._builder.unlike_tweet(tweet_id)
        response = await self.__get_response__(**request_data)
        return response

    async def retweet_tweet(self, tweet_id):
        request_data = self._builder.retweet_tweet(tweet_id)
        response = await self.__get_response__(**request_data)
        return response

    async def delete_retweet(self, tweet_id):
        request_data = self._builder.delete_retweet(tweet_id)
        response = await self.__get_response__(**request_data)
        return response

    async def get_user_communities(self, user_id):
        request_data = self._builder.get_user_communities(user_id)
        response = await self.__get_response__(**request_data)
        return response

    async def get_community(self, community_id):
        request_data = self._builder.get_community(community_id)
        response = await self.__get_response__(**request_data)
        return response

    async def get_community_tweets(self, community_id, filter_, cursor):
        request_data = self._builder.get_community_tweets(community_id, filter_, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_community_members(self, community_id, filter_, cursor):
        request_data = self._builder.get_community_members(community_id, filter_, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_tweet_notifications(self, cursor):
        request_data = self._builder.get_new_user_tweet_notification(cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def follow_user(self, user_id):
        request_data = self._builder.follow_user(user_id)
        request_data['headers']['content-type'] = f"application/x-www-form-urlencoded"
        response = await self.__get_response__(**request_data)
        return response

    async def unfollow_user(self, user_id):
        request_data = self._builder.unfollow_user(user_id)
        request_data['headers']['content-type'] = f"application/x-www-form-urlencoded"
        response = await self.__get_response__(**request_data)
        return response
    
    async def block_user(self, user_id):
        request_data = self._builder.block_user(user_id)
        request_data['headers']['content-type'] = f"application/x-www-form-urlencoded"
        response = await self.__get_response__(**request_data)
        return response

    async def unblock_user(self, user_id):
        request_data = self._builder.unblock_user(user_id)
        request_data['headers']['content-type'] = f"application/x-www-form-urlencoded"
        response = await self.__get_response__(**request_data)
        return response

    async def mute_user(self, user_id):
        request_data = self._builder.mute_user(user_id)
        request_data['headers']['content-type'] = f"application/x-www-form-urlencoded"
        response = await self.__get_response__(**request_data)
        return response

    async def unmute_user(self, user_id):
        request_data = self._builder.un_mute_user(user_id)
        request_data['headers']['content-type'] = f"application/x-www-form-urlencoded"
        response = await self.__get_response__(**request_data)
        return response

    async def get_user_followers(self, user_id, cursor=None):
        request_data = self._builder.get_user_followers(user_id, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_user_followings(self, user_id, cursor=None):
        request_data = self._builder.get_user_followings(user_id, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_user_subscribers(self, user_id, cursor=None):
        request_data = self._builder.get_user_subscribers(user_id, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def toggle_user_notifications(self, user_id, action):
        request_data = self._builder.toggle_user_notifications(user_id, action)
        response = await self.__get_response__(**request_data)
        return response

    async def get_lists(self, cursor=None):
        request_data = self._builder.get_lists(cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_list(self, list_id):
        request_data = self._builder.get_list(list_id)
        response = await self.__get_response__(**request_data)
        return response

    async def get_list_members(self, list_id, cursor):
        request_data = self._builder.get_list_member(list_id, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_list_tweets(self, list_id, cursor):
        request_data = self._builder.get_list_tweets(list_id, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def add_list_member(self, list_id, user_id):
        request_data = self._builder.add_member_to_list(list_id, user_id)
        response = await self.__get_response__(**request_data)
        return response

    async def remove_list_member(self, list_id, user_id):
        request_data = self._builder.remove_member_from_list(list_id, user_id)
        response = await self.__get_response__(**request_data)
        return response

    async def create_list(self, name, description, is_private):
        request_data = self._builder.create_list(name, description, is_private)
        response = await self.__get_response__(**request_data)
        return response

    async def delete_list(self, list_id):
        request_data = self._builder.delete_list(list_id)
        response = await self.__get_response__(**request_data)
        return response

    async def gif_search(self, search_term, cursor):
        request_data = self._builder.search_gifs(search_term, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_mutual_friends(self, user_id, cursor):
        request_data = self._builder.get_mutual_friend(user_id, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def get_topic_landing_page(self, topic_id, cursor=None):
        request_data = self._builder.get_topic_landing_page(topic_id, cursor)
        response = await self.__get_response__(**request_data)
        return response

    async def add_group_member(self, member_ids, conversation_id):
        request_data = self._builder.add_member_to_group(member_ids, conversation_id)
        response = await self.__get_response__(**request_data)
        return response

    async def remove_group_member(self, member_ids, conversation_id):
        request_data = self._builder.remove_member_from_group(member_ids, conversation_id)
        response = await self.__get_response__(**request_data)
        return response

    async def pin_tweet(self, tweet_id):
        request_data = self._builder.pin_tweet(tweet_id)
        response = await self.__get_response__(**request_data)
        return response

    async def unpin_tweet(self, tweet_id):
        request_data = self._builder.unpin_tweet(tweet_id)
        response = await self.__get_response__(**request_data)
        return response

    async def get_scheduled_tweets(self):
        request_data = self._builder.get_scheduled_tweet()
        response = await self.__get_response__(**request_data)
        return response

    async def delete_scheduled_tweet(self, tweet_id):
        request_data = self._builder.delete_scheduled_tweet(tweet_id)
        response = await self.__get_response__(**request_data)
        return response

    async def download_media(self, media_url, filename: str = None, progress_callback: Callable[[str, int, int], None] = None):
        filename = os.path.basename(media_url).split("?")[0] if not filename else filename
        headers = self._get_request_headers()

        if media_url.startswith("https://ton.twitter.com") or media_url.startswith("https://ton.x.com"):
            headers['referer'] = "https://x.com/"

        async with self._session.stream('GET', media_url, follow_redirects=True, headers=headers, timeout=600) as response:
            response.raise_for_status()

            try:
                total_size = int(response.headers['content-length'])
            except:
                warnings.warn("Unable to get 'content-length', it will be set to zero")
                total_size = 0

            downloaded = 0
            f = open(filename, 'wb')
            async for chunk in response.aiter_bytes(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)

                if progress_callback:
                    if inspect.iscoroutinefunction(progress_callback):
                        await progress_callback(filename, total_size, downloaded)
                    else:
                        progress_callback(filename, total_size, downloaded)

            f.close()

        return filename
