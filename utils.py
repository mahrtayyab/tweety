import random
import string

from bs4 import BeautifulSoup as bs
import requests as s


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


def format_tweet_json(response,include_extras):
    tweet = {
        "result": {
            "tweets": []
        }
    }
    __cursor = []
    for i in response.json()['data']['user']['result']['timeline']['timeline']['instructions'][0]['entries']:
        if str(i['entryId']).split("-")[0] == "tweet":
            tweet['result']['tweets'].append(i['content']['itemContent']['tweet_results']['result']['legacy'])
        elif str(i['entryId']).split("-")[0] == "cursor":
            if i['content']['cursorType'] == "Bottom":
                __cursor.append(i['content']['value'])
            # __cursor.append(i)
        else:
            if include_extras is True:
                if str(i['entryId']).split("-")[0] in tweet['result']:
                    pass
                else:
                    tweet['result'][f"{str(i['entryId']).split('-')[0]}"] = []
                tweet['result'][f"{str(i['entryId']).split('-')[0]}"].append(i)
            else:
                pass
    return tweet, __cursor
