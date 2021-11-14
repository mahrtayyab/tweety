import pprint
import re
import openpyxl
from _types import TweetDict
from utils import *
import traceback
import requests as s


class Twitter:
    def __init__(self, profile_name=None):
        if profile_name:
            if profile_name.startswith("https://"):
                self.profile_url = profile_name
            else:
                self.profile_url = f"https://twitter.com/{profile_name}"
        else:
            self.profile_url = None
        self.user_by_screen_url = "https://twitter.com/i/api/graphql/B-dCk4ph5BZ0UReWK590tw/UserByScreenName?variables="
        self.tweets_url = "https://twitter.com/i/api/graphql/Lya9A5YxHQxhCQJ5IPtm7A/UserTweets?variables="
        self.trends_url = "https://api.twitter.com/2/guide.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&count=20&candidate_source=trends&include_page_configuration=false&entity_tokens=false&ext=mediaStats%2ChighlightedLabel"
        self.search_url = "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={}&count=20&query_source=typeahead_click&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2CvoiceInfo"
        self.tweet_detail_url = "https://twitter.com/i/api/graphql/4tzuTRu5-fpJTS7bDF6Nlg/TweetDetail?variables=%7B%22focalTweetId%22%3A%22{}%22%2C%22with_rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withTweetQuoteCount%22%3Atrue%2C%22withBirdwatchNotes%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D"
        self.proxy = {"http": random.choice(proxyFactory())}
        self.guest_token = self.__get_guest_token()
        self.guest_headers = get_headers(self.guest_token)

    def __get_guest_token(self):
        try:
            if self.profile_url:
                response = s.get(self.profile_url, headers=get_headers(), proxies=self.proxy)
            else:
                response = s.get("https://twitter.com/i/trends", headers=get_headers(), proxies=self.proxy)
            guest_token = re.findall(
                'document\.cookie = decodeURIComponent\("gt=(.*?); Max-Age=10800; Domain=\.twitter\.com; Path=/; Secure"\);',
                response.text)
            try:
                return guest_token[0]
            except IndexError:
                raise ValueError("Guest Token Couldn't be found, Aborting.")
        except:
            traceback.print_exc()
            exit(1)

    def __verify_user(self):
        user = self.profile_url.split("/")[-1]
        data = str(get_graph_ql_query(2, user))
        response = s.get(f"{self.user_by_screen_url}{data}", headers=self.guest_headers,
                         proxies=self.proxy)
        try:
            if response.json()['data']['user']['result']['legacy']['profile_banner_extensions']:
                json_ = response.json()
                return json_
        except:
            return {"error":"Either User not Found or is Restricted"}

    def get_user_info(self, banner_extensions=False, image_extensions=False):
        try:
            if self.profile_url:
                json_ = self.__verify_user()
                try:
                    if "error" in json_:
                        return json_
                    else:
                        if not banner_extensions or banner_extensions is False:
                            del json_['data']['user']['result']['legacy']['profile_banner_extensions']
                        if not image_extensions or image_extensions is False:
                            del json_['data']['user']['result']['legacy']['profile_image_extensions']
                        return json_
                except:
                    return json_
            else:
                raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")
        except:
            traceback.print_exc()
            exit(1)

    def get_user_id(self):
        try:
            if self.profile_url:
                user = self.get_user_info()
                try:
                    if "error" in user:
                        return 0
                    else:
                        return user['data']['user']['result']['rest_id']
                except:
                    return 0
            else:
                raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")
        except:
            traceback.print_exc()
            exit(1)

    def get_tweets(self,pages=None,include_extras=False,simplify=True) -> TweetDict:
        try:
            if self.profile_url:
                user_id = self.get_user_id()
                if user_id == 0:
                    return TweetDict({"error":"Either User not Found or is Restricted"})
                else:
                    result = {"tweets":[]}
                    data = str(get_graph_ql_query(1, user_id))
                    response = s.get(f"{self.tweets_url}{data}", headers=self.guest_headers,
                                     proxies=self.proxy)
                    tweet,__nextCursor = format_tweet_json(response,include_extras=include_extras,simplify=simplify)
                    result['tweets'].append(tweet)
                    if not pages or pages == 1 or pages == "1":
                        return TweetDict(result)
                    else:
                        for io in range(2, pages + 1):
                            nextCursor = __nextCursor[0]
                            data = str(get_graph_ql_query(1, user_id, nextCursor))
                            response = s.get(f"{self.tweets_url}{data}", headers=self.guest_headers,
                                             proxies=self.proxy)
                            tweet, __nextCursor = format_tweet_json(response,include_extras=include_extras,simplify=simplify)
                            result['tweets'].append(tweet)
                    return TweetDict(result)
            else:
                raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")
        except:
            traceback.print_exc()
            exit(1)

    def get_trends(self) -> dict:
        trends = {
            "trends":[]
        }
        response = s.get(f"{self.trends_url}", headers=self.guest_headers,
                         proxies=self.proxy)
        for i in response.json()['timeline']['instructions'][1]['addEntries']['entries'][1]['content']['timelineModule']['items']:
            data = {
                "name":i['item']['content']['trend']['name'],
                "url": str(i['item']['content']['trend']['url']['url']).replace("twitter://","https://twitter.com/").replace("query","q"),
            }
            try:
                if i['item']['content']['trend']['trendMetadata']['metaDescription']:
                    data['tweet_count'] = i['item']['content']['trend']['trendMetadata']['metaDescription']
            except:
                pass
            trends['trends'].append(data)
        return trends

    def search(self, keyword, pages=1, simplify=True, latest=False) ->TweetDict:
        if keyword.startswith("#"):
            keyword = f"%23{keyword[1:]}"
        if latest is False:
            r = s.get(self.search_url.format(keyword), headers=self.guest_headers, proxies=self.proxy)
        else:
            url = f"{self.search_url}&tweet_search_mode=live"
            r = s.get(url.format(keyword), headers=self.guest_headers, proxies=self.proxy)
        result = {"tweets":[]}
        tweets_, __cursor = format_search(r, simplify)
        result['tweets'].append(tweets_)
        if not pages or pages == 1 or pages == "1":
            return TweetDict(result)
        else:
            for io in range(2, pages + 1):
                try:
                    nextCursor = __cursor[0]
                    if latest is False:
                        url = f"{self.search_url}&cursor={nextCursor}"
                    else:
                        url = f"{self.search_url}&tweet_search_mode=live&cursor={nextCursor}"
                    r = s.get(url.format(keyword), headers=self.guest_headers, proxies=self.proxy)
                    tweets_, __cursor = format_search(r, simplify)
                    result['tweets'].append(tweets_)
                except:
                    pass
        return TweetDict(result)

    def tweet_detail(self,identifier):
        if str(identifier).startswith("https://"):
            if str(identifier).endswith("/"):
                tweetId = str(identifier)[:-1].split("/")[-1]
            else:
                tweetId = str(identifier).split("/")[-1]
        else:
            tweetId = identifier
        result = {
            "conversation_threads":[]
        }
        r = s.get(self.tweet_detail_url.format(tweetId), headers=self.guest_headers, proxies=self.proxy)
        for entry in r.json()['data']['threaded_conversation_with_injections']['instructions'][0]['entries']:
            if str(entry['entryId']).split("-")[0] == "tweet":
                tweet = entry['content']['itemContent']['tweet_results']['result']['legacy']
                result['tweet'] = tweet
            else:
                result['conversation_threads'].append(entry)
        return result