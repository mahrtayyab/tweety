import random
import string
import traceback
from ._types import Tweet, UserTweets, Media,ShortUser,User,Search,Trends,UserLegacy,Card
from bs4 import BeautifulSoup as bs
import requests as s


UserTweets = UserTweets
User = User
Search = Search
Trends = Trends
UserLegacy = UserLegacy
Card = Card


def proxyFactory() -> list:
    # https://proxylist.geonode.com/api/organdasn?limit=200&page=2
    r2 = s.get("https://free-proxy-list.net/")
    soup = bs(r2.content, "html.parser")
    tds = soup.find("tbody").find_all("tr")
    proxies = []
    for io in tds:
        proxies.append(f"{io.find_all('td')[0].text}:{io.find_all('td')[1].text}")
    return proxies


def get_graph_ql_query(typed, user, pages=None) -> str:
    """

    :param typed: internal script query type
    :param user: username or user_id
    :param pages: cursor of next page
    :return: string on graphql query object
    """
    if typed == 1:
        """
        {
            "userId":"",
            "count":20,
            "cursor":""
            "withTweetQuoteCount":true,
            "includePromotedContent":true,
            "withSuperFollowsUserFields":false,
            "withUserResults":true,
            "withBirdwatchPivots":false,
            "withReactionsMetadata":false,
            "withReactionsPerspective":false,
            "withSuperFollowsTweetFields":false,
            "withVoice":true
        }
        """
        if pages:
            data = '''%7B%22userId%22%3A%22''' + user + '''%22%2C%22count%22%3A20%2C%22cursor%22%3A%22''' + pages + '''%22%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D'''
        else:
            data = '''%7B%22userId%22%3A%22''' + user + '''%22%2C%22count%22%3A20%2C%22withTweetQuoteCount%22%3Atrue%2C%22includePromotedContent%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%2C%22withUserResults%22%3Atrue%2C%22withBirdwatchPivots%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Afalse%2C%22withVoice%22%3Atrue%7D'''
    elif typed == 2:
        if pages:
            data = '''%7B%22userId%22%3A%22''' + user + '''%22%2C%22count%22%3A40%2C%22cursor%22%3A%22''' + pages + '''%22%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Afalse%2C%22__fs_interactive_text%22%3Afalse%2C%22__fs_responsive_web_uc_gql_enabled%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Afalse%7D'''
        else:
            data = '''%7B%22userId%22%3A%22''' + user + '''%22%2C%22count%22%3A40%2C%22includePromotedContent%22%3Atrue%2C%22withCommunity%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Atrue%2C%22withDownvotePerspective%22%3Afalse%2C%22withReactionsMetadata%22%3Afalse%2C%22withReactionsPerspective%22%3Afalse%2C%22withSuperFollowsTweetFields%22%3Atrue%2C%22withVoice%22%3Atrue%2C%22withV2Timeline%22%3Afalse%2C%22__fs_interactive_text%22%3Afalse%2C%22__fs_responsive_web_uc_gql_enabled%22%3Afalse%2C%22__fs_dont_mention_me_view_api_enabled%22%3Afalse%7D'''
    else:
        """
        {
             "screen_name":f"{user}",
             "withSafetyModeUserFields":True,
             "withSuperFollowsUserFields":False
         }
        """
        data = '''%7B%22screen_name%22%3A%22''' + user + '''%22%2C%22withSafetyModeUserFields%22%3Atrue%2C%22withSuperFollowsUserFields%22%3Afalse%7D'''
    return data


def get_headers(typed=None) -> dict:
    if not typed:
        headers = {
            "authority": "twitter.com",
            "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            "x-twitter-client-language": "en",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "accept-encoding": "gzip, deflate, br",
            "upgrade-insecure-requests": "1",
            "sec-ch-ua-platform": 'Windows"',
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
        }
    else:
        headers = {
            'x-csrf-token': ''.join(random.choices(string.ascii_letters + string.digits, k=32)),
            'authorization': "Bearer " + "AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            'content-type': "application/json",
            'referer': "https://twitter.com/AmitabhJha3",
            "authority": "twitter.com",
            "sec-ch-ua": '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            "x-twitter-client-language": "en",
            "upgrade-insecure-requests": "1",
            "sec-ch-ua-platform": 'Windows"',
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
            "x-guest-token": typed
        }
    return headers


def format_search(response,simplify):
    tweet = []
    __cursor = []
    users = response.json()['globalObjects']['users']
    for i in response.json()['timeline']['instructions'][0]['addEntries']['entries']:
        try:
            if i['content']['operation']:
                if i['content']['operation']['cursor']['cursorType'] == "Bottom":
                    __cursor.append(i['content']['operation']['cursor']['value'])
        except:
            pass
    for i in response.json()['globalObjects']['tweets']:
        if simplify:
            tweet_ = Tweet(
                simplify_tweet(
                    response.json()['globalObjects']['tweets'][i],
                    response.json()['globalObjects']['tweets'][i]['id'],
                    users.get(str(response.json()['globalObjects']['tweets'][i]['user_id'])),
                    True
                )
            )
            tweet.append(tweet_)
        else:
            tweet.append(response.json()['globalObjects']['tweets'][i])
    try:
        if not __cursor:
            for i in response.json()['timeline']['instructions']:
                for key in i.keys():
                    if key == "replaceEntry":
                        if i['replaceEntry']['entry']['content']['operation']['cursor']['cursorType'] == "Bottom":
                            __cursor.append(i['replaceEntry']['entry']['content']['operation']['cursor']['value'])
                            break
    except:
        pass
    return tweet, __cursor


def simplify_tweet(tweet, rest_id,author,author_legacy=False,card=None):
    try:
        created_on = tweet['created_at'] if tweet['created_at'] else ""
    except KeyError:
        created_on = ""
    rest_id = rest_id
    try:
        is_retweet = True if str(tweet['full_text']).startswith("RT") else False
    except:
        is_retweet = False
    try:
        if is_retweet:
            text = tweet['retweeted_status_result']['result']['legacy']['full_text']
        else:
            text = tweet['full_text'] if tweet['full_text'] else ""
    except KeyError:
        text = ""
    try:
        is_reply = True if tweet.get('in_reply_to_status_id') is not None or tweet.get('in_reply_to_user_id') is not None or tweet.get('in_reply_to_screen_name') is not None else False
    except:
        is_reply = False
    if is_reply:
        reply_to = tweet['in_reply_to_screen_name']
    try:
        language = tweet['lang'] if tweet['lang'] else ""
    except KeyError:
        language = ""
    try:
        likes = tweet['favorite_count'] if tweet['favorite_count'] else ""
    except KeyError:
        likes = ""
    try:
        retweet_count = tweet['retweet_count'] if tweet['retweet_count'] else ""
    except KeyError:
        retweet_count = ""
    try:
        source = str(tweet['source']).split(">")[1].split("<")[0] if tweet['source'] else ""
    except KeyError:
        source = ""
    try:
        media = [Media(i) for i in tweet['extended_entities']['media']] if tweet.get('extended_entities').get('media') else None
    except (KeyError,AttributeError):
        media = ""
    try:
        mentions = [ShortUser(l) for l in tweet['entities']['user_mentions']] if tweet.get('entities').get('user_mentions') else None
    except KeyError:
        mentions = ""
    try:
        urls = tweet['entities']['urls'] if tweet['entities']['urls'] else ""
    except KeyError:
        urls = ""
    try:
        hashtags = tweet['entities']['hashtags'] if tweet['entities']['hashtags'] else ""
    except KeyError:
        hashtags = ""
    try:
        symbols = tweet['entities']['symbols'] if tweet['entities']['symbols'] else ""
    except KeyError:
        symbols = ""
    if card:
        card_ = Card(card)
    else:
        card_ = None
    if not author_legacy:
        author_ = User(author,3)
    else:
        author_ = UserLegacy(author)
    result = {
        "created_on": created_on,
        "author":author_,
        "is_retweet": is_retweet,
        "is_reply":is_reply,
        "tweet_id": rest_id,
        "tweet_body": text,
        "language": language,
        "likes": likes,
        "card":card_,
        "retweet_counts": retweet_count,
        "source": source,
        "media": media,
        "user_mentions": mentions,
        "urls": urls,
        "hashtags": hashtags,
        "symbols": symbols
    }
    if is_reply:
        result['reply_to'] = reply_to
    return result


def format_tweet_json(response):
    tweet = []
    __cursor = []
    if response.json()['data']['user']['result']['timeline']['timeline']['instructions'][0]['type'] == "TimelineAddEntries":
        h = 0
    else:
        h = 1
    for i in response.json()['data']['user']['result']['timeline']['timeline']['instructions'][h]['entries']:
        if str(i['entryId']).split("-")[0] == "tweet":
            try:
                tweet.append(
                    Tweet(
                        simplify_tweet(
                            i['content']['itemContent']['tweet_results']['result']['legacy'],
                            i['content']['itemContent']['tweet_results']['result']['rest_id'],
                            i['content']['itemContent']['tweet_results']['result']['core'],
                            False,
                            i['content']['itemContent']['tweet_results']['result'].get("card")
                        )
                    )
                )
            except:
                pass
        elif str(i['entryId']).split("-")[0] == "cursor":
            if i['content']['cursorType'] == "Bottom":
                __cursor.append(i['content']['value'])
    return tweet, __cursor


def formatThreadedTweet(r):
    result = {
        "tweet":{},
        "threads":[]
    }
    for entry in r.json()['data']['threaded_conversation_with_injections']['instructions'][0]['entries']:
        if str(entry['entryId']).split("-")[0] == "tweet":
            result['tweet'] = simplify_tweet(
                    entry['content']['itemContent']['tweet_results']['result']['legacy'],
                    entry['content']['itemContent']['tweet_results']['result']['rest_id'],
                    entry['content']['itemContent']['tweet_results']['result']['core']
                )
        else:
            if str(entry['entryId']).split("-")[0] == "conversationthread":
                for item in entry['content']['items']:
                    try:
                        tweet = item['item']['itemContent']['tweet_results']['result']
                        result['threads'].append(
                            simplify_tweet(
                                tweet['legacy'],
                                tweet['rest_id'],
                                tweet['core']
                            )
                        )
                    except KeyError as e:
                        pass
    return result


def searchFilters(filter_):
    __search_url = "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&send_error_codes=true&simple_quoted_tweet=true&q={}&count=20&query_source=typeahead_click&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2CvoiceInfo"
    __user_search_url = "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q={}&result_filter=user&count=20&query_source=recent_search_click&pc=1&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CsuperFollowMetadata"
    __photo_search_url = "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q={}&result_filter=image&count=20&query_source=recent_search_click&pc=0&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CsuperFollowMetadata"
    __video_search_url = "https://twitter.com/i/api/2/search/adaptive.json?include_profile_interstitial_type=1&include_blocking=1&include_blocked_by=1&include_followed_by=1&include_want_retweets=1&include_mute_edge=1&include_can_dm=1&include_can_media_tag=1&include_ext_has_nft_avatar=1&skip_status=1&cards_platform=Web-12&include_cards=1&include_ext_alt_text=true&include_quote_count=true&include_reply_count=1&tweet_mode=extended&include_entities=true&include_user_entities=true&include_ext_media_color=true&include_ext_media_availability=true&include_ext_sensitive_media_warning=true&include_ext_trusted_friends_metadata=true&send_error_codes=true&simple_quoted_tweet=true&q={}&result_filter=video&count=20&query_source=recent_search_click&pc=0&spelling_corrections=1&ext=mediaStats%2ChighlightedLabel%2ChasNftAvatar%2CvoiceInfo%2CsuperFollowMetadata"
    if not filter_:
        return __search_url
    elif filter_ and filter_.lower() == "latest":
        return f"{__search_url}&tweet_search_mode=live"
    elif filter_ and filter_.lower() == "users":
        return __user_search_url
    elif filter_ and filter_.lower() == "photos":
        return __photo_search_url
    elif filter_ and filter_.lower() == "videos":
        return __video_search_url
    else:
        return __search_url


def formatUserSearch(response):
    results = []
    __cursor = []
    for i in response.json()['timeline']['instructions'][-1]['addEntries']['entries']:
        if str(i['entryId']).split("-")[0] == "cursor":
            if i['content']['operation']['cursor']['cursorType'] == "Bottom":
                __cursor.append(i['content']['operation']['cursor']['value'])
    for i in response.json()['globalObjects']['users'].values():
        results.append(User(i,2))
    return results,__cursor
