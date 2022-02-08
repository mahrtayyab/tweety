import re
from .utils import *
from .exceptions_ import *
import traceback
import requests as s
import sys


class Twitter:
    def __init__(self, profile_name=None):
        if profile_name:
            if profile_name.startswith("https://"):
                self.profile_url = profile_name
            else:
                self.profile_url = f"https://twitter.com/{profile_name}"
        else:
            self.profile_url = None
        self.__user_by_screen_url = "https://twitter.com/i/api/graphql/B-dCk4ph5BZ0UReWK590tw/UserByScreenName?variables="
        self.__tweets_url = "https://twitter.com/i/api/graphql/Lya9A5YxHQxhCQJ5IPtm7A/UserTweets?variables="
        self.__tweets_with_replies = "https://twitter.com/i/api/graphql/B9izm_qt4l5qWUWrympCVw/UserTweetsAndReplies?variables="
        self.__trends_url = "https://api.twitter.com/2/guide.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&count=20&candidate_source=trends&include_page_configuration=false&entity_tokens=false&ext=mediaStats%2ChighlightedLabel"
        self.__search_url = "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={}&count=20&query_source=typeahead_click&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2CvoiceInfo"
        self.__tweet_detail_url = "https://twitter.com/i/api/graphql/4tzuTRu5-fpJTS7bDF6Nlg/TweetDetail?variables=%7B%22focalTweetId%22%3A%22{}%22%2C%22with_rux_injections%22%3Afalse%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withTweetQuoteCount%22%3Atrue%2C%22withBirdwatchNotes%22%3Afalse%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D"
        self.__guest_token_url = "https://api.twitter.com/1.1/guest/activate.json"
        self.__proxy = {"http": random.choice(proxyFactory())}
        self.__guest_token = self.__get_guest_token()
        self.__guest_headers = get_headers(self.__guest_token)

    def __get_guest_token(self, max_retries=10):
        try:
            guest_token = ""
            for i in range(0, int(max_retries)):
                if self.profile_url:
                    response = s.get(self.profile_url, headers=get_headers(), proxies=self.__proxy)
                else:
                    response = s.get("https://twitter.com/i/trends", headers=get_headers(), proxies=self.__proxy)
                guest_token_ = re.findall('document\.cookie = decodeURIComponent\("gt=(.*?); Max-Age=10800; Domain=\.twitter\.com; Path=/; Secure"\);',response.text)
                try:
                    if guest_token_[0]:
                        guest_token = guest_token_[0]
                        return guest_token
                except IndexError:
                    try:
                        headers = get_headers()
                        headers['x-csrf-token'] = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
                        headers['authorization'] = "Bearer " + "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
                        headers['content-type'] = 'application/x-www-form-urlencoded'
                        headers['accept'] = "*/*"
                        response = s.post(self.__guest_token_url,headers=headers,proxies=self.__proxy)
                        guest_token = response.json()['guest_token']
                        return response.json()['guest_token']
                    except:
                        continue
            if guest_token == "":
                sys.exit(f"Script Aborting : Guest Token couldn't be found after {max_retries} retires.")
        except Exception as e:
            traceback.print_exc()
            sys.exit(f"Script Aborting : Guest Token couldn't be found after {max_retries} retires.\n{e}")

    def __verify_user(self):
        user = self.profile_url.split("/")[-1]
        data = str(get_graph_ql_query(3, user))
        response = s.get(
            f"{self.__user_by_screen_url}{data}",
            headers=self.__guest_headers,
            proxies=self.__proxy
        )
        if response.json().get('data'):
            return response.json()
        else:
            return 0

    def get_user_info(self, banner_extensions=False, image_extensions=False):
        if self.profile_url:
            json_ = self.__verify_user()
            if json_ == 0:
                raise UserNotFound()
            else:
                if not banner_extensions or banner_extensions is False:
                    del json_['data']['user']['result']['legacy']['profile_banner_extensions']
                if not image_extensions or image_extensions is False:
                    del json_['data']['user']['result']['legacy']['profile_image_extensions']
                return User(json_)
        else:
            raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")

    def get_user_id(self):
        if self.profile_url:
            user = self.__verify_user()
            if user == 0:
                raise UserNotFound()
            else:
                return User(user).rest_id
        else:
            raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")

    def get_tweets(self,pages=1,include_extras=False,replies=False):
        try:
            if self.profile_url:
                user_id = self.get_user_id()
                result = {"tweets":[]}
                __nextCursor = None
                for page in range(0,int(pages)):
                    if replies:
                        data = str(get_graph_ql_query(2, user_id,__nextCursor))
                        response = s.get(f"{self.__tweets_with_replies}{data}", headers=self.__guest_headers,
                                         proxies=self.__proxy)
                    else:
                        data = str(get_graph_ql_query(1, user_id,__nextCursor))
                        response = s.get(f"{self.__tweets_url}{data}", headers=self.__guest_headers,
                                         proxies=self.__proxy)
                    tweet,__Cursor = format_tweet_json(response,include_extras=include_extras,simplify=True)
                    for i in tweet['result']['tweets']:
                        result['tweets'].append(i)
                    if __nextCursor != __Cursor:
                        __nextCursor = __Cursor[0]
                    else:
                        break
                return UserTweets(result,user_id)
            else:
                raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")
        except:
            traceback.print_exc()
            exit(1)

    def get_trends(self) -> dict:
        trends = {"trends":[]}
        response = s.get(f"{self.__trends_url}", headers=self.__guest_headers,
                         proxies=self.__proxy)
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
            trends['trends'].append(Trends(data))
        return trends

    def search(self, keyword, pages=1, latest=False):
        result = {"tweets":[]}
        if keyword.startswith("#"):
            keyword = f"%23{keyword[1:]}"
        nextCursor = None
        for page in range(0,int(pages)):
            if nextCursor:
                search_url = f"{self.__search_url}&cursor={nextCursor}"
            else:
                search_url = self.__search_url
            if latest is False:
                r = s.get(search_url.format(keyword), headers=self.__guest_headers, proxies=self.__proxy)
            else:
                url = f"{search_url}&tweet_search_mode=live"
                r = s.get(url.format(keyword), headers=self.__guest_headers, proxies=self.__proxy)
            tweets_, __cursor = format_search(r, True)
            for i in tweets_['result']['tweets']:
                result['tweets'].append(i)
            if __cursor != nextCursor:
                nextCursor = __cursor[0]
            else:
                break
        return Search(result,keyword)

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
        r = s.get(self.__tweet_detail_url.format(tweetId), headers=self.__guest_headers, proxies=self.__proxy)
        for entry in r.json()['data']['threaded_conversation_with_injections']['instructions'][0]['entries']:
            if str(entry['entryId']).split("-")[0] == "tweet":
                tweet = entry['content']['itemContent']['tweet_results']['result']['legacy']
                result['tweet'] = tweet
            else:
                result['conversation_threads'].append(entry)
        return result
