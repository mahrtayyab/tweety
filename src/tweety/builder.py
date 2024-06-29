import json
import urllib
from urllib.parse import urlencode
import random
from functools import wraps
from .exceptions import DeniedLogin
from . import utils
from .types import HOME_TIMELINE_TYPE_FOR_YOU


def return_with_headers(func):
    @wraps(func)
    def wrapper(self, *arg, **kw):
        request_data = func(self, *arg, **kw)
        if len(request_data) == 2:
            return dict(method=request_data[0], headers={}, url=request_data[1])
        elif len(request_data) == 3:
            return dict(method=request_data[0], headers={}, url=request_data[1], json=request_data[2])
        else:
            return dict(method=request_data[0], headers={}, url=request_data[1], json=request_data[2], data=request_data[3])

    return wrapper


class UrlBuilder:
    URL_GUEST_TOKEN = "https://api.x.com/1.1/guest/activate.json"
    URL_HOME_PAGE = "https://x.com/"
    URL_API_INIT = "https://x.com/i/api/1.1/branch/init.json"
    URL_USER_BY_SCREEN_NAME = "https://x.com/i/api/graphql/qW5u-DAuXpMEG0zA1F7UGQ/UserByScreenName"
    URL_USER_BY_USER_IDS = "https://x.com/i/api/graphql/9UCmrCOmAn6TYy_Y13cSjA/UsersByRestIds"
    URL_USER_TWEETS = "https://x.com/i/api/graphql/WzJjibAcDa-oCjCcLOotcg/UserTweets"
    URL_USER_MEDIAS = "https://x.com/i/api/graphql/cEjpJXA15Ok78yO4TUQPeQ/UserMedia"
    URL_USER_HIGHLIGHTS = "https://x.com/i/api/graphql/eOTTj_P8aj8rRzED2BzzLQ/UserHighlightsTweets"
    URL_USER_LIKES = "https://x.com/i/api/graphql/B8I_QCljDBVfin21TTWMqA/Likes"
    URL_USER_TWEETS_WITH_REPLIES = "https://x.com/i/api/graphql/1-5o8Qhfc2kWlu_2rWNcug/UserTweetsAndReplies"
    URL_TRENDS = "https://x.com/i/api/2/guide.json"
    URL_SEARCH = "https://x.com/i/api/graphql/TQmyZ_haUqANuyBcFBLkUw/SearchTimeline"
    URL_SEARCH_TYPEHEAD = "https://x.com/i/api/1.1/search/typeahead.json"
    URL_GIF_SEARCH = "https://x.com/i/api/1.1/foundmedia/search.json"
    URL_PLACE_SEARCH = "https://x.com/i/api/1.1/geo/places.json"
    URL_TOPIC_LANDING = "https://x.com/i/api/graphql/IY9rfrxdSmamr10ZxvVBxg/TopicLandingPage"
    URL_AUDIO_SPACE_BY_ID = "https://x.com/i/api/graphql/gpc0LEdR6URXZ7HOo42_bQ/AudioSpaceById"
    URL_AUDIO_SPACE_STREAM = "https://x.com/i/api/1.1/live_video_stream/status/{}"
    URL_TWEET_DETAILS = "https://x.com/i/api/graphql/VwKJcAd7zqlBOitPLUrB8A/TweetDetail"
    URL_TWEET_ANALYTICS = "https://x.com/i/api/graphql/vnwexpl0q33_Bky-SROVww/TweetActivityQuery"
    URL_TWEET_TRANSLATE = "https://x.com/i/api/1.1/strato/column/None/tweetId={},destinationLanguage={},translationSource=Some(Google),feature=None,timeout=None,onlyCached=None/translation/service/translateTweet"
    URL_TWEET_DETAILS_AS_GUEST = "https://api.x.com/graphql/Xl5pC_lBk_gcO2ItU39DQw/TweetResultByRestId"
    URL_TWEET_HISTORY = "https://x.com/i/api/graphql/MYJ08HcXJuxtXMXWMP-63w/TweetEditHistory"
    URL_AUSER_INITIAL_INBOX = "https://x.com/i/api/1.1/dm/inbox_initial_state.json"  # noqa
    URL_AUSER_INBOX_UPDATES = "https://x.com/i/api/1.1/dm/user_updates.json"  # noqa
    URL_AUSER_TRUSTED_INBOX = "https://x.com/i/api/1.1/dm/inbox_timeline/trusted.json"  # noqa
    URL_AUSER_UNTRUSTED_INBOX = "https://x.com/i/api/1.1/dm/inbox_timeline/untrusted.json"  # noqa
    URL_AUSER_UPDATE_GROUP_NAME = "https://x.com/i/api/1.1/dm/conversation/{}/update_name.json"  # noqa
    URL_AUSER_UPDATE_GROUP_AVATAR = "https://x.com/i/api/1.1/dm/conversation/{}/update_avatar.json"  # noqa
    URL_AUSER_NOTIFICATION_MENTIONS = "https://x.com/i/api/2/notifications/mentions.json"  # noqa
    URL_AUSER_SETTINGS = "https://api.x.com/1.1/account/settings.json"  # noqa
    URL_AUSER_ADD_GROUP_MEMBER = "https://x.com/i/api/graphql/oBwyQ0_xVbAQ8FAyG0pCRA/AddParticipantsMutation"  # noqa
    URL_AUSER_REMOVE_GROUP_MEMBER = "https://api.x.com/1.1/dm/conversation/{}/remove_participants.json"  # noqa
    URL_AUSER_SEND_MESSAGE = "https://x.com/i/api/1.1/dm/new2.json"  # noqa
    URL_AUSER_CONVERSATION = "https://x.com/i/api/1.1/dm/conversation/{}.json"  # noqa
    URL_AUSER_CREATE_TWEET = "https://x.com/i/api/graphql/oB-5XsHNAbjvARJEc8CZFw/CreateTweet"  # noqa
    URL_AUSER_DELETE_TWEET = "https://x.com/i/api/graphql/VaenaVgh5q5ih7kvyVjgtg/DeleteTweet"  # noqa
    URL_AUSER_CREATE_POOL = "https://caps.x.com/v2/cards/create.json"  # noqa
    URL_AUSER_VOTE_POOL = "https://caps.x.com/v2/capi/passthrough/1"  # noqa
    URL_AUSER_CREATE_TWEET_SCHEDULE = "https://x.com/i/api/graphql/LCVzRQGxOaGnOnYH01NQXg/CreateScheduledTweet"  # noqa
    URL_AUSER_CREATE_MEDIA = "https://upload.x.com/i/media/upload.json"  # noqa
    URL_AUSER_CREATE_MEDIA_METADATA = "https://x.com/i/api/1.1/media/metadata/create.json"  # noqa
    URL_AUSER_BOOKMARK = "https://x.com/i/api/graphql/bN6kl72VsPDRIGxDIhVu7A/Bookmarks"  # noqa
    URL_AUSER_HOME_TIMELINE = "https://x.com/i/api/graphql/1u0Wlkw6Ru1NwBUD-pDiww/HomeTimeline"  # noqa
    URL_AUSER_HOME_TIMELINE_LATEST = "https://x.com/i/api/graphql/9EwYy8pLBOSFlEoSP2STiQ/HomeLatestTimeline"  # noqa
    URL_AUSER_TWEET_FAVOURITERS = "https://x.com/i/api/graphql/yoghorQ6KbhB1qpXefXuLQ/Favoriters"  # noqa
    URL_AUSER_TWEET_RETWEETERS = "https://x.com/i/api/graphql/_nBuZh82i3A0Ohkjw4FqCg/Retweeters"  # noqa
    URL_AUSER_LIKE_TWEET = "https://x.com/i/api/graphql/lI07N6Otwv1PhnEgXILM7A/FavoriteTweet"  # noqa
    URL_AUSER_UNLIKE_TWEET = "https://x.com/i/api/graphql/ZYKSe-w7KEslx3JhSIk5LA/UnfavoriteTweet"  # noqa
    URL_AUSER_BOOKMARK_TWEET = "https://x.com/i/api/graphql/aoDbu3RHznuiSkQ9aNM67Q/CreateBookmark"  # noqa
    URL_AUSER_BOOKMARK_DELETE_TWEET = "https://x.com/i/api/graphql/Wlmlj2-xzyS1GN3a6cj-mQ/DeleteBookmark"  # noqa
    URL_AUSER_POST_TWEET_RETWEET = "https://x.com/i/api/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet"  # noqa
    URL_AUSER_DELETE_TWEET_RETWEET = "https://x.com/i/api/graphql/iQtK4dl5hBmXewYZuEOKVw/DeleteRetweet"  # noqa
    URL_AUSER_CREATE_FRIEND = "https://x.com/i/api/1.1/friendships/create.json"  # noqa
    URL_AUSER_DESTROY_FRIEND = "https://x.com/i/api/1.1/friendships/destroy.json"  # noqa
    URL_AUSER_BLOCK_FRIEND = "https://x.com/i/api/1.1/blocks/create.json"  # noqa
    URL_AUSER_UNBLOCK_FRIEND = "https://x.com/i/api/1.1/blocks/destroy.json"  # noqa
    URL_AUSER_MUTE_USER = "https://x.com/i/api/1.1/mutes/users/create.json"  # noqa
    URL_AUSER_UNMUTE_USER = "https://x.com/i/api/1.1/mutes/users/destroy.json"  # noqa
    URL_AUSER_GET_COMMUNITIES = "https://x.com/i/api/graphql/VwuY9V1tDSzglyc9HsC8dw/CommunitiesMembershipsTimeline"
    URL_AUSER_GET_COMMUNITY = "https://x.com/i/api/graphql/wYwM9x1NTCQKPx50Ih35Tg/CommunitiesFetchOneQuery"  # noqa
    URL_AUSER_GET_COMMUNITY_TWEETS = "https://x.com/i/api/graphql/X3ziwTzWWeaFPsesEwWY-A/CommunityTweetsTimeline"  # noqa
    URL_AUSER_GET_COMMUNITY_TWEETS_TOP = "https://x.com/i/api/graphql/UwEaY0_gBZFCQq-gEnArjg/CommunityTweetsRankedTimeline"  # noqa
    URL_AUSER_GET_COMMUNITY_MEMBERS = "https://x.com/i/api/graphql/uDM1rSTpOPMuhBCf2mun9Q/membersSliceTimeline_Query"  # noqa
    URL_AUSER_GET_COMMUNITY_MEMBERS_MODERATOR = "https://x.com/i/api/graphql/DB68-nKYyzPN8tXKr5xZng/moderatorsSliceTimeline_Query"  # noqa
    URL_AUSER_GET_NOTIFICATION_USER_FOLLOWED = "https://x.com/i/api/2/notifications/device_follow.json"  # noqa
    URL_AUSER_UPDATE_FRIENDSHIP = "https://x.com/i/api/1.1/friendships/update.json"  # noqa
    URL_AUSER_GET_LISTS = "https://x.com/i/api/graphql/xoietOOE63W0cH9LFt4yRA/ListsManagementPageTimeline"  # noqa
    URL_AUSER_GET_LIST = "https://x.com/i/api/graphql/zNcfphEciDXgu0vdIMhSaA/ListByRestId"  # noqa
    URL_AUSER_GET_LIST_MEMBER = "https://x.com/i/api/graphql/WWxrex_8HmKW2dzlPnwtTg/ListMembers"  # noqa
    URL_AUSER_GET_LIST_TWEETS = "https://x.com/i/api/graphql/TXyJ3x6-VnEbkV09UzebUQ/ListLatestTweetsTimeline"  # noqa
    URL_AUSER_ADD_LIST_MEMBER = "https://x.com/i/api/graphql/sw71TVciw1b2nRwV6eDZNA/ListAddMember"  # noqa
    URL_AUSER_DELETE_LIST_MEMBER = "https://x.com/i/api/graphql/kHdBGndqf_JX3ef1T1931A/ListRemoveMember"  # noqa
    URL_AUSER_CREATE_LIST = "https://x.com/i/api/graphql/nHFMQuE4PMED1R0JTN4d-Q/CreateList"  # noqa
    URL_AUSER_DELETE_LIST = "https://x.com/i/api/graphql/UnN9Th1BDbeLjpgjGSpL3Q/DeleteList"  # noqa
    URL_AUSER_GET_USER_FOLLOWERS = "https://x.com/i/api/graphql/ihMPm0x-pC35X86L_nUp_Q/Followers"  # noqa
    URL_AUSER_GET_USER_FOLLOWINGS = "https://x.com/i/api/graphql/bX-gXhcglOa--1gzgDlb8A/Following"  # noqa
    URL_AUSER_GET_USER_SUBSCRIBERS = "https://x.com/i/api/graphql/NHT8e7FjnCS3TP0QfP_OUQ/UserCreatorSubscriptions"  # noqa
    # URL_AUSER_GET_MUTUAL_FRIENDS = "https://x.com/i/api/1.1/friends/following/list.json"  # noqa
    URL_AUSER_GET_MUTUAL_FRIENDS = "https://x.com/i/api/graphql/35Y2QFmL84HIisnm-FHAng/FollowersYouKnow"  # noqa
    URL_AUSER_GET_BLOCKED_USERS = "https://x.com/i/api/graphql/f87G4V_l5E9rJ-Ylw0D-yQ/BlockedAccountsAll"  # noqa
    URL_PIN_TWEET = "https://x.com/i/api/graphql/VIHsNu89pK-kW35JpHq7Xw/PinTweet"  # noqa
    URL_UnPIN_TWEET = "https://x.com/i/api/graphql/BhKei844ypCyLYCg0nwigw/UnpinTweet"  # noqa
    URL_GET_SCHEDULED_TWEETS = "https://x.com/i/api/graphql/ITtjAzvlZni2wWXwf295Qg/FetchScheduledTweets"
    URL_DELETE_SCHEDULED_TWEETS = "https://x.com/i/api/graphql/CTOVqej0JBXAZSwkp1US0g/DeleteScheduledTweet"

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
        features = {
            "hidden_profile_likes_enabled": True,
            "hidden_profile_subscriptions_enabled": True,
            "subscriptions_verification_info_is_identity_verified_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "responsive_web_twitter_article_notes_tab_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": True,
            "subscriptions_verification_info_verified_since_enabled": True,
            "highlights_tweets_tab_ui_enabled": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
            "responsive_web_graphql_timeline_navigation_enabled": True
        }

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_USER_BY_SCREEN_NAME, urlencode(params))

    @return_with_headers
    def users_by_rest_id(self, user_ids):
        variables = {"userIds": user_ids}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True, "rweb_tipjar_consumption_enabled": True}

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_USER_BY_USER_IDS, urlencode(params))

    @return_with_headers
    def user_media(self, user_id, cursor=None):
        variables = {"userId": str(user_id), "count": 20, "includePromotedContent": False,
                     "withClientEventToken": False,
                     "withBirdwatchNotes": True, "withVoice": True, "withV2Timeline": True}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_USER_MEDIAS, urlencode(params))

    @return_with_headers
    def user_highlights(self, user_id, cursor=None):
        variables = {"userId": str(user_id), "count": 20, "includePromotedContent": True, "withVoice": True}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_USER_HIGHLIGHTS, urlencode(params))

    @return_with_headers
    def user_likes(self, user_id, cursor=None):
        variables = {"userId": str(user_id), "count": 20, "includePromotedContent": False,
                     "withClientEventToken": False, "withBirdwatchNotes": True, "withVoice": True,
                     "withV2Timeline": True}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_USER_LIKES, urlencode(params))

    @return_with_headers
    def user_tweets(self, user_id, replies=False, cursor=None):
        if not replies:
            variables = {"userId": str(user_id), "count": 20, "includePromotedContent": True,
                         "withQuickPromoteEligibilityTweetFields": True, "withVoice": True, "withV2Timeline": True}
            features = {"rweb_tipjar_consumption_enabled": True, "rweb_lists_timeline_redesign_enabled": True,
                        "blue_business_profile_image_shape_enabled": True,
                        "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                        "creator_subscriptions_tweet_preview_api_enabled": True,
                        "responsive_web_graphql_timeline_navigation_enabled": True,
                        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                        "tweetypie_unmention_optimization_enabled": True, "vibe_api_enabled": True,
                        "responsive_web_edit_tweet_api_enabled": True,
                        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                        "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                        "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                        "standardized_nudges_misinfo": True,
                        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                        "interactive_text_enabled": True, "responsive_web_text_conversations_enabled": False,
                        "longform_notetweets_rich_text_read_enabled": True,
                        "longform_notetweets_inline_media_enabled": False,
                        "responsive_web_enhance_cards_enabled": False}
            fieldToggles = {"withArticleRichContentState": True, "withGrokAnalyze": True, "withAuxiliaryUserLabels": True, "withArticlePlainText": True}
            url = self.URL_USER_TWEETS
        else:
            variables = {"userId": str(user_id), "count": 20, "includePromotedContent": True, "withCommunity": True,
                         "withVoice": True, "withV2Timeline": True}
            features = {"rweb_tipjar_consumption_enabled": True, "rweb_lists_timeline_redesign_enabled": True,
                        "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                        "creator_subscriptions_tweet_preview_api_enabled": True,
                        "responsive_web_graphql_timeline_navigation_enabled": True,
                        "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                        "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                        "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                        "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                        "responsive_web_twitter_article_tweet_consumption_enabled": True,
                        "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                        "standardized_nudges_misinfo": True,
                        "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                        "longform_notetweets_rich_text_read_enabled": True,
                        "longform_notetweets_inline_media_enabled": True,
                        "responsive_web_media_download_video_enabled": True,
                        "responsive_web_enhance_cards_enabled": False}
            fieldToggles = {"withArticleRichContentState": True, "withGrokAnalyze": True, "withAuxiliaryUserLabels": True, "withArticlePlainText": True}
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
            'include_ext_limited_action_results': True,
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
        features = {"creator_subscriptions_quote_tweet_preview_enabled": True, "articles_preview_enabled": True,
                    "communities_web_enable_tweet_community_results_fetch": True,
                    "rweb_tipjar_consumption_enabled": True, "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "responsive_web_home_pinned_timelines_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False,
                    "rweb_lists_timeline_redesign_enabled": True, "rweb_video_timestamps_enabled": True}
        fieldToggles = {"withArticleRichContentState": True}
        if cursor:
            variables['cursor'] = cursor

        if filter_:
            variables['product'] = filter_
        params = {'variables': str(json.dumps(variables, separators=(',', ':'))),
                  'features': str(json.dumps(features, separators=(',', ':')))}

        return "GET", self._build(self.URL_SEARCH, urlencode(params, safe="()%", quote_via=urllib.parse.quote))

    @return_with_headers
    def search_place(self, lat=None, long=None, search_term=None):
        params = {
            'query_type': 'tweet_compose_location'
        }

        if lat and long:
            params.update({"lat": lat, "long": long})

        if search_term:
            params['search_term'] = search_term

        return "GET", self._build(self.URL_PLACE_SEARCH, urlencode(params))

    @return_with_headers
    def search_typehead(self, q, result_type='events,users,topics,lists'):
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
            'include_entities': '1',
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

        features = {"c9s_tweet_anatomy_moderator_badge_enabled": True,
                    "creator_subscriptions_quote_tweet_preview_enabled": True,
                    "articles_preview_enabled": True,
                    "communities_web_enable_tweet_community_results_fetch": True,
                    "rweb_video_timestamps_enabled": True,
                    "rweb_tipjar_consumption_enabled": True, "rweb_lists_timeline_redesign_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": False, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}
        fieldToggles = {"withArticleRichContentState": True, "withArticlePlainText": True, "withGrokAnalyze": True}

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

        variables = {"tweetId": str(tweet_id), "withCommunity": True,
                     "includePromotedContent": True, "withVoice": True}

        features = {
            "rweb_video_timestamps_enabled": True,
            "articles_preview_enabled": True,
            "creator_subscriptions_quote_tweet_preview_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "communities_web_enable_tweet_community_results_fetch": True,
            "creator_subscriptions_tweet_preview_api_enabled": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "tweetypie_unmention_optimization_enabled": True,
            "responsive_web_edit_tweet_api_enabled": True,
            "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
            "view_counts_everywhere_api_enabled": True,
            "longform_notetweets_consumption_enabled": True,
            "responsive_web_twitter_article_tweet_consumption_enabled": True,
            "tweet_awards_web_tipping_enabled": True,
            "responsive_web_home_pinned_timelines_enabled": True,
            "freedom_of_speech_not_reach_fetch_enabled": True,
            "standardized_nudges_misinfo": True,
            "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
            "longform_notetweets_rich_text_read_enabled": True,
            "longform_notetweets_inline_media_enabled": True,
            "responsive_web_graphql_exclude_directive_enabled": True,
            "verified_phone_label_enabled": True,
            "responsive_web_media_download_video_enabled": True,
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
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True, "rweb_video_timestamps_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "responsive_web_media_download_video_enabled": True,
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
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
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
    def get_initial_inbox(self):
        params = {
            'nsfw_filtering_enabled': 'false',
            'filter_low_quality': 'false',
            'include_quality': 'all',
            'include_profile_interstitial_type': '1',
            'include_blocking': '1',
            'include_blocked_by': '1',
            'include_followed_by': '1',
            'include_want_retweets': '1',
            'include_mute_edge': '1',
            'include_can_dm': '1',
            'include_can_media_tag': '1',
            'include_ext_is_blue_verified': '1',
            'include_ext_verified_type': '1',
            'include_ext_profile_image_shape': '1',
            'skip_status': '1',
            'dm_secret_conversations_enabled': 'false',
            'krs_registration_enabled': 'true',
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': 'true',
            'include_ext_limited_action_results': 'true',
            'include_quote_count': 'true',
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_views': 'true',
            'dm_users': 'true',
            'include_groups': 'true',
            'include_inbox_timelines': 'true',
            'include_ext_media_color': 'true',
            'supports_reactions': 'true',
            'include_ext_edit_control': 'true',
            'include_ext_business_affiliations_label': 'true',
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl,article',
        }

        return "GET", self._build(self.URL_AUSER_INITIAL_INBOX, urlencode(params))

    @return_with_headers
    def get_inbox_updates(self, cursor, active_conversation=None):
        params = {
            'nsfw_filtering_enabled': 'false',
            'filter_low_quality': 'false',
            'include_quality': 'all',
            'dm_secret_conversations_enabled': 'false',
            'krs_registration_enabled': 'true',
            'cards_platform': 'Web-12',
            'include_cards': '1',
            'include_ext_alt_text': 'true',
            'include_ext_limited_action_results': 'true',
            'include_quote_count': 'true',
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_views': 'true',
            'dm_users': 'true',
            'include_groups': 'true',
            'include_inbox_timelines': 'true',
            'include_ext_media_color': 'true',
            'supports_reactions': 'true',
            'include_ext_edit_control': 'true',
            'include_ext_business_affiliations_label': 'true',
            'ext': 'mediaColor,altText,businessAffiliationsLabel,mediaStats,highlightedLabel,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl,article',
            'cursor': cursor
        }

        if active_conversation:
            params['active_conversation_id'] = active_conversation

        return "GET", self._build(self.URL_AUSER_INBOX_UPDATES, urlencode(params))

    @return_with_headers
    def get_trusted_inbox(self, max_id=None):
        params = {
            'filter_low_quality': True,
            'include_quality': 'all',
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
            'count': 100,
            'tweet_mode': 'extended',
            'include_ext_views': True,
            'dm_users': True,
            'include_groups': True,
            'include_inbox_timelines': True,
            'include_ext_media_color': True,
            'supports_reactions': True,
            'include_ext_edit_control': True,
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
        }
        if max_id:
            params['max_id'] = max_id

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
            'dm_users': True,
            'include_groups': True,
            'include_inbox_timelines': True,
            'include_ext_media_color': True,
            'supports_reactions': True,
            'include_ext_edit_control': True,
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,hasNftAvatar,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl',
        }

        return "GET", self._build(self.URL_AUSER_UNTRUSTED_INBOX, urlencode(params))

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
    def add_member_to_group(self, member_ids, conversation_id):
        json_data = {
            'variables': {
                'addedParticipants': member_ids,
                'conversationId': conversation_id,
            },
            'queryId': utils.create_query_id(),
        }

        return "POST", self.URL_AUSER_ADD_GROUP_MEMBER, json_data

    @return_with_headers
    def remove_member_from_group(self, member_ids, conversation_id):
        params = {
            'participant_ids': member_ids,  # "1,2,3"
            'request_id': utils.create_query_id(),
        }

        return "POST", self._build(self.URL_AUSER_REMOVE_GROUP_MEMBER.format(conversation_id), urlencode(params))

    @return_with_headers
    def get_bookmarks(self, cursor=None):
        variables = {"count": 20, "includePromotedContent": True}
        features = {"graphql_timeline_v2_bookmark_timeline": True, "rweb_lists_timeline_redesign_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True,
                    "responsive_web_enhance_cards_enabled": False}
        fieldToggles = {"withAuxiliaryUserLabels": True, "withArticleRichContentState": True}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features)),
                  'fieldToggles': str(json.dumps(fieldToggles))}

        return "GET", self._build(self.URL_AUSER_BOOKMARK, urlencode(params))

    @return_with_headers
    def create_group(self, participants, first_message):
        params = {
            'ext': 'mediaColor,altText,mediaStats,highlightedLabel,voiceInfo,birdwatchPivot,superFollowMetadata,unmentionInfo,editControl,article',
            'include_ext_alt_text': 'true',
            'include_ext_limited_action_results': 'true',
            'include_reply_count': '1',
            'tweet_mode': 'extended',
            'include_ext_views': 'true',
            'include_groups': 'true',
            'include_inbox_timelines': 'true',
            'include_ext_media_color': 'true',
            'supports_reactions': 'true',
        }

        json_data = {
            'recipient_ids': participants,
            'request_id': utils.create_request_id(),
            'text': first_message,
            'cards_platform': 'Web-12',
            'include_cards': 1,
            'include_quote_count': True,
            'dm_users': False
        }

        return "POST", self._build(self.URL_AUSER_SEND_MESSAGE, urlencode(params)), json_data

    @return_with_headers
    def update_conversation_group_name(self, conversation_id, name):
        data = {'name': name}
        url = self.URL_AUSER_UPDATE_GROUP_NAME.format(conversation_id)
        return "POST", url, None, data

    @return_with_headers
    def update_conversation_group_avatar(self, conversation_id, avatar_id):
        data = {'avatar_id': avatar_id}
        url = self.URL_AUSER_UPDATE_GROUP_AVATAR.format(conversation_id)
        return "POST", url, None, data

    @return_with_headers
    def send_message(self, conversation_id, text, media_id=None, reply_to_message_id=None, audio_only=False, quote_tweet_id=None):
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
            'dm_users': False
        }

        if media_id:
            json_data['media_id'] = media_id

            if audio_only:
                json_data["audio_only_media_attachment"] = True

        if reply_to_message_id:
            json_data["reply_to_dm_id"] = reply_to_message_id

        if quote_tweet_id:
            json_data["tweet_id"] = quote_tweet_id

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
    def create_tweet(
            self,
            text,
            files,
            filter_=None,
            reply_to=None,
            quote_tweet_url=None,
            pool=None,
            geo=None,
            batch_compose=False
    ):
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
            "articles_preview_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "rweb_video_timestamps_enabled": True,
            "creator_subscriptions_quote_tweet_preview_enabled": True,
            "c9s_tweet_anatomy_moderator_badge_enabled": True,
            "communities_web_enable_tweet_community_results_fetch": True,
            'tweetypie_unmention_optimization_enabled': True,
            'responsive_web_edit_tweet_api_enabled': True,
            'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            'view_counts_everywhere_api_enabled': True,
            'longform_notetweets_consumption_enabled': True,
            'responsive_web_twitter_article_tweet_consumption_enabled': True,
            'tweet_awards_web_tipping_enabled': True,
            'longform_notetweets_rich_text_read_enabled': True,
            'longform_notetweets_inline_media_enabled': True,
            'responsive_web_graphql_exclude_directive_enabled': True,
            'verified_phone_label_enabled': True,
            'freedom_of_speech_not_reach_fetch_enabled': True,
            'standardized_nudges_misinfo': True,
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
            'responsive_web_media_download_video_enabled': True,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
            'responsive_web_graphql_timeline_navigation_enabled': True,
            'responsive_web_enhance_cards_enabled': False
        }

        fieldToggles = {
            'withArticleRichContentState': True,
            'withAuxiliaryUserLabels': True
        }

        if reply_to:
            variables['reply'] = {
                'exclude_reply_user_ids': [],
                'in_reply_to_tweet_id': reply_to
            }

        if quote_tweet_url:
            variables['attachment_url'] = quote_tweet_url

        if batch_compose:
            variables['batch_compose'] = 'BatchFirst' if not reply_to else 'BatchSubsequent'

        if filter_:
            variables['conversation_control'] = {"mode": filter_}

        if pool:
            variables['card_uri'] = pool

        if geo:
            variables['geo'] = {"place_id": geo}

        json_data = dict(
            variables=variables,
            features=features,
            queryId=utils.create_query_id(),
            fieldToggles=fieldToggles
        )

        return "POST", self.URL_AUSER_CREATE_TWEET, json_data

    @return_with_headers
    def schedule_tweet(
            self,
            date,
            text,
            files,
            filter_=None,
            reply_to=None,
            geo=None
    ):
        media_ids = []

        if files:
            files = [files] if isinstance(files, list) else files
            media_ids = [i["media_id"] for i in utils.create_media_entities(files)]

        variables = {
            'post_tweet_request': {
                'auto_populate_reply_metadata': False,
                'status': text,
                'exclude_reply_user_ids': [],
                'media_ids': media_ids,
            },
            'execute_at': date,
        }

        if reply_to:
            variables["post_tweet_request"]["in_reply_to_status_id"] = reply_to

        if filter_:
            variables['conversation_control'] = {"mode": filter_}

        if geo:
            variables['geo'] = {"place_id": geo}

        json_data = {
            'variables': variables,
            'queryId': utils.create_query_id(),
        }

        return "POST", self.URL_AUSER_CREATE_TWEET_SCHEDULE, json_data

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
            "creator_subscriptions_quote_tweet_preview_enabled" : True,
            "articles_preview_enabled": True,
            "rweb_tipjar_consumption_enabled": True,
            "communities_web_enable_tweet_community_results_fetch": True,
            'rweb_lists_timeline_redesign_enabled': True,
            'responsive_web_graphql_exclude_directive_enabled': True,
            'verified_phone_label_enabled': True,
            'creator_subscriptions_tweet_preview_api_enabled': True,
            'responsive_web_graphql_timeline_navigation_enabled': True,
            'responsive_web_graphql_skip_user_profile_image_extensions_enabled': False,
            'tweetypie_unmention_optimization_enabled': True,
            'responsive_web_edit_tweet_api_enabled': True,
            'graphql_is_translatable_rweb_tweet_is_translatable_enabled': True,
            'view_counts_everywhere_api_enabled': True,
            'longform_notetweets_consumption_enabled': True,
            'responsive_web_twitter_article_tweet_consumption_enabled': True,
            'tweet_awards_web_tipping_enabled': True,
            'freedom_of_speech_not_reach_fetch_enabled': True,
            'standardized_nudges_misinfo': True,
            'tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled': True,
            'longform_notetweets_rich_text_read_enabled': True,
            'longform_notetweets_inline_media_enabled': True,
            'responsive_web_media_download_video_enabled': True,
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
                    "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}
        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_AUSER_TWEET_FAVOURITERS, urlencode(params))

    @return_with_headers
    def get_tweet_retweets(self, tweet_id, cursor=None):
        variables = {"tweetId": tweet_id, "count": 20,
                     "includePromotedContent": True}
        features = {"rweb_lists_timeline_redesign_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}
        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_AUSER_TWEET_RETWEETERS, urlencode(params))

    @return_with_headers
    def get_audio_space(self, audio_space_id):
        variables = {"id": audio_space_id, "isMetatagsQuery": False, "withReplays": True, "withListeners": True}
        features = {"spaces_2022_h2_spaces_communities": True, "spaces_2022_h2_clipping": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True,
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
            'cookie_set_host': 'x.com',
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
    def mute_user(self, user_id):
        data = {
            'user_id': user_id,
        }
        return "POST", self.URL_AUSER_MUTE_USER, None, data

    @return_with_headers
    def un_mute_user(self, user_id):
        data = {
            'user_id': user_id,
        }
        return "POST", self.URL_AUSER_UNMUTE_USER, None, data


    @return_with_headers
    def get_user_followers(self, user_id, cursor=None):
        variables = {"userId": user_id, "count": 50, "includePromotedContent": False}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "responsive_web_home_pinned_timelines_enabled": False,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_USER_FOLLOWERS, urlencode(params))

    @return_with_headers
    def get_user_followings(self, user_id, cursor=None):
        variables = {"userId": user_id, "count": 50, "includePromotedContent": False}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "responsive_web_home_pinned_timelines_enabled": False,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_USER_FOLLOWINGS, urlencode(params))

    @return_with_headers
    def get_user_subscribers(self, user_id, cursor=None):
        variables = {"userId": str(user_id), "count": 20, "includePromotedContent": False}
        features = {"rweb_tipjar_consumption_enabled": True, "responsive_web_graphql_exclude_directive_enabled": True,
                    "verified_phone_label_enabled": True, "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "communities_web_enable_tweet_community_results_fetch": True,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "articles_preview_enabled": True,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True,
                    "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True,
                    "creator_subscriptions_quote_tweet_preview_enabled": False,
                    "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "tweet_with_visibility_results_prefer_gql_media_interstitial_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_USER_SUBSCRIBERS, urlencode(params))

    @return_with_headers
    def get_user_communities(self, user_id):
        variables = {"userId": str(user_id), "withCommunity": True}
        features = {"rweb_tipjar_consumption_enabled": True, "responsive_web_graphql_exclude_directive_enabled": True,
                    "verified_phone_label_enabled": True, "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "communities_web_enable_tweet_community_results_fetch": True,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "articles_preview_enabled": True,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True,
                    "creator_subscriptions_quote_tweet_preview_enabled": True,
                    "freedom_of_speech_not_reach_fetch_enabled": True, "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True, "responsive_web_enhance_cards_enabled": False}

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_AUSER_GET_COMMUNITIES, urlencode(params))
    @return_with_headers
    def get_community(self, community_id):
        variables = {"communityId": community_id, "withDmMuting": False, "withSafetyModeUserFields": False}
        features = {"responsive_web_graphql_exclude_directive_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True, "verified_phone_label_enabled": True}

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_AUSER_GET_COMMUNITY, urlencode(params))

    @return_with_headers
    def get_community_tweets(self, community_id, filter_=None, cursor=None):
        variables = {"count": 20, "communityId": community_id, "withCommunity": True}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}

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
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_LISTS, urlencode(params))

    @return_with_headers
    def get_list(self, list_id):
        variables = {"listId": list_id}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "responsive_web_graphql_timeline_navigation_enabled": True}

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_LIST, urlencode(params))

    @return_with_headers
    def get_list_member(self, list_id, cursor=None):
        variables = {"listId": str(list_id), "count": 50, "withSafetyModeUserFields": True}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_AUSER_GET_LIST_MEMBER, urlencode(params))

    @return_with_headers
    def get_list_tweets(self, list_id, cursor=None):
        variables = {"listId": str(list_id), "count": 50}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "tweetypie_unmention_optimization_enabled": True, "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}

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
                'verified_phone_label_enabled': True,
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
                'verified_phone_label_enabled': True,
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
                'verified_phone_label_enabled': True,
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
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}

        return "GET", self._build(self.URL_AUSER_GET_MUTUAL_FRIENDS, urlencode(params))

    @return_with_headers
    def get_topic_landing_page(self, topic_id, cursor=None):
        variables = {"rest_id": str(topic_id), "context": "{}"}
        features = {"responsive_web_graphql_exclude_directive_enabled": True, "verified_phone_label_enabled": True,
                    "responsive_web_graphql_timeline_navigation_enabled": True,
                    "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                    "creator_subscriptions_tweet_preview_api_enabled": True,
                    "c9s_tweet_anatomy_moderator_badge_enabled": True, "tweetypie_unmention_optimization_enabled": True,
                    "responsive_web_edit_tweet_api_enabled": True,
                    "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                    "view_counts_everywhere_api_enabled": True, "longform_notetweets_consumption_enabled": True,
                    "responsive_web_twitter_article_tweet_consumption_enabled": True,
                    "tweet_awards_web_tipping_enabled": True, "freedom_of_speech_not_reach_fetch_enabled": True,
                    "standardized_nudges_misinfo": True,
                    "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": True,
                    "rweb_video_timestamps_enabled": True, "longform_notetweets_rich_text_read_enabled": True,
                    "longform_notetweets_inline_media_enabled": True,
                    "responsive_web_media_download_video_enabled": True, "responsive_web_enhance_cards_enabled": False}

        if cursor:
            variables['cursor'] = cursor

        params = {'variables': str(json.dumps(variables)), 'features': str(json.dumps(features))}
        return "GET", self._build(self.URL_TOPIC_LANDING, urlencode(params))

    @return_with_headers
    def pin_tweet(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': str(tweet_id),
            },
            'queryId': utils.create_query_id(),
        }

        return "POST", self.URL_PIN_TWEET, json_data

    @return_with_headers
    def unpin_tweet(self, tweet_id):
        json_data = {
            'variables': {
                'tweet_id': str(tweet_id),
            },
            'queryId': utils.create_query_id(),
        }

        return "POST", self.URL_UnPIN_TWEET, json_data

    @return_with_headers
    def get_scheduled_tweet(self):
        params = {'variables': str(json.dumps({"ascending": True}))}
        return "GET", self._build(self.URL_GET_SCHEDULED_TWEETS, urlencode(params))

    @return_with_headers
    def delete_scheduled_tweet(self, tweet_id):
        json_data = {
            'variables': {'scheduled_tweet_id': str(tweet_id)},
            'queryId': utils.create_query_id(),
        }

        return "POST", self.URL_DELETE_SCHEDULED_TWEETS, json_data


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
                        # 'response': "{\"rf\":{\"ee9d114bd114827ce8d4cca456f19b3374321d65f0c52660b185810fef13f85e\":-8,\"a1a6293fd3b347788d825c22dc3f5da69e314776cd4e10978f0508c1727c471e\":124,\"ad9f941bbb8b0a8bbc18aeebb8d5b2b3ee363c68fbde149b7f9ee9945abfe522\":-214,\"c32d5d4020fe0180a3afdee9e931d1c38a436cfa58e511be8f0be534934beba1\":203},\"s\":\"WCdLUtsnS3qdTPMQrei9PN3O7Ln86ojKdsZyfMmr5q0jEsdXE6KR7qrF1eOaKlf75eReaup2xTEuBSAXd55oPEDL79NZtoM5tr33sVgNhL2N2YVLPI7X3h-0Ah2NvS6WaQTbLXK0ShEiGS9z48qalQ-oM5smlxhZhLRL7rS-y9IB_euQooEmwC3Dyn-Ka8uXybagc8C6ENaKBk9cBDkw7CFHBKekunjnKElUr0VGCYuuWJtX2PL4AMkZgBtpD_2PVbl_RN8mZkw7cx5Qbr_dGvo8vNKSmHdCwYFwKz6q38TMXXEEgQw_3BnYpqnhC4P-xDwrR_b3W7S2zZ8rSp6wUgAAAYj7_CMQ\"}",
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

    def ArkoseLogin(self, **login_data):
        captcha_token = login_data["captcha_token"]
        return {
            'flow_token': self.get_flow_token(login_data['json_']),
            'subtask_inputs': [
                {
                    'subtask_id': 'ArkoseLogin',
                    'web_modal': {
                        'completion_deeplink': f'twitter://onboarding/web_modal/next_link?access_token={captcha_token}',
                        'link': 'next_link',
                    },
                },
            ],
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
