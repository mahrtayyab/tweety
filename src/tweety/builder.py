import json
from urllib.parse import urlencode
import random
import string
from functools import wraps

REQUEST_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
REQUEST_PLATFORMS = ['Linux', 'Windows']


def return_with_headers(func):
    @wraps(func)
    def wrapper(self, *arg, **kw):
        method, url = func(self, *arg, **kw)
        return dict(method=method, headers=self._get_headers(), url=url)

    return wrapper


class UrlBuilder:
    URL_GUEST_TOKEN = "https://api.twitter.com/1.1/guest/activate.json"
    URL_API_INIT = "https://twitter.com/i/api/1.1/branch/init.json"
    URL_USER_BY_SCREEN_NAME = "https://twitter.com/i/api/graphql/oUZZZ8Oddwxs8Cd3iW3UEA/UserByScreenName"
    URL_USER_TWEETS = "https://twitter.com/i/api/graphql/WzJjibAcDa-oCjCcLOotcg/UserTweets"
    URL_USER_TWEETS_WITH_REPLIES = "https://twitter.com/i/api/graphql/1-5o8Qhfc2kWlu_2rWNcug/UserTweetsAndReplies"
    URL_TRENDS = "https://twitter.com/i/api/2/guide.json"
    URL_SEARCH = "https://twitter.com/i/api/graphql/nK1dw4oV3k4w5TdtcAdSww/SearchTimeline"
    URL_TWEET_DETAILS = "https://twitter.com/i/api/graphql/3XDB26fBve-MmjHaWTUZxA/TweetDetail"
    URL_AUSER_INBOX = "https://twitter.com/i/api/1.1/dm/user_updates.json"  # noqa
    URL_AUSER_TRUSTED_INBOX = "https://twitter.com/i/api/1.1/dm/inbox_timeline/trusted.json"  # noqa
    URL_AUSER_NOTIFICATION_MENTIONS = "https://twitter.com/i/api/2/notifications/mentions.json"  # noqa
    URL_AUSER_SETTINGS = "https://api.twitter.com/1.1/account/settings.json"  # noqa
    URL_AUSER_SEND_MESSAGE = "https://twitter.com/i/api/1.1/dm/new2.json"  # noqa
    URL_AUSER_CONVERSATION = "https://twitter.com/i/api/1.1/dm/conversation/{}.json"  # noqa

    def __init__(self):
        self.cookies = None
        self.user_id = None
        self.guest_token = None

    def set_cookies(self, cookies):
        if isinstance(cookies, dict):
            self.cookies = cookies
        else:
            self.cookies = dict()
            split_cookies = cookies.split(";")
            for cookie in split_cookies:
                split_cookie = cookie.split("=")

                if len(split_cookie) == 2:
                    key = cookie.split("=")[0]
                    value = cookie.split("=")[1]
                    self.cookies[key] = value

    def _get_headers(self):
        headers = {
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'en-PK,en;q=0.9',
            'authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'content-type': 'application/x-www-form-urlencoded',
            'referer': 'https://twitter.com/',
            'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': f'"{random.choice(REQUEST_PLATFORMS)}"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': REQUEST_USER_AGENT,
            'x-csrf-token': self._get_csrf(),
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'en',
        }

        if self.guest_token or self.cookies:
            headers['content-type'] = 'application/json'
            # headers['referer'] = f'https://twitter.com/{self.username}'
            headers['sec-fetch-site'] = 'same-origin'

            if self.guest_token:
                headers['x-guest-token'] = self.guest_token

        return headers

    def _get_csrf(self):
        if self.cookies and self.cookies.get("ct0"):
            return self.cookies.get("ct0")

        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    @staticmethod
    def _build(url, params):
        return "?".join([url, params])

    @return_with_headers
    def get_guest_token(self):
        return "POST", self.URL_GUEST_TOKEN

    @return_with_headers
    def init_api(self):
        return "POST", self.URL_API_INIT

    @return_with_headers
    def build_flow(self, _url):
        return "POST", _url

    @return_with_headers
    def user_by_screen_name(self, username):
        variables = {"screen_name": str(username), "withSafetyModeUserFields": True}
        features = {"hidden_profile_likes_enabled": False, "responsive_web_graphql_exclude_directive_enabled": True,
                    "verified_phone_label_enabled": False,
                    "subscriptions_verification_info_verified_since_enabled": True,
                    "highlights_tweets_tab_ui_enabled": True, "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True}

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_USER_BY_SCREEN_NAME, urlencode(params))

    @return_with_headers
    def user_tweets(self, user_id, replies=False, cursor=None):
        if not replies:
            variables = {"userId": str(user_id), "count": 20, "includePromotedContent": True,
                         "withQuickPromoteEligibilityTweetFields": True, "withVoice": True, "withV2Timeline": True}
            features = {"rweb_lists_timeline_redesign_enabled": True,
                        "blue_business_profile_image_shape_enabled": True,
                        "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                        "creator_subscriptions_tweet_preview_api_enabled": False,
                        "responsive_web_graphql_timeline_navigation_enabled": True,
                        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                        "tweetypie_unmention_optimization_enabled": True, "vibe_api_enabled": True,
                        "responsive_web_edit_tweet_api_enabled": True,
                        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                        "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                        "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                        "standardized_nudges_misinfo": True,
                        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                        "interactive_text_enabled": True, "responsive_web_text_conversations_enabled": False,
                        "longform_notetweets_rich_text_read_enabled": True,
                        "longform_notetweets_inline_media_enabled": False,
                        "responsive_web_enhance_cards_enabled": False}
            fieldToggles = {"withArticleRichContentState": False}
            url = self.URL_USER_TWEETS
        else:
            variables = {"userId": str(user_id), "count": 20, "includePromotedContent": True, "withCommunity": True,
                         "withVoice": True, "withV2Timeline": True}
            features = {"rweb_lists_timeline_redesign_enabled": True,
                        "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                        "creator_subscriptions_tweet_preview_api_enabled": True,
                        "responsive_web_graphql_timeline_navigation_enabled": True,
                        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                        "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                        "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                        "responsive_web_twitter_article_tweet_consumption_enabled": False,
                        "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                        "standardized_nudges_misinfo": True,
                        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                        "longform_notetweets_rich_text_read_enabled": True,
                        "longform_notetweets_inline_media_enabled": True,
                        "responsive_web_media_download_video_enabled": False,
                        "responsive_web_enhance_cards_enabled": False}
            fieldToggles = {"withAuxiliaryUserLabels": False, "withArticleRichContentState": False}
            url = self.URL_USER_TWEETS_WITH_REPLIES

        if cursor:
            variables['cursor'] = str(cursor)

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features)),
                  'fieldToggles': str(json.dumps(fieldToggles))}

        return "GET", self._build(url, urlencode(params))

    @return_with_headers
    def trends(self):
        params = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_has_nft_avatar': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'skip_status': '1',
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': True,
            'include_ext_limited_action_results': False,
            'include_quote_count': True,
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_collab_control': True,
            'include_ext_views': True,
            'include_entities': True,
            'include_user_entities': True,
            'include_ext_media_color': True,
            'include_ext_media_availability': True,
            'include_ext_sensitive_media_warning': True,
            'include_ext_trusted_friends_metadata': True,
            'send_error_codes': True,
            'simple_quoted_tweet': True,
            'count': '40',
            'requestContext': 'launch',
            'candidate_source': 'trends',
            'include_page_configuration': False,
            'entity_tokens': False,
            'ext': 'mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,enrichments,superFollowMetadata,unmentionInfo,editControl,collab_control,vibe',
        }
        return "GET", self._build(self.URL_TRENDS, urlencode(params))

    @return_with_headers
    def search(self, keyword, cursor, filter_):
        variables = {"rawQuery": str(keyword), "count": 20, "querySource": "typed_query", "product": "Top"}
        features = {"rweb_lists_timeline_redesign_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": False,
                    "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": False, "responsive_web_enhance_cards_enabled": False}
        fieldToggles = {"withArticleRichContentState": False}

        if cursor:
            variables['cursor'] = cursor

        if filter_ and filter_ == "latest":
            variables['product'] = "Latest"
        elif filter_ and filter_ == "users":
            variables['product'] = "People"
        elif filter_ and filter_ == "photos":
            variables['product'] = "Photos"
        elif filter_ and filter_ == "videos":
            variables['product'] = "Videos"

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features)),
                  'fieldToggles': str(json.dumps(fieldToggles))}

        return "GET", self._build(self.URL_SEARCH, urlencode(params))

    @return_with_headers
    def tweet_detail(self, tweet_id, cursor=None):
        variables = {"focalTweetId": str(tweet_id), "with_rux_injections": False,
                     "includePromotedContent": True, "withCommunity": True,
                     "withQuickPromoteEligibilityTweetFields": True, "withBirdwatchNotes": True, "withVoice": True,
                     "withV2Timeline": True}

        features = {"rweb_lists_timeline_redesign_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": False,
                    "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": False, "responsive_web_enhance_cards_enabled": False}
        fieldToggles = {"withArticleRichContentState": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features)),
                  'fieldToggles': str(json.dumps(fieldToggles))}

        return "GET", self._build(self.URL_TWEET_DETAILS, urlencode(params))

    @return_with_headers
    def get_mentions(self, cursor=None):
        params = {
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_has_nft_avatar': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': True,
            'include_ext_limited_action_results': True,
            'include_quote_count': True,
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_views': True,
            'include_entities': True,
            'include_user_entities': True,
            'include_ext_media_color': True,
            'include_ext_media_availability': True,
            'include_ext_sensitive_media_warning': True,
            'include_ext_trusted_friends_metadata': True,
            'send_error_codes': True,
            'simple_quoted_tweet': True,
            'count': '20',
            'requestContext': 'launch',
            'ext': 'mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
        }

        if cursor:
            params['cursor'] = cursor

        return "GET", self._build(self.URL_AUSER_NOTIFICATION_MENTIONS, urlencode(params))

    @return_with_headers
    def get_inbox(self, cursor, active_conversation=None):
        params = {
            'nsfw_filtering_enabled': False,
            'filter_low_quality': True,
            'include_quality': 'all',
            'dm_secret_conversations_enabled': False,
            'krs_registration_enabled': True,
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': True,
            'include_ext_limited_action_results': True,
            'include_quote_count': True,
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_views': True,
            'dm_users': False,
            'include_groups': True,
            'include_inbox_timelines': True,
            'include_ext_media_color': True,
            'supports_reactions': True,
            'include_ext_edit_control': True,
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
        }

        if active_conversation:
            params['active_conversation_id'] = active_conversation

        if cursor:
            params['cursor'] = cursor

        return "GET", self._build(self.URL_AUSER_INBOX, urlencode(params))

    @return_with_headers
    def get_trusted_inbox(self, max_id):
        params = {
            'filter_low_quality': True,
            'include_quality': 'all',
            'max_id': max_id,
            'nsfw_filtering_enabled': False,
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_has_nft_avatar': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'dm_secret_conversations_enabled': False,
            'krs_registration_enabled': True,
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': True,
            'include_ext_limited_action_results': True,
            'include_quote_count': True,
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_views': True,
            'dm_users': False,
            'include_groups': True,
            'include_inbox_timelines': True,
            'include_ext_media_color': True,
            'supports_reactions': True,
            'include_ext_edit_control': True,
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
        }

        return "GET", self._build(self.URL_AUSER_TRUSTED_INBOX, urlencode(params))

    @return_with_headers
    def get_untrusted_inbox(self, max_id, low_quality=False):
        params = {
            'filter_low_quality': True if not low_quality else False,
            'include_quality': 'high',
            'max_id': max_id,
            'nsfw_filtering_enabled': False,
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_has_nft_avatar': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'dm_secret_conversations_enabled': False,
            'krs_registration_enabled': True,
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': True,
            'include_ext_limited_action_results': True,
            'include_quote_count': True,
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_views': True,
            'dm_users': False,
            'include_groups': True,
            'include_inbox_timelines': True,
            'include_ext_media_color': True,
            'supports_reactions': True,
            'include_ext_edit_control': True,
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
        }

        return "GET", self._build(self.URL_AUSER_TRUSTED_INBOX, urlencode(params))

    @return_with_headers
    def get_conversation_with_messages(self, conversation_id, max_id=None):
        params = {
            'context': 'FETCH_DM_CONVERSATION',
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_has_nft_avatar': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'dm_secret_conversations_enabled': 'false',
            'krs_registration_enabled': True,
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': True,
            'include_ext_limited_action_results': True,
            'include_quote_count': True,
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_views': True,
            'dm_users': 'false',
            'include_groups': True,
            'include_inbox_timelines': True,
            'include_ext_media_color': True,
            'supports_reactions': True,
            'include_conversation_info': True,
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
        }

        if max_id:
            params['max_id'] = max_id

        return "GET", self._build(self.URL_AUSER_CONVERSATION.format(conversation_id), urlencode(params))

    @return_with_headers
    def send_message(self):
        params = {
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
            'include_ext_alt_text': True,
            'include_ext_limited_action_results': True,
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_views': True,
            'include_groups': True,
            'include_inbox_timelines': True,
            'include_ext_media_color': True,
            'supports_reactions': True,
        }

        return "POST", self._build(self.URL_AUSER_SEND_MESSAGE, urlencode(params))

    @return_with_headers
    def aUser_settings(self):
        params = {
            'include_mention_filter': True,
            'include_nsfw_user_flag': True,
            'include_nsfw_admin_flag': True,
            'include_ranked_timeline': True,
            'include_alt_text_compose': True,
            'ext': 'ssoConnections',
            'include_country_code': True,
            'include_ext_dm_nsfw_media_filter': True,
            'include_ext_sharing_audiospaces_listening_data_with_followers': True,
        }

        return "GET", self._build(self.URL_AUSER_SETTINGS, urlencode(params))


class FlowData:
    IGNORE_MEMBERS = ['get']

    def __init__(self, username, password, extra):
        self._username = username
        self._password = password
        self._extra = extra
        self.initial_state = "startFlow"

    def get(self, called_member, **kwargs):
        for member in dir(self):
            if member not in self.IGNORE_MEMBERS and callable(getattr(self, member)):
                if member == called_member:
                    return getattr(self, member)(**kwargs)

    @staticmethod
    def get_flow_token(_json):
        return _json['flow_token']

    @staticmethod
    def startFlow(json_, username, password):
        return {
            'input_flow_data': {
                'flow_context': {
                    'debug_overrides': {},
                    'start_location': {
                        'location': 'unknown',
                    },
                },
            },
            'subtask_versions': {
                'action_list': 2,
                'alert_dialog': 1,
                'app_download_cta': 1,
                'check_logged_in_account': 1,
                'choice_selection': 3,
                'contacts_live_sync_permission_prompt': 0,
                'cta': 7,
                'email_verification': 2,
                'end_flow': 1,
                'enter_date': 1,
                'enter_email': 2,
                'enter_password': 5,
                'enter_phone': 2,
                'enter_recaptcha': 1,
                'enter_text': 5,
                'enter_username': 2,
                'generic_urt': 3,
                'in_app_notification': 1,
                'interest_picker': 3,
                'js_instrumentation': 1,
                'menu_dialog': 1,
                'notifications_permission_prompt': 2,
                'open_account': 2,
                'open_home_timeline': 1,
                'open_link': 1,
                'phone_verification': 4,
                'privacy_options': 1,
                'security_key': 3,
                'select_avatar': 4,
                'select_banner': 2,
                'settings_list': 7,
                'show_code': 1,
                'sign_up': 2,
                'sign_up_review': 4,
                'tweet_selection_urt': 1,
                'update_users': 1,
                'upload_media': 1,
                'user_recommendations_list': 4,
                'user_recommendations_urt': 1,
                'wait_spinner': 3,
                'web_modal': 1,
            },
        }

    def LoginJsInstrumentationSubtask(self, json_, username, password):
        return {
            "flow_token": self.get_flow_token(json_),
            "subtask_inputs": [
                {
                    "subtask_id": "LoginJsInstrumentationSubtask",
                    'js_instrumentation': {
                        'response': "{\"rf\":{\"ee9d114bd114827ce8d4cca456f19b3374321d65f0c52660b185810fef13f85e\":-8,\"a1a6293fd3b347788d825c22dc3f5da69e314776cd4e10978f0508c1727c471e\":124,\"ad9f941bbb8b0a8bbc18aeebb8d5b2b3ee363c68fbde149b7f9ee9945abfe522\":-214,\"c32d5d4020fe0180a3afdee9e931d1c38a436cfa58e511be8f0be534934beba1\":203},\"s\":\"WCdLUtsnS3qdTPMQrei9PN3O7Ln86ojKdsZyfMmr5q0jEsdXE6KR7qrF1eOaKlf75eReaup2xTEuBSAXd55oPEDL79NZtoM5tr33sVgNhL2N2YVLPI7X3h-0Ah2NvS6WaQTbLXK0ShEiGS9z48qalQ-oM5smlxhZhLRL7rS-y9IB_euQooEmwC3Dyn-Ka8uXybagc8C6ENaKBk9cBDkw7CFHBKekunjnKElUr0VGCYuuWJtX2PL4AMkZgBtpD_2PVbl_RN8mZkw7cx5Qbr_dGvo8vNKSmHdCwYFwKz6q38TMXXEEgQw_3BnYpqnhC4P-xDwrR_b3W7S2zZ8rSp6wUgAAAYj7_CMQ\"}",
                        'link': 'next_link',
                    }
                }
            ]
        }

    def LoginEnterUserIdentifierSSO(self, json_, username, password):
        return {
            "flow_token": self.get_flow_token(json_),
            'subtask_inputs': [
                {
                    'subtask_id': 'LoginEnterUserIdentifierSSO',
                    'settings_list': {
                        'setting_responses': [
                            {
                                'key': 'user_identifier',
                                'response_data': {
                                    'text_data': {
                                        'result': username,
                                    },
                                },
                            },
                        ],
                        'link': 'next_link',
                    },
                },
            ]
        }

    def LoginEnterPassword(self, json_, username, password):
        return {
            "flow_token": self.get_flow_token(json_),
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterPassword",
                    "enter_password": {
                        "password": password,
                        "link": "next_link"
                    }
                }
            ]
        }

    def AccountDuplicationCheck(self, json_, username, password):
        return {
            "flow_token": self.get_flow_token(json_),
            "subtask_inputs": [
                {
                    "subtask_id": "AccountDuplicationCheck",
                    "check_logged_in_account": {
                        "link": "AccountDuplicationCheck_false"
                    }
                }
            ]
        }

    def LoginEnterAlternateIdentifierSubtask(self, json_, username, password):
        reason = json_['subtasks'][0]['enter_text']['secondary_text']['text']
        print(reason)
        getAlternate = input("> ")
        return {
            "flow_token": self.get_flow_token(json_),
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterAlternateIdentifierSubtask",
                    "enter_text": {
                        "text": getAlternate,
                        "link": "next_link"
                    }
                }
            ]
        }
