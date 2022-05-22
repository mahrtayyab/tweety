import random
import re
import string
import traceback

import requests as s
from .exceptions_ import GuestTokenNotFound, UnknownError
from .utils import get_headers, searchFilters


class Request:
    def __init__(self, profile_url, max_retries=10):
        self.__user_by_screen_url = "https://twitter.com/i/api/graphql/B-dCk4ph5BZ0UReWK590tw/UserByScreenName?variables="
        self.__tweets_url = "https://twitter.com/i/api/graphql/Lya9A5YxHQxhCQJ5IPtm7A/UserTweets?variables="
        self.__tweets_with_replies = "https://twitter.com/i/api/graphql/B9izm_qt4l5qWUWrympCVw/UserTweetsAndReplies?variables="
        self.__trends_url = "https://api.twitter.com/2/guide.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&count=20&candidate_source=trends&include_page_configuration=false&entity_tokens=false&ext=mediaStats%2ChighlightedLabel"
        self.__search_url = "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={}&count=20&query_source=typeahead_click&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2CvoiceInfo"
        self.__user_search_url = "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q={}&result_filter=user&count=20&query_source=recent_search_click&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CsuperFollowMetadata"
        self.__tweet_detail_url = "https://twitter.com/i/api/graphql/4tzuTRu5-fpJTS7bDF6Nlg/TweetDetail?variables=%7B%22focalTweetId%22%3A%22{}%22%2C%22with_rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withTweetQuoteCount%22%3Atrue%2C%22withBirdwatchNotes%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D"
        self.__guest_token_url = "https://api.twitter.com/1.1/guest/activate.json"
        self.__proxy = None
        self.__guest_token = self.__get_guest_token__(profile_url, max_retries)
        self.__guest_headers = get_headers(self.__guest_token)

    def __get_guest_token__(self, profile_url, max_retries=10):
        try:
            guest_token = ""
            for i in range(0, int(max_retries)):
                if profile_url:
                    response = s.get(profile_url, headers=get_headers(), proxies=self.__proxy)
                else:
                    response = s.get("https://twitter.com/i/trends", headers=get_headers(), proxies=self.__proxy)
                guest_token_ = re.findall(
                    'document\.cookie = decodeURIComponent\("gt=(.*?); Max-Age=10800; Domain=\.twitter\.com; Path=/; Secure"\);',
                    response.text)
                try:
                    if guest_token_[0]:
                        guest_token = guest_token_[0]
                        return guest_token
                except IndexError:
                    try:
                        headers = get_headers()
                        headers['x-csrf-token'] = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                        headers[
                            'authorization'] = "Bearer " + "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
                        headers['content-type'] = 'application/x-www-form-urlencoded'
                        headers['accept'] = "*/*"
                        response = s.post(self.__guest_token_url, headers=headers, proxies=self.__proxy)
                        guest_token = response.json()['guest_token']
                        return response.json()['guest_token']
                    except:
                        continue
            if guest_token == "":
                raise GuestTokenNotFound(f"Guest Token couldn't be found after {max_retries} retires.")
        except:
            error = traceback.format_exc().splitlines()[-1]
            raise UnknownError(str(error))

    def verify_user(self, data):
        response = s.get(f"{self.__user_by_screen_url}{data}", headers=self.__guest_headers, proxies=self.__proxy)
        if response.json().get('data'):
            return response.json()
        else:
            return 0

    def get_tweets(self, data, replies=False):
        if replies:
            response = s.get(f"{self.__tweets_with_replies}{data}", headers=self.__guest_headers,proxies=self.__proxy)
        else:
            response = s.get(f"{self.__tweets_url}{data}", headers=self.__guest_headers,proxies=self.__proxy)
        return response

    def get_trends(self):
        response = s.get(f"{self.__trends_url}", headers=self.__guest_headers,proxies=self.__proxy)
        return response

    def perform_search(self,keyword,cursor,filter_):
        if keyword.startswith("#"):
            keyword = f"%23{keyword[1:]}"
        url = searchFilters(filter_=filter_)
        if cursor:
            search_url = f"{url}&cursor={cursor}"
        else:
            search_url = url
        response = s.get(search_url.format(keyword), headers=self.__guest_headers, proxies=self.__proxy)
        return response

    def get_tweet_detail(self,tweetId):
        response = s.get(self.__tweet_detail_url.format(tweetId),headers=self.__guest_headers,proxies=self.__proxy)
        return response
