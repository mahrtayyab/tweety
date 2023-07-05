import functools
import re
from typing import Union

from .types.n_types import Proxy
from .exceptions_ import *
from .http import Request
from .types.usertweet import UserTweets
from .types.search import Search
from .types.mentions import Mention
from .types.inbox import Inbox, SendMessage, Conversation
from .updates import UpdateMethods
from .types.twDataTypes import User, Trends, Tweet
from .utils import create_conversation_id


def AuthRequired(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.user is None:
            raise AuthenticationRequired(200, "GenericForbidden", None)

        return f(self, *args, **kwargs)

    return wrapper


class Twitter(UpdateMethods):
    def __init__(self, max_retires: int = 10, proxy: Union[dict, Proxy] = None, cookies: Union[str, dict] = None):
        """
        Constructor of the Twitter Public class

        :param max_retires: (`int`) Number of retries the script would make , if the guest token wasn't found
        :param proxy: (`dict` or `Proxy`) Provide the proxy you want to use while making a request
        :param cookies: (`str` or `dict`) Cookies which will be used for user authentication
        """

        if not cookies:
            raise AuthenticationRequired(200, "GenericForbidden", None)

        self.request = Request(max_retries=max_retires, proxy=proxy, cookies=cookies)
        self.user = self.get_user_info()
        super().__init__(self.request)
        self.request.set_user(self.user)

    def get_user_info(self, username: str = None, banner_extensions: bool = False, image_extensions: bool = False):
        """
        Get the User Info of the specified username

        :param username: (`str`) username to get information of
        :param banner_extensions: (`boolean`) Get the Banner extension on the user page
        :param image_extensions: (`boolean`) Get the Image extension on the user page

        :return: .types.twDataTypes.User
        """

        user_raw = self.request.get_user(username)

        if not banner_extensions or banner_extensions is False:
            try:
                del user_raw['data']['user']['result']['legacy']['profile_banner_extensions']
            except KeyError:
                pass

        if not image_extensions or image_extensions is False:
            try:
                del user_raw['data']['user']['result']['legacy']['profile_image_extensions']
            except KeyError:
                pass

        return User(user_raw['data']['user']['result'])

    @property
    def user_id(self):
        """
        Get the user unique twitter id

        :return: int
        """
        return self.user.id if self.user else None

    def _get_user_id(self, username):
        if isinstance(username, User):
            user_id = username.rest_id
        elif isinstance(username, int):
            user_id = username
        elif isinstance(username, str) and str(username).isdigit():
            user_id = int(username)
        else:
            user_id = self.get_user_info(username).rest_id

        return user_id

    def get_tweets(self, username: Union[str, int, User], pages: int = 1, replies: bool = False, wait_time: int = 2, cursor: str = None):
        """
         Get the tweets from a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: replies: (`boolean`) get the replied tweets of the user too
        :param: wait_time: (`int`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.usertweet.UserTweets
        """
        if wait_time is None:
            wait_time = 0

        user_id = self._get_user_id(username)

        userTweets = UserTweets(user_id, self.request, pages, replies, wait_time, cursor)

        # TODO : Find proper way to run the generator
        results = [i for i in userTweets.generator()]

        return userTweets

    def iter_tweets(self,  username: Union[str, int, User], pages: int = 1, replies: bool = False, wait_time: int = 2, cursor: str = None):
        """
         Generator for getting the tweets from a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: replies: (`boolean`) get the replied tweets of the user too
        :param: wait_time: (`int`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: (.types.usertweet.UserTweets, list[.types.twDataTypes.Tweet])
        """
        if wait_time is None:
            wait_time = 0

        user_id = self._get_user_id(username)

        userTweets = UserTweets(user_id, self.request, pages, replies, wait_time, cursor)

        return userTweets.generator()

    def get_trends(self):
        """
        Get the Trends from you locale

        :return:list of .types.twDataTypes.Trends
        """
        trends = []
        response = self.request.get_trends()
        for i in response['timeline']['instructions'][1]['addEntries']['entries'][1]['content']['timelineModule']['items']:
            data = {
                "name": i['item']['content']['trend']['name'],
                "url": str(i['item']['content']['trend']['url']['url']).replace("twitter://",
                                                                                "https://twitter.com/").replace("query",
                                                                                                                "q"),
            }
            try:
                if i['item']['content']['trend']['trendMetadata']['metaDescription']:
                    data['tweet_count'] = i['item']['content']['trend']['trendMetadata']['metaDescription']
            except:
                pass
            trends.append(Trends(data))
        return trends

    @AuthRequired
    def search(self, keyword: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None):
        """
        Search for a keyword or hashtag on Twitter

        :param keyword: (`str`) The keyword which is supposed to be searched
        :param pages: (`int`) The number of pages to get
        :param filter_: (
           `str`| `filters.SearchFilters.Users()`| `filters.SearchFilters.Latest()` | `filters.SearchFilters.Photos()` | `filters.SearchFilters.Videos()`
        )
        :param wait_time : (`int`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


        :return: .types.search.Search | if iter: (.types.search.Search, list[.types.twDataTypes.Tweet])
        """
        if wait_time is None:
            wait_time = 0

        search = Search(keyword, self.request, pages, filter_, wait_time, cursor)

        # TODO : Find proper way to run the generator
        results = [i for i in search.generator()]

        return search

    @AuthRequired
    def iter_search(self, keyword: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None):
        """
        Search for a keyword or hashtag on Twitter

        :param keyword: (`str`) The keyword which is supposed to be searched
        :param pages: (`int`) The number of pages to get
        :param filter_: (
           `str`| `filters.SearchFilters.Users()`| `filters.SearchFilters.Latest()` | `filters.SearchFilters.Photos()` | `filters.SearchFilters.Videos()`
        )
        :param wait_time : (`int`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


        :return: (.types.search.Search, list[.types.twDataTypes.Tweet])
        """
        if wait_time is None:
            wait_time = 0

        search = Search(keyword, self.request, pages, filter_, wait_time, cursor)

        return search.generator()

    def get_mentions(self, pages: int = 1, wait_time: int = 2, cursor: str = None):
        """

        :param pages: (`int`) The number of pages to get
        :param wait_time: (`int`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :return:
        """

        if wait_time is None:
            wait_time = 0

        mentions = Mention(self.user.id, self.request, pages, wait_time, cursor)
        results = [i for i in mentions.generator()]

        return mentions

    def get_inbox(self, user_id: Union[int, str, User] = None, cursor: str = None):
        """
        :param user_id : (`str`, `int`, `User`) User id or username of the user whom to get the messages of. Default is ALL
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
                                It is used to get the messages updates
        :return:
        """

        if user_id:
            user_id = self._get_user_id(user_id)

        inbox = Inbox(user_id, self.request, cursor)

        return inbox

    def send_message(self, username: Union[str, int, User], text: str):
        user_id = self._get_user_id(username)
        conversation_id = create_conversation_id(self.user.id, user_id)
        return SendMessage(self.request, conversation_id, text).send()

    def tweet_detail(self, identifier: str):
        """
        Get Detail of a single tweet

        :param identifier: (`str`) The unique identifier of the tweet , either the `Tweet id` or `Tweet Link`

        :return: .types.twDataTypes.Tweet
        """

        tweetId = re.findall("\d+", identifier)[0]

        r = self.request.get_tweet_detail(tweetId)

        try:
            for entry in r['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']:
                if str(entry['entryId']).split("-")[0] == "tweet":
                    raw_tweet = entry['content']['itemContent']['tweet_results']['result']

                    if raw_tweet['rest_id'] == str(tweetId):
                        return Tweet(raw_tweet, self.request, r)

        except KeyError:
            raise InvalidTweetIdentifier(144, "StatusNotFound", r)
