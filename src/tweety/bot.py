import functools
import re
from typing import Union, Generator
from .utils import find_objects
from .types import Proxy, UserTweets, Search, User, Tweet, Trends
from .exceptions_ import *
from .session import Session
from .http import Request
from .types.twDataTypes import AudioSpace


class BotMethods:
    LOGIN_URL = "https://api.twitter.com/1.1/onboarding/task.json?flow_name=login&api_version=1&known_device_token="

    def __init__(self, session_name: Union[str, Session], proxy: Union[dict, Proxy] = None):
        """
        Constructor of the Twitter Public class

        :param session_name: (`str`, `Session`) This is the name of the session which will be saved and can be loaded later
        :param proxy: (`dict` or `Proxy`) Provide the proxy you want to use while making a request
        """

        self._login_url = self.LOGIN_URL
        self._username = None
        self._password = None
        self._extra = None
        self._login_flow = None
        self._login_flow_state = None
        self._last_json = {}

        self._event_builders = []
        self.session = Session(session_name) if isinstance(session_name, str) else session_name
        self.logged_in = False
        self._proxy = proxy.get_dict() if isinstance(proxy, Proxy) else proxy
        self.request = self.http = Request(max_retries=10, proxy=self._proxy)
        self.user = None

    def get_user_info(self, username: str = None) -> User:
        """
        Get the User Info of the specified username

        :param username: (`str`) username to get information of

        :return: .types.twDataTypes.User
        """

        user_raw = self.request.get_user(username)

        return User(user_raw, self)

    @property
    def user_id(self) -> int:
        """
        Get the user unique twitter id

        :return: int
        """
        return self.user.id if self.user else None

    def _get_user_id(self, username) -> int:
        if isinstance(username, User):
            user_id = username.id
        elif isinstance(username, int):
            user_id = username
        elif isinstance(username, str) and str(username).isdigit():
            user_id = int(username)
        else:
            user_id = self.get_user_info(username).id

        return user_id

    def get_tweets(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            replies: bool = False,
            wait_time: int = 2,
            cursor: str = None
    ) -> UserTweets:
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

        userTweets = UserTweets(user_id, self, pages, replies, wait_time, cursor)

        list(userTweets.generator())

        return userTweets

    def iter_tweets(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            replies: bool = False,
            wait_time: int = 2,
            cursor: str = None
    ):

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

        userTweets = UserTweets(user_id, self, pages, replies, wait_time, cursor)

        return userTweets.generator()

    def get_trends(self):
        """
        Get the Trends from you locale

        :return:list of .types.twDataTypes.Trends
        """
        trends = []
        response = self.request.get_trends()

        entries = find_objects(response, "addEntries", None)
        if not entries or len(entries) == 0:
            return trends

        for entry in entries['entries']:
            if str(entry['entryId']) == "trends":
                for item in entry['content']['timelineModule']['items']:
                    trends.append(Trends(item))

        return trends

    def search(
            self,
            keyword: str,
            pages: int = 1,
            filter_: str = None,
            wait_time: int = 2,
            cursor: str = None
    ) -> Search:

        """
        Search for a keyword or hashtag on Twitter

        :param keyword: (`str`) The keyword which is supposed to be searched
        :param pages: (`int`) The number of pages to get
        :param filter_: (
           `str`| `filters.SearchFilters.Users()`| `filters.SearchFilters.Latest()` | `filters.SearchFilters.Photos()` | `filters.SearchFilters.Videos()`
        )
        :param wait_time : (`int`) seconds to wait between multiple requests
        :param cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


        :return: .types.search.Search
        """
        if wait_time is None:
            wait_time = 0

        search = Search(keyword, self, pages, filter_, wait_time, cursor)

        list(search.generator())

        return search

    def iter_search(
            self,
            keyword: str,
            pages: int = 1,
            filter_: str = None,
            wait_time: int = 2,
            cursor: str = None
    ):
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

        search = Search(keyword, self, pages, filter_, wait_time, cursor)

        return search.generator()

    def get_audio_space(self, space_id: Union[str, Tweet]):
        """

        :param space_id: Id of the Audio Space , or the Tweet Object that Space Audio is part of.
        :return: .types.twDataTypes.AudioSpace
        """

        if isinstance(space_id, Tweet):
            space_id = space_id.audio_space_id

        space = self.http.get_audio_space(space_id)

        return AudioSpace(space, self)


    def tweet_detail(self, identifier: str) -> Tweet:
        """
        Get Detail of a single tweet

        :param identifier: (`str`) The unique identifier of the tweet , either the `Tweet id` or `Tweet Link`

        :return: .types.twDataTypes.Tweet
        """

        tweetId = re.findall("\d+", identifier)[-1]

        response = self.request.get_tweet_detail(tweetId)
        _tweet_before = []
        entries  = find_objects(response, "type", "TimelineAddEntries")

        if not entries or len(entries) == 0:
            raise InvalidTweetIdentifier(response=response)


        for entry in entries['entries']:
            if str(entry['entryId']).split("-")[0] == "tweet":
                tweet = Tweet(entry, self, response)

                if str(tweet.id) == str(tweetId):
                    tweet.threads.extend(_tweet_before)
                    return tweet
                else:
                    _tweet_before.append(tweet)

        raise InvalidTweetIdentifier(response=response)

