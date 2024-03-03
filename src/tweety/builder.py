import json
import urllib
from urllib.parse import urlencode
import random
from .exceptions_ import DeniedLogin
from functools import wraps
from . import utils
from .types import HOME_TIMELINE_TYPE_FOR_YOU, HOME_TIMELINE_TYPE_FOLLOWING

REQUEST_USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
REQUEST_PLATFORMS = ['Linux', 'Windows']


def return_with_headers(func):
    @wraps(func)
    def wrapper(self, *arg, **kw):
        request_data = func(self, *arg, **kw)
        if len(request_data) == 2:
            return dict(method=request_data[0], headers=self._get_headers(), url=request_data[1])
        elif len(request_data) == 3:
            return dict(method=request_data[0], headers=self._get_headers(), url=request_data[1], json=request_data[2])
        else:
            return dict(method=request_data[0], headers=self._get_headers(), url=request_data[1], json=request_data[2],
                        data=request_data[3])

    return wrapper


class UrlBuilder:
    URL_GUEST_TOKEN = "https://api.twitter.com/1.1/guest/activate.json"
    URL_HOME_PAGE = "https://twitter.com/"
    URL_API_INIT = "https://twitter.com/i/api/1.1/branch/init.json"
    URL_USER_BY_SCREEN_NAME = "https://twitter.com/i/api/graphql/oUZZZ8Oddwxs8Cd3iW3UEA/UserByScreenName"
    URL_USER_BY_USER_IDS = "https://twitter.com/i/api/graphql/itEhGywpgX9b3GJCzOtSrA/UsersByRestIds"
    URL_USER_TWEETS = "https://twitter.com/i/api/graphql/WzJjibAcDa-oCjCcLOotcg/UserTweets"
    URL_USER_MEDIAS = "https://twitter.com/i/api/graphql/cEjpJXA15Ok78yO4TUQPeQ/UserMedia"
    URL_USER_TWEETS_WITH_REPLIES = "https://twitter.com/i/api/graphql/1-5o8Qhfc2kWlu_2rWNcug/UserTweetsAndReplies"
    URL_TRENDS = "https://twitter.com/i/api/2/guide.json"
    URL_SEARCH = "https://twitter.com/i/api/graphql/Aj1nGkALq99Xg3XI0OZBtw/SearchTimeline"
    URL_SEARCH_TYPEHEAD = "https://twitter.com/i/api/1.1/search/typeahead.json"
    URL_GIF_SEARCH = "https://twitter.com/i/api/1.1/foundmedia/search.json"
    URL_TOPIC_LANDING = "https://twitter.com/i/api/graphql/IY9rfrxdSmamr10ZxvVBxg/TopicLandingPage"
    URL_AUDIO_SPACE_BY_ID = "https://twitter.com/i/api/graphql/gpc0LEdR6URXZ7HOo42_bQ/AudioSpaceById"
    URL_AUDIO_SPACE_STREAM = "https://twitter.com/i/api/1.1/live_video_stream/status/{}"
    URL_TWEET_DETAILS = "https://twitter.com/i/api/graphql/3XDB26fBve-MmjHaWTUZxA/TweetDetail"
    URL_TWEET_ANALYTICS = "https://twitter.com/i/api/graphql/vnwexpl0q33_Bky-SROVww/TweetActivityQuery"
    URL_TWEET_TRANSLATE = "https://twitter.com/i/api/1.1/strato/column/None/tweetId={},destinationLanguage={},translationSource=Some(Google),feature=None,timeout=None,onlyCached=None/translation/service/translateTweet"
    URL_TWEET_DETAILS_AS_GUEST = "https://api.twitter.com/graphql/5GOHgZe-8U2j5sVHQzEm9A/TweetResultByRestId"
    URL_TWEET_HISTORY = "https://twitter.com/i/api/graphql/MYJ08HcXJuxtXMXWMP-63w/TweetEditHistory"
    URL_AUSER_INBOX = "https://twitter.com/i/api/1.1/dm/user_updates.json"  # noqa
    URL_AUSER_TRUSTED_INBOX = "https://twitter.com/i/api/1.1/dm/inbox_timeline/trusted.json"  # noqa
    URL_AUSER_NOTIFICATION_MENTIONS = "https://twitter.com/i/api/2/notifications/mentions.json"  # noqa
    URL_AUSER_SETTINGS = "https://api.twitter.com/1.1/account/settings.json"  # noqa
    URL_AUSER_SEND_MESSAGE = "https://twitter.com/i/api/1.1/dm/new2.json"  # noqa
    URL_AUSER_CONVERSATION = "https://twitter.com/i/api/1.1/dm/conversation/{}.json"  # noqa
    URL_AUSER_CREATE_TWEET = "https://twitter.com/i/api/graphql/tTsjMKyhajZvK4q76mpIBg/CreateTweet"  # noqa
    URL_AUSER_DELETE_TWEET = "https://twitter.com/i/api/graphql/VaenaVgh5q5ih7kvyVjgtg/DeleteTweet"  # noqa
    URL_AUSER_CREATE_POOL = "https://caps.twitter.com/v2/cards/create.json"  # noqa
    URL_AUSER_VOTE_POOL = "https://caps.twitter.com/v2/capi/passthrough/1"  # noqa
    URL_AUSER_CREATE_TWEET_SCHEDULE = "https://twitter.com/i/api/graphql/LCVzRQGxOaGnOnYH01NQXg/CreateScheduledTweet"  # noqa
    URL_AUSER_CREATE_MEDIA = "https://upload.twitter.com/i/media/upload.json"  # noqa
    URL_AUSER_CREATE_MEDIA_METADATA = "https://twitter.com/i/api/1.1/media/metadata/create.json"  # noqa
    URL_AUSER_BOOKMARK = "https://twitter.com/i/api/graphql/bN6kl72VsPDRIGxDIhVu7A/Bookmarks"  # noqa
    URL_AUSER_HOME_TIMELINE = "https://twitter.com/i/api/graphql/W4Tpu1uueTGK53paUgxF0Q/HomeTimeline"  # noqa
    URL_AUSER_HOME_TIMELINE_LATEST = "https://twitter.com/i/api/graphql/IjTuxEFmAb6DvzycVz4fHg/HomeLatestTimeline"  # noqa
    URL_AUSER_TWEET_FAVOURITERS = "https://twitter.com/i/api/graphql/yoghorQ6KbhB1qpXefXuLQ/Favoriters"  # noqa
    URL_AUSER_TWEET_RETWEETERS = "https://twitter.com/i/api/graphql/_nBuZh82i3A0Ohkjw4FqCg/Retweeters"  # noqa
    URL_AUSER_LIKE_TWEET = "https://twitter.com/i/api/graphql/lI07N6Otwv1PhnEgXILM7A/FavoriteTweet"  # noqa
    URL_AUSER_UNLIKE_TWEET = "https://twitter.com/i/api/graphql/ZYKSe-w7KEslx3JhSIk5LA/UnfavoriteTweet"  # noqa
    URL_AUSER_BOOKMARK_TWEET = "https://twitter.com/i/api/graphql/aoDbu3RHznuiSkQ9aNM67Q/CreateBookmark"  # noqa
    URL_AUSER_BOOKMARK_DELETE_TWEET = "https://twitter.com/i/api/graphql/Wlmlj2-xzyS1GN3a6cj-mQ/DeleteBookmark"  # noqa
    URL_AUSER_POST_TWEET_RETWEET = "https://twitter.com/i/api/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet"  # noqa
    URL_AUSER_DELETE_TWEET_RETWEET = "https://twitter.com/i/api/graphql/iQtK4dl5hBmXewYZuEOKVw/DeleteRetweet"  # noqa
    URL_AUSER_CREATE_FRIEND = "https://twitter.com/i/api/1.1/friendships/create.json"  # noqa
    URL_AUSER_DESTROY_FRIEND = "https://twitter.com/i/api/1.1/friendships/destroy.json"  # noqa
    URL_AUSER_BLOCK_FRIEND = "https://twitter.com/i/api/1.1/blocks/create.json"  # noqa
    URL_AUSER_UNBLOCK_FRIEND = "https://twitter.com/i/api/1.1/blocks/destroy.json"  # noqa
    URL_AUSER_GET_COMMUNITY = "https://twitter.com/i/api/graphql/wYwM9x1NTCQKPx50Ih35Tg/CommunitiesFetchOneQuery"  # noqa
    URL_AUSER_GET_COMMUNITY_TWEETS = "https://twitter.com/i/api/graphql/X3ziwTzWWeaFPsesEwWY-A/CommunityTweetsTimeline"  # noqa
    URL_AUSER_GET_COMMUNITY_TWEETS_TOP = "https://twitter.com/i/api/graphql/UwEaY0_gBZFCQq-gEnArjg/CommunityTweetsRankedTimeline"  # noqa
    URL_AUSER_GET_COMMUNITY_MEMBERS = "https://twitter.com/i/api/graphql/uDM1rSTpOPMuhBCf2mun9Q/membersSliceTimeline_Query"  # noqa
    URL_AUSER_GET_COMMUNITY_MEMBERS_MODERATOR = "https://twitter.com/i/api/graphql/DB68-nKYyzPN8tXKr5xZng/moderatorsSliceTimeline_Query"  # noqa
    URL_AUSER_GET_NOTIFICATION_USER_FOLLOWED = "https://twitter.com/i/api/2/notifications/device_follow.json"  # noqa
    URL_AUSER_UPDATE_FRIENDSHIP = "https://twitter.com/i/api/1.1/friendships/update.json"  # noqa
    URL_AUSER_GET_LISTS = "https://twitter.com/i/api/graphql/xoietOOE63W0cH9LFt4yRA/ListsManagementPageTimeline"  # noqa
    URL_AUSER_GET_LIST = "https://twitter.com/i/api/graphql/zNcfphEciDXgu0vdIMhSaA/ListByRestId"  # noqa
    URL_AUSER_GET_LIST_MEMBER = "https://twitter.com/i/api/graphql/WWxrex_8HmKW2dzlPnwtTg/ListMembers"  # noqa
    URL_AUSER_GET_LIST_TWEETS = "https://twitter.com/i/api/graphql/TXyJ3x6-VnEbkV09UzebUQ/ListLatestTweetsTimeline"  # noqa
    URL_AUSER_ADD_LIST_MEMBER = "https://twitter.com/i/api/graphql/sw71TVciw1b2nRwV6eDZNA/ListAddMember"  # noqa
    URL_AUSER_DELETE_LIST_MEMBER = "https://twitter.com/i/api/graphql/kHdBGndqf_JX3ef1T1931A/ListRemoveMember"  # noqa
    URL_AUSER_CREATE_LIST = "https://twitter.com/i/api/graphql/nHFMQuE4PMED1R0JTN4d-Q/CreateList"  # noqa
    URL_AUSER_DELETE_LIST = "https://twitter.com/i/api/graphql/UnN9Th1BDbeLjpgjGSpL3Q/DeleteList"  # noqa
    URL_AUSER_GET_USER_FOLLOWERS = "https://twitter.com/i/api/graphql/ihMPm0x-pC35X86L_nUp_Q/Followers"  # noqa
    URL_AUSER_GET_USER_FOLLOWINGS = "https://twitter.com/i/api/graphql/bX-gXhcglOa--1gzgDlb8A/Following"  # noqa
    # URL_AUSER_GET_MUTUAL_FRIENDS = "https://twitter.com/i/api/1.1/friends/following/list.json"  # noqa
    URL_AUSER_GET_MUTUAL_FRIENDS = "https://twitter.com/i/api/graphql/35Y2QFmL84HIisnm-FHAng/FollowersYouKnow"  # noqa
    URL_AUSER_GET_BLOCKED_USERS = "https://twitter.com/i/api/graphql/f87G4V_l5E9rJ-Ylw0D-yQ/BlockedAccountsAll"  # noqa

    def __init__(self):
        self.cookies = None
        self.user_id = None
        self.guest_token = None
        self.custom_headers = {}

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
            # 'Authority': 'twitter.com',
            'Accept': '*/*',
            'Accept-Language': 'en-PK,en;q=0.9',
            'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://twitter.com/',
            'Sec-Ch-Ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': f'"{random.choice(REQUEST_PLATFORMS)}"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': REQUEST_USER_AGENT,
            'X-Csrf-Token': self._get_csrf(),
            'X-Twitter-Active-User': 'yes',
            'X-Twitter-Client-Language': 'en',
        }

        if self.guest_token or self.cookies:
            headers['Content-Type'] = 'application/json'
            headers['Sec-Fetch-Site'] = 'same-origin'

            if self.cookies:
                headers['X-Twitter-Auth-Type'] = 'OAuth2Session'

            if self.guest_token and not self.cookies:
                headers['X-Guest-Token'] = self.guest_token

        headers.update(self.custom_headers)

        return headers

    def _get_csrf(self):
        if self.cookies and self.cookies.get("ct0"):
            return self.cookies.get("ct0")

        return utils.get_random_string(32)

    @staticmethod
    def _build(url, params):
        return "?".join([url, params])

    @return_with_headers
    def get_guest_token(self):
        return "POST", self.URL_GUEST_TOKEN

    @return_with_headers
    def get_guest_token_fallback(self):
        return "GET", self.URL_HOME_PAGE

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
    def users_by_rest_id(self, user_ids):
        variables = {"userIds" : user_ids}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True}

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_USER_BY_USER_IDS, urlencode(params))

    @return_with_headers
    def user_media(self, user_id, cursor=None):
        variables = {"userId": str(user_id), "count": 20, "includePromotedContent": False,
                     "withClientEventToken": False,
                     "withBirdwatchNotes": False, "withVoice": True, "withV2Timeline": True}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": False,
                    "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": False, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_USER_MEDIAS, urlencode(params))

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
            'count': '100',
            'requestContext': 'launch',
            'candidate_source': 'trends',
            'include_page_configuration': False,
            'entity_tokens': False,
            'ext': 'mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,enrichments,superFollowMetadata,unmentionInfo,editControl,collab_control,vibe',
        }
        return "GET", self._build(self.URL_TRENDS, urlencode(params))

    @return_with_headers
    def search(self, keyword, cursor, filter_):
        keyword = str(keyword)
        variables = {"rawQuery": keyword, "count": 20, "querySource": "typed_query", "product": "Top"}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "responsive_web_home_pinned_timelines_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": False,
                    "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": False, "responsive_web_enhance_cards_enabled": False,
                    "rweb_lists_timeline_redesign_enabled": False, "rweb_video_timestamps_enabled": True}
        fieldToggles = {"withArticleRichContentState": False}
        if cursor:
            variables['cursor'] = cursor

        if filter_:
            variables['product'] = filter_
        params = {'variables': str(json.dumps(variables, separators=(',', ':'))),
                  'features': str(json.dumps(features, separators=(',', ':')))}

        return "GET", self._build(self.URL_SEARCH, urlencode(params, safe="()%", quote_via=urllib.parse.quote))

    @return_with_headers
    def search_typehead(self, q, result_type='events,users,topics,lists'):
        params = {
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'q': str(q),
            'src': 'search_box',
            'result_type': result_type,
        }
        return "GET", self._build(self.URL_SEARCH_TYPEHEAD, urlencode(params))

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
            variables['cursor'], variables['referrer'] = cursor, "tweet"

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features)),
                  'fieldToggles': str(json.dumps(fieldToggles))}

        return "GET", self._build(self.URL_TWEET_DETAILS, urlencode(params))

    @return_with_headers
    def tweet_translate(self, tweet_id, target_language):
        url = self.URL_TWEET_TRANSLATE.format(tweet_id, f"Some({target_language})")
        return "GET", url

    @return_with_headers
    def tweet_detail_as_guest(self, tweet_id):

        variables = {"tweetId": str(tweet_id), "withCommunity": False,
                     "includePromotedContent": True, "withVoice": False}

        features = {
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": False,
            "tweet_awards_web_tipping_enabled": False,
            "responsive_web_home_pinned_timelines_enabled": True,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": False,
            "responsive_web_media_download_video_enabled": False,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True,
            "responsive_web_enhance_cards_enabled": False
        }

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_TWEET_DETAILS_AS_GUEST, urlencode(params))

    @return_with_headers
    def tweet_edit_history(self, tweet_id):

        variables = {"tweetId": str(tweet_id), "withQuickPromoteEligibilityTweetFields": True}

        features = {"c9s_tweet_anatomy_moderator_badge_enabled": True,
                    "freedom_of_speech_not_reach_fetch_enabled": True, "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": False,
                    "tweet_awards_web_tipping_enabled": False, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True, "rweb_video_timestamps_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "responsive_web_media_download_video_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "responsive_web_enhance_cards_enabled": False}

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_TWEET_HISTORY, urlencode(params))

    @return_with_headers
    def get_tweet_analytics(self, tweet_id):
        variables = {"restId": str(tweet_id), "from_time": "2011-01-01T00:00:00.000Z",
                     "to_time": "2050-02-20T14:07:53.617Z", "first_48_hours_time": "2023-12-30T10:36:27.000Z",
                     "requested_organic_metrics": ["DetailExpands", "Engagements", "Follows", "Impressions",
                                                   "LinkClicks", "ProfileVisits"],
                     "requested_promoted_metrics": ["DetailExpands", "Engagements", "Follows", "Impressions",
                                                    "LinkClicks", "ProfileVisits", "CostPerFollower"]}
        features = {"responsive_web_tweet_analytics_m3_enabled": False}
        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_TWEET_ANALYTICS, urlencode(params))

    @return_with_headers
    def get_blocked_users(self, cursor=None):
        variables = {"count": 100, "includePromotedContent": False, "withSafetyModeUserFields": False}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_BLOCKED_USERS, urlencode(params))

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
            'include_ext_business_affiliations_label': True,
            'ext': 'mediaColor,altText,businessAffiliationsLabel,mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
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
    def get_bookmarks(self, cursor=None):
        variables = {"count": 20, "includePromotedContent": True}
        features = {"graphql_timeline_v2_bookmark_timeline": True, "rweb_lists_timeline_redesign_enabled": True,
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

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features)),
                  'fieldToggles': str(json.dumps(fieldToggles))}

        return "GET", self._build(self.URL_AUSER_BOOKMARK, urlencode(params))

    @return_with_headers
    def send_message(self, conversation_id, text, media_id=None):
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

        json_data = {
            'conversation_id': conversation_id,
            'recipient_ids': False,
            'request_id': utils.create_request_id(),
            'text': text,
            'cards_platform': 'Web-12',
            'include_cards': 1,
            'include_quote_count': True,
            'dm_users': False,
        }
        if media_id:
            json_data['media_id'] = media_id

        return "POST", self._build(self.URL_AUSER_SEND_MESSAGE, urlencode(params)), json_data

    @return_with_headers
    def create_pool(self, pool):
        params = {"card_data": pool}

        return "POST", self._build(self.URL_AUSER_CREATE_POOL, urlencode(params))

    @return_with_headers
    def delete_tweet(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': tweet_id,
                'dark_request': False,
            },
            'queryId': utils.create_query_id()
        }

        return "POST", self.URL_AUSER_DELETE_TWEET, json_data

    @return_with_headers
    def create_tweet(self, text, files, filter_=None, reply_to=None, quote_tweet_url=None, pool=None):
        media_entities = utils.create_media_entities(files)
        variables = {
            'tweet_text': text,
            'dark_request': False,
            'media': {
                'media_entities': media_entities,
                'possibly_sensitive': False,
            },
            'semantic_annotation_ids': []
        }

        features = {
            'tweetypie_unmention_optimization_enabled': True,
            'responsive_web_edit_tweet_api_enabled': True,
            'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            'view_counts_everywhere_api_enabled': True,
            'longform_notetweets_consumption_enabled': True,
            'responsive_web_twitter_article_tweet_consumption_enabled': False,
            'tweet_awards_web_tipping_enabled': False,
            'longform_notetweets_rich_text_read_enabled': True,
            'longform_notetweets_inline_media_enabled': True,
            'responsive_web_graphql_exclude_directive_enabled': True,
            'verified_phone_label_enabled': False,
            'freedom_of_speech_not_reach_fetch_enabled': True,
            'standardized_nudges_misinfo': True,
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
            'responsive_web_media_download_video_enabled': False,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
            'responsive_web_graphql_timeline_navigation_enabled': True,
            'responsive_web_enhance_cards_enabled': False
        }

        fieldToggles = {
            'withArticleRichContentState': False,
            'withAuxiliaryUserLabels': False
        }

        if reply_to:
            variables['reply'] = {
                'exclude_reply_user_ids': [],
                'in_reply_to_tweet_id': reply_to
            }
        elif quote_tweet_url:
            variables['attachment_url'] = quote_tweet_url

        if filter_:
            variables['conversation_control'] = {"mode": filter_}

        if pool:
            variables['card_uri'] = pool

        json_data = dict(
            variables=variables,
            features=features,
            queryId=utils.create_query_id(),
            fieldToggles=fieldToggles
        )

        return "POST", self.URL_AUSER_CREATE_TWEET, json_data

    @return_with_headers
    def poll_vote(self, poll_id, poll_name, tweet_id, choice):
        params = {
            'twitter:string:card_uri': poll_id,
            'twitter:long:original_tweet_id': tweet_id,
            'twitter:string:response_card_name': poll_name,
            'twitter:string:cards_platform': 'Web-12',
            'twitter:string:selected_choice': choice,
        }

        return "POST", self._build(self.URL_AUSER_VOTE_POOL, urlencode(params))

    @return_with_headers
    def schedule_create_tweet(self, text, files, time):
        variables = {
            'post_tweet_request': {
                'auto_populate_reply_metadata': False,
                'status': text,
                'exclude_reply_user_ids': [],
                'media_ids': files
            },
            'execute_at': time,
        }
        json_data = dict(
            variables=variables,
            queryId=utils.create_query_id()
        )

        return "POST", self.URL_AUSER_CREATE_TWEET_SCHEDULE, json_data

    @return_with_headers
    def set_media_metadata(self, media_id, alt_text, sensitive_tags):
        if not sensitive_tags:
            sensitive_tags = []

        sensitive_media = utils.check_sensitive_media_tags(sensitive_tags)
        json_data = {
            'media_id': media_id,
            'alt_text': {
                'text': alt_text,
            }
        }
        if sensitive_media:
            json_data['sensitive_media_warning'] = sensitive_media

        return "POST", self.URL_AUSER_CREATE_MEDIA_METADATA, json_data

    @return_with_headers
    def upload_media_init(self, size, mime_type, media_category, source_url=None):
        params = {
            'command': 'INIT',
            'total_bytes': str(int(size)),
            'media_type': mime_type,
            'media_category': media_category,
        }

        if source_url:
            del params['total_bytes']
            params['source_url'] = source_url

        return 'POST', self._build(self.URL_AUSER_CREATE_MEDIA, urlencode(params))

    @return_with_headers
    def upload_media_append(self, media_id, segment_index):
        params = {
            'command': 'APPEND',
            'media_id': media_id,
            'segment_index': segment_index,
        }
        return 'POST', self._build(self.URL_AUSER_CREATE_MEDIA, urlencode(params))

    @return_with_headers
    def upload_media_finalize(self, media_id, md5_hash=None):
        params = {
            'command': 'FINALIZE',
            'media_id': media_id
        }

        if md5_hash:
            params['original_md5'] = md5_hash

        return 'POST', self._build(self.URL_AUSER_CREATE_MEDIA, urlencode(params))

    @return_with_headers
    def upload_media_status(self, media_id):
        params = {
            'command': 'STATUS',
            'media_id': media_id,
        }
        return 'GET', self._build(self.URL_AUSER_CREATE_MEDIA, urlencode(params))

    @return_with_headers
    def home_timeline(self, timeline_type, cursor=None):
        variables = {
            'count': 20,
            'includePromotedContent': True,
            'latestControlAvailable': True,
            'requestContext': 'launch',
            'withCommunity': True,
            'seenTweetIds': [],
        }
        features = {
            'rweb_lists_timeline_redesign_enabled': True,
            'responsive_web_graphql_exclude_directive_enabled': True,
            'verified_phone_label_enabled': False,
            'creator_subscriptions_tweet_preview_api_enabled': True,
            'responsive_web_graphql_timeline_navigation_enabled': True,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
            'tweetypie_unmention_optimization_enabled': True,
            'responsive_web_edit_tweet_api_enabled': True,
            'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            'view_counts_everywhere_api_enabled': True,
            'longform_notetweets_consumption_enabled': True,
            'responsive_web_twitter_article_tweet_consumption_enabled': False,
            'tweet_awards_web_tipping_enabled': False,
            'freedom_of_speech_not_reach_fetch_enabled': True,
            'standardized_nudges_misinfo': True,
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
            'longform_notetweets_rich_text_read_enabled': True,
            'longform_notetweets_inline_media_enabled': True,
            'responsive_web_media_download_video_enabled': False,
            'responsive_web_enhance_cards_enabled': False, 'rweb_video_timestamps_enabled': True,
            'c9s_tweet_anatomy_moderator_badge_enabled': True
        }
        queryId = utils.create_query_id()

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features)),
                  'queryId': str(queryId)}

        if timeline_type == HOME_TIMELINE_TYPE_FOR_YOU:
            url = self.URL_AUSER_HOME_TIMELINE
        else:
            url = self.URL_AUSER_HOME_TIMELINE_LATEST

        return "GET", self._build(url, urlencode(params))

    @return_with_headers
    def get_tweet_likes(self, tweet_id, cursor=None):
        variables = {"tweetId": tweet_id, "count": 20,
                     "includePromotedContent": True}
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
        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_AUSER_TWEET_FAVOURITERS, urlencode(params))

    @return_with_headers
    def get_tweet_retweets(self, tweet_id, cursor=None):
        variables = {"tweetId": tweet_id, "count": 20,
                     "includePromotedContent": True}
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
        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_AUSER_TWEET_RETWEETERS, urlencode(params))

    @return_with_headers
    def get_audio_space(self, audio_space_id):
        variables = {"id": audio_space_id, "isMetatagsQuery": False, "withReplays": True, "withListeners": True}
        features = {"spaces_2022_h2_spaces_communities": True, "spaces_2022_h2_clipping": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
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
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_enhance_cards_enabled": False}

        params = {
            'variables': json.dumps(variables),
            'features': json.dumps(features),
        }
        return "GET", self._build(self.URL_AUDIO_SPACE_BY_ID, urlencode(params))

    @return_with_headers
    def get_audio_stream(self, media_key):
        params = {
            'client': 'web',
            'use_syndication_guest_id': 'false',
            'cookie_set_host': 'twitter.com',
        }

        return "GET", self._build(self.URL_AUDIO_SPACE_STREAM.format(media_key), urlencode(params))

    @return_with_headers
    def like_tweet(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': tweet_id
            },
            'queryId': utils.create_query_id()
        }

        return "POST", self.URL_AUSER_LIKE_TWEET, json_data

    @return_with_headers
    def unlike_tweet(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': tweet_id
            },
            'queryId': utils.create_query_id()
        }

        return "POST", self.URL_AUSER_UNLIKE_TWEET, json_data

    @return_with_headers
    def bookmark_tweet(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': tweet_id
            },
            'queryId': utils.create_query_id()
        }

        return "POST", self.URL_AUSER_BOOKMARK_TWEET, json_data

    @return_with_headers
    def delete_tweet_bookmark(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': tweet_id
            },
            'queryId': utils.create_query_id()
        }

        return "POST", self.URL_AUSER_BOOKMARK_DELETE_TWEET, json_data

    @return_with_headers
    def retweet_tweet(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': tweet_id,
                'dark_request': False,
            },
            'queryId': utils.create_query_id()
        }

        return "POST", self.URL_AUSER_POST_TWEET_RETWEET, json_data

    @return_with_headers
    def delete_retweet(self, tweet_id):
        json_data = {
            'variables': {
                'source_tweet_id': str(tweet_id),
                'dark_request': False,
            },
            'queryId': utils.create_query_id(),
        }
        return "POST", self.URL_AUSER_DELETE_TWEET_RETWEET, json_data

    @return_with_headers
    def follow_user(self, user_id):
        data = {
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
            'user_id': user_id,
        }

        return "POST", self.URL_AUSER_CREATE_FRIEND, None, data

    @return_with_headers
    def unfollow_user(self, user_id):
        data = {
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
            'user_id': user_id,
        }

        return "POST", self.URL_AUSER_DESTROY_FRIEND, None, data

    @return_with_headers
    def block_user(self, user_id):
        data = {
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
            'user_id': user_id,
        }

        return "POST", self.URL_AUSER_BLOCK_FRIEND, None, data

    @return_with_headers
    def unblock_user(self, user_id):
        data = {
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
            'user_id': user_id,
        }

        return "POST", self.URL_AUSER_UNBLOCK_FRIEND, None, data

    @return_with_headers
    def get_user_followers(self, user_id, cursor=None):
        variables = {"userId": user_id, "count": 50, "includePromotedContent": False}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "responsive_web_home_pinned_timelines_enabled": False,
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

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_USER_FOLLOWERS, urlencode(params))

    @return_with_headers
    def get_user_followings(self, user_id, cursor=None):
        variables = {"userId": user_id, "count": 50, "includePromotedContent": False}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "responsive_web_home_pinned_timelines_enabled": False,
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

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_USER_FOLLOWINGS, urlencode(params))

    @return_with_headers
    def get_community(self, community_id):
        variables = {"communityId": community_id, "withDmMuting": False, "withSafetyModeUserFields": False}
        features = {"responsive_web_graphql_exclude_directive_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True, "verified_phone_label_enabled": False}

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_AUSER_GET_COMMUNITY, urlencode(params))

    @return_with_headers
    def get_community_tweets(self, community_id, filter_=None, cursor=None):
        variables = {"count": 20, "communityId": community_id, "withCommunity": True}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
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

        if cursor:
            variables['cursor'] = cursor

        if filter_ and filter_.lower() == "top":
            url = self.URL_AUSER_GET_COMMUNITY_TWEETS_TOP
        else:
            url = self.URL_AUSER_GET_COMMUNITY_TWEETS

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(url, urlencode(params))

    @return_with_headers
    def get_community_members(self, community_id, filter_=None, cursor=None):
        variables = {"communityId": community_id, "cursor": cursor}
        features = {"responsive_web_graphql_timeline_navigation_enabled": True}

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        if filter_ and filter_.lower() == "mods":
            url = self.URL_AUSER_GET_COMMUNITY_MEMBERS_MODERATOR
        else:
            url = self.URL_AUSER_GET_COMMUNITY_MEMBERS

        return "GET", self._build(url, urlencode(params))

    @return_with_headers
    def get_new_user_tweet_notification(self, cursor=None):
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
            'count': '50',
            'ext': 'mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
        }

        if cursor:
            params['cursor'] = cursor

        return "GET", self._build(self.URL_AUSER_GET_NOTIFICATION_USER_FOLLOWED, urlencode(params))

    @return_with_headers
    def toggle_user_notifications(self, user_id, action):
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
            'cursor': '-1',
            'id': user_id,
            'device': action,
        }

        return "POST", self._build(self.URL_AUSER_UPDATE_FRIENDSHIP, urlencode(params))

    @return_with_headers
    def get_lists(self, cursor=None):
        variables = {"count": 100}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
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

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_LISTS, urlencode(params))

    @return_with_headers
    def get_list(self, list_id):
        variables = {"listId": list_id}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True}

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_LIST, urlencode(params))

    @return_with_headers
    def get_list_member(self, list_id, cursor=None):
        variables = {"listId": str(list_id), "count": 50, "withSafetyModeUserFields": True}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
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

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_LIST_MEMBER, urlencode(params))

    @return_with_headers
    def get_list_tweets(self, list_id, cursor=None):
        variables = {"listId": str(list_id), "count": 50}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
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

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_LIST_TWEETS, urlencode(params))

    @return_with_headers
    def create_list(self, name, description, is_private):
        json_data = {
            'variables': {
                'isPrivate': is_private,
                'name': name,
                'description': description,
            },
            'features': {
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': False,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'responsive_web_graphql_timeline_navigation_enabled': True,
            },
            'queryId': utils.create_query_id(),
        }

        return "POST", self.URL_AUSER_CREATE_LIST, json_data

    @return_with_headers
    def delete_list(self, list_id):
        json_data = {
            'variables': {
                'listId': str(list_id),
            },
            'queryId': utils.create_query_id(),
        }

        return "POST", self.URL_AUSER_DELETE_LIST, json_data

    @return_with_headers
    def add_member_to_list(self, list_id, user_id):
        json_data = {
            'variables': {
                'listId': str(list_id),
                'userId': str(user_id),
            },
            'features': {
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': False,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'responsive_web_graphql_timeline_navigation_enabled': True,
            },
            'queryId': utils.create_query_id(),
        }

        return "POST", self.URL_AUSER_ADD_LIST_MEMBER, json_data

    @return_with_headers
    def remove_member_from_list(self, list_id, user_id):
        json_data = {
            'variables': {
                'listId': str(list_id),
                'userId': str(user_id),
            },
            'features': {
                'responsive_web_graphql_exclude_directive_enabled': True,
                'verified_phone_label_enabled': False,
                'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
                'responsive_web_graphql_timeline_navigation_enabled': True,
            },
            'queryId': utils.create_query_id(),
        }

        return "POST", self.URL_AUSER_DELETE_LIST_MEMBER, json_data

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

    @return_with_headers
    def search_gifs(self, search_term, cursor=None):
        params = {
            'q': search_term
        }
        if cursor:
            params['cursor'] = cursor

        return "GET", self._build(self.URL_GIF_SEARCH, urlencode(params))

    @return_with_headers
    def get_mutual_friend(self, user_id, cursor):
        variables = {"userId": str(user_id), "count": 20, "includePromotedContent": False}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": False, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_AUSER_GET_MUTUAL_FRIENDS, urlencode(params))

    @return_with_headers
    def get_topic_landing_page(self, topic_id, cursor=None):
        variables = {"rest_id": str(topic_id), "context": "{}"}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": False, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_TOPIC_LANDING, urlencode(params))


class FlowData:
    IGNORE_MEMBERS = ['get']

    def __init__(self):
        self.initial_state = "startFlow"

    def get(self, called_member, **kwargs):
        if called_member is None:
            return self.startFlow(**kwargs)

        for member in dir(self):
            if member not in self.IGNORE_MEMBERS and callable(getattr(self, member)):
                if member == called_member:
                    return getattr(self, member)(**kwargs)

    @staticmethod
    def get_flow_token(_json):
        return _json['flow_token']

    @staticmethod
    def startFlow(**kwargs):
        return {
            'input_flow_data': {
                'flow_context': {
                    'debug_overrides': {},
                    'start_location': {
                        'location': 'splash_screen',
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

    def LoginJsInstrumentationSubtask(self, **login_data):
        return {
            "flow_token": self.get_flow_token(login_data['json_']),
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

    def LoginEnterUserIdentifierSSO(self, **login_data):
        return {
            "flow_token": self.get_flow_token(login_data['json_']),
            'subtask_inputs': [
                {
                    'subtask_id': 'LoginEnterUserIdentifierSSO',
                    'settings_list': {
                        'setting_responses': [
                            {
                                'key': 'user_identifier',
                                'response_data': {
                                    'text_data': {
                                        'result': login_data['username'],
                                    },
                                },
                            },
                        ],
                        'link': 'next_link',
                    },
                },
            ]
        }

    def LoginEnterPassword(self, **login_data):
        return {
            "flow_token": self.get_flow_token(login_data['json_']),
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterPassword",
                    "enter_password": {
                        "password": login_data['password'],
                        "link": "next_link"
                    }
                }
            ]
        }

    def AccountDuplicationCheck(self, **login_data):
        return {
            "flow_token": self.get_flow_token(login_data['json_']),
            "subtask_inputs": [
                {
                    "subtask_id": "AccountDuplicationCheck",
                    "check_logged_in_account": {
                        "link": "AccountDuplicationCheck_false"
                    }
                }
            ]
        }

    def LoginEnterAlternateIdentifierSubtask(self, **login_data):
        return {
            "flow_token": self.get_flow_token(login_data['json_']),
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterAlternateIdentifierSubtask",
                    "enter_text": {
                        "text": login_data['extra'],
                        "link": "next_link"
                    }
                }
            ]
        }

    def LoginAcid(self, **login_data):
        return {
            "flow_token": self.get_flow_token(login_data['json_']),
            "subtask_inputs": [
                {
                    "subtask_id": "LoginAcid",
                    "enter_text": {
                        "text": login_data['extra'],
                        "link": "next_link"
                    }
                }
            ]
        }

    def LoginTwoFactorAuthChallenge(self, **login_data):
        return {
            "flow_token": self.get_flow_token(login_data['json_']),
            "subtask_inputs": [
                {
                    "subtask_id": "LoginTwoFactorAuthChallenge",
                    "enter_text": {
                        "text": login_data['extra'],
                        "link": "next_link"
                    }
                }
            ]
        }

    @staticmethod
    def DenyLoginSubtask(**login_data):
        text = login_data['json_']['subtasks'][0]['cta']['primary_text']['text']
        secondary_text = login_data['json_']['subtasks'][0]['cta']['secondary_text']['text'].replace('\n', '')
        raise DeniedLogin(
            error_code=37,
            error_name="GenericAccessDenied",
            response=None,
            message=f"{text} : {secondary_text}"
        )
