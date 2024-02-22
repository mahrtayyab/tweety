from typing import Union
from urllib.parse import urlparse
from .utils import find_objects, AuthRequired, get_user_from_typehead
from .types import (Proxy, TweetComments, UserTweets, Search, User, Tweet, Trends, Community, CommunityTweets,
                    CommunityMembers, UserFollowers, UserFollowings, TweetHistory, UserMedia, GifSearch,
                    ShortUser, TypeHeadSearch, TweetTranslate, AudioSpace)
from .exceptions_ import *
from .session import Session
from .http import Request


class BotMethods:
    LOGIN_URL = "https://api.twitter.com/1.1/onboarding/task.json?flow_name=login"

    def __init__(self, session_name: Union[str, Session], proxy: Union[dict, Proxy] = None, **httpx_kwargs):
        """
        Constructor of the Twitter Public class

        :param: session_name: (`str`, `Session`) This is the name of the session which will be saved and can be loaded later
        :param: proxy: (`dict` or `Proxy`) Provide the proxy you want to use while making a request
        """

        self._login_url = self.LOGIN_URL
        self._username = None
        self._password = None
        self._extra = None
        self._login_flow = None
        self._login_flow_state = None
        self._last_json = {}
        self._cached_users = {}
        self._proxy = proxy.get_dict() if isinstance(proxy, Proxy) else proxy

        self._event_builders = []
        self.session = Session(self, session_name) if isinstance(session_name, str) else session_name
        self.logged_in = False
        self.request = self.http = Request(self, max_retries=10, proxy=self._proxy, **httpx_kwargs)
        self.user = None

    def get_user_info(self, username: str = None) -> User:
        """
        Get the User Info of the specified username

        :param: username: (`str`) username to get information of

        :return: .types.twDataTypes.User
        """

        user_raw = self.request.get_user(username)
        user = User(self, user_raw)
        self._cached_users[str(username).lower()] = user.id
        return user

    @property
    def user_id(self) -> int:
        """
        Get the user unique twitter id of authenticated user

        :return: int
        """
        return self.user.id if self.user else None

    @property
    def cache(self):
        return self._cached_users

    def get_user_id(self, username):
        return self._get_user_id(username)

    def _get_user_id(self, username):
        if isinstance(username, (User, ShortUser)):
            user_id = username.id
        elif isinstance(username, int) or (isinstance(username, str) and str(username).isdigit()):
            user_id = username
        elif self._cached_users.get(username.lower()):
            user_id = self._cached_users[username.lower()]
        else:
            user = get_user_from_typehead(username, self.typehead_user_search(username))

            if not user:
                user = self.get_user_info(username)

            if user:
                user_id = user.id
            else:
                raise UserNotFound()
        return user_id

    def get_tweets(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            replies: bool = False,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> UserTweets:
        """
         Get the tweets from a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: replies: (`boolean`) get the replied tweets of the user too
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
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
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):

        """
         Generator for getting the tweets from a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: replies: (`boolean`) get the replied tweets of the user too
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: (.types.usertweet.UserTweets, list[.types.twDataTypes.Tweet])
        """
        if wait_time is None:
            wait_time = 0

        user_id = self._get_user_id(username)

        userTweets = UserTweets(user_id, self, pages, replies, wait_time, cursor)

        return userTweets.generator()

    @AuthRequired
    def get_user_media(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> UserMedia:
        """
         Get the media from a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.usertweet.UserMedia
        """
        if wait_time is None:
            wait_time = 0

        user_id = self._get_user_id(username)

        userMedia = UserMedia(user_id, self, pages, wait_time, cursor)

        list(userMedia.generator())

        return userMedia

    @AuthRequired
    def iter_user_media(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):

        """
         Generator for getting the media from a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: (.types.usertweet.UserMedia, list[.types.twDataTypes.Tweet])
        """
        if wait_time is None:
            wait_time = 0

        user_id = self._get_user_id(username)

        userMedia = UserMedia(user_id, self, pages, wait_time, cursor)

        return userMedia.generator()

    @AuthRequired
    def get_trends(self):
        """
        Get the Trends from you locale

        :return: list of .types.twDataTypes.Trends
        """
        trends = []
        response = self.request.get_trends()

        entries = find_objects(response, "addEntries", None)
        if not entries or len(entries) == 0:
            return trends

        for entry in entries['entries']:
            if str(entry['entryId']) == "trends":
                for item in entry['content']['timelineModule']['items']:
                    trends.append(Trends(self, item))

        return trends

    @AuthRequired
    def search(
            self,
            keyword: str,
            pages: int = 1,
            filter_: str = None,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> Search:

        """
        Search for a keyword or hashtag on Twitter

        :param: keyword: (`str`) The keyword which is supposed to be searched
        :param: pages: (`int`) The number of pages to get
        :param: filter_: (
           `str`| `filters.SearchFilters.Users()`| `filters.SearchFilters.Latest()` | `filters.SearchFilters.Photos()` | `filters.SearchFilters.Videos()`
        )
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


        :return: .types.search.Search
        """
        if wait_time is None:
            wait_time = 0

        search = Search(keyword, self, pages, filter_, wait_time, cursor)

        list(search.generator())

        return search

    @AuthRequired
    def iter_search(
            self,
            keyword: str,
            pages: int = 1,
            filter_: str = None,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """
        Search for a keyword or hashtag on Twitter

        :param: keyword: (`str`) The keyword which is supposed to be searched
        :param: pages: (`int`) The number of pages to get
        :param: filter_: (
           `str`| `filters.SearchFilters.Users()`| `filters.SearchFilters.Latest()` | `filters.SearchFilters.Photos()` | `filters.SearchFilters.Videos()`
        )
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


        :return: (.types.search.Search, list[.types.twDataTypes.Tweet])
        """
        if wait_time is None:
            wait_time = 0

        search = Search(keyword, self, pages, filter_, wait_time, cursor)

        return search.generator()

    @AuthRequired
    def typehead_user_search(self, keyword):
        return TypeHeadSearch(self, keyword, "users")

    @AuthRequired
    def get_audio_space(self, space_id: Union[str, Tweet]) -> AudioSpace:
        """

        :param: space_id: ID of the Audio Space , or the Tweet Object that Space Audio is part of.
        :return: .types.twDataTypes.AudioSpace
        """

        if isinstance(space_id, Tweet):
            space_id = space_id.audio_space_id

        space = self.http.get_audio_space(space_id)

        if not find_objects(space, "metadata", None):
            raise AudioSpaceNotFound(404, "BadRequest", response=space)

        return AudioSpace(self, space)

    @AuthRequired
    def get_community(self, community_id):
        """

        :param: community_id: ID of the community to get
        :return:
        """

        response = self.http.get_community(community_id)
        return Community(self, response)

    @AuthRequired
    def iter_community_tweets(
            self,
            community_id: Union[str, int, Community],
            pages: int = 1,
            filter_: str = None,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):

        """
         Generator for getting the tweets from a community

        :param: community_id: (`str` | `int` | `Community`) ID of the community whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: filter_: (`str`) Filter the Tweets
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: (.types.community.CommunityTweets, list[.types.twDataTypes.Tweet])
        """
        if wait_time is None:
            wait_time = 0

        if isinstance(community_id, Community):
            community_id = community_id.id

        communityTweets = CommunityTweets(community_id, self, pages, filter_, wait_time, cursor)

        return communityTweets.generator()

    @AuthRequired
    def get_community_tweets(
            self,
            community_id: Union[str, int, Community],
            pages: int = 1,
            filter_: str = None,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):

        """
         Getting the tweets from a community

        :param: community_id: (`str` | `int` | `Community`) ID of the community whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: filter_: (`str`) Filter the Tweets
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.community.CommunityTweets
        """
        if wait_time is None:
            wait_time = 0

        if isinstance(community_id, Community):
            community_id = community_id.id

        communityTweets = CommunityTweets(community_id, self, pages, filter_, wait_time, cursor)

        list(communityTweets.generator())

        return communityTweets

    @AuthRequired
    def get_community_members(
            self,
            community_id: Union[str, int, Community],
            pages: int = 1,
            filter_: str = None,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """
         Getting the Members from a community

        :param: community_id: (`str` | `int` | `Community`) ID of the community whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: filter_: (`str`) Filter the Members
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.community.CommunityMembers
        """

        if wait_time is None:
            wait_time = 0

        if isinstance(community_id, Community):
            community_id = community_id.id

        communityTweets = CommunityMembers(community_id, self, pages, filter_, wait_time, cursor)

        list(communityTweets.generator())

        return communityTweets

    @AuthRequired
    def iter_community_members(
            self,
            community_id: Union[str, int, Community],
            pages: int = 1,
            filter_: str = None,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """
         Getting the Members from a community

        :param: community_id: (`str` | `int` | `Community`) ID of the community whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: filter_: (`str`) Filter the Members
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: (.types.community.CommunityMembers, [.types.twDataTypes.User])
        """

        if wait_time is None:
            wait_time = 0

        if isinstance(community_id, Community):
            community_id = community_id.id

        communityTweets = CommunityMembers(community_id, self, pages, filter_, wait_time, cursor)

        return communityTweets.generator()

    @AuthRequired
    def get_user_followers(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> UserFollowers:
        """
         Get the followers of a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the followers of
        :param: pages: (`int`) number of pages to be scraped
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.follow.UserFollowers
        """
        if wait_time is None:
            wait_time = 0

        if not username:
            username = self.me.username

        user_id = self._get_user_id(username)

        userFollowers = UserFollowers(user_id, self, pages, wait_time, cursor)

        list(userFollowers.generator())

        return userFollowers

    @AuthRequired
    def iter_user_followers(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):

        """
         Generator for getting the followers from a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the followers of
        :param: pages: (`int`) number of pages to be scraped
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: (.types.follow.UserFollowers, list[.types.twDataTypes.User])
        """
        if wait_time is None:
            wait_time = 0

        if not username:
            username = self.me.username

        user_id = self._get_user_id(username)

        userFollowers = UserFollowers(user_id, self, pages, wait_time, cursor)

        return userFollowers.generator()

    @AuthRequired
    def get_user_followings(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> UserFollowings:
        """
         Get the Followings of a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the followings of
        :param: pages: (`int`) number of pages to be scraped
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.follow.UserFollowings
        """
        if wait_time is None:
            wait_time = 0

        if not username:
            username = self.me.username

        user_id = self._get_user_id(username)

        userFollowings = UserFollowings(user_id, self, pages, wait_time, cursor)

        list(userFollowings.generator())

        return userFollowings

    @AuthRequired
    def iter_user_followings(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):

        """
         Generator for getting the followings from a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the followings of
        :param: pages: (`int`) number of pages to be scraped
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: (.types.follow.UserFollowings, list[.types.twDataTypes.User])
        """
        if wait_time is None:
            wait_time = 0

        if not username:
            username = self.me.username

        user_id = self._get_user_id(username)

        userFollowings = UserFollowings(user_id, self, pages, wait_time, cursor)

        return userFollowings.generator()

    @AuthRequired
    def get_tweet_comments(
            self,
            tweet_id: Union[str, Tweet],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None,
            get_hidden: bool = False
    ):
        """

        :param: tweet_id: Tweet ID or the Tweet Object of which the Comments to get
        :param: pages: (`int`) The number of pages to get
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :param: get_hidden: (`bool`) get the hidden comments (most likely offensive comments)
        :return: .types.likes.TweetLikes
        """

        comments = TweetComments(tweet_id, self, get_hidden, pages, wait_time, cursor)
        list(comments.generator())
        return comments

    @AuthRequired
    def iter_tweet_comments(
            self,
            tweet_id: Union[str, Tweet],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None,
            get_hidden: bool = False
    ):
        """

        :param: tweet_id: Tweet ID or the Tweet Object of which the Likes to get
        :param: pages: (`int`) The number of pages to get
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)
        :param: get_hidden: (`bool`) get the hidden comments (most likely offensive comments)

        :return: (.types.likes.TweetLikes, list[.types.twDataTypes.User])
        """

        if isinstance(tweet_id, Tweet):
            tweet_id = tweet_id.id

        comments = TweetComments(tweet_id, self, get_hidden, pages, wait_time, cursor)

        return comments.generator()

    @AuthRequired
    def tweet_edit_history(self, identifier) -> TweetHistory:
        """
        Get Edit History of a Tweet

        :param identifier: (`str`) The unique identifier of the tweet , either the `Tweet id` or `Tweet Link`

        :return: .types.usertweet.TweetHistory
        """

        tweetId = urlparse(str(identifier)).path.split("/")[-1]
        return TweetHistory(tweetId, self)

    def tweet_detail(self, identifier: str) -> Tweet:
        """
        Get Detail of a single tweet

        :param: identifier: (`str`) The unique identifier of the tweet , either the `Tweet id` or `Tweet Link`

        :return: .types.twDataTypes.Tweet
        """

        tweetId = urlparse(str(identifier)).path.split("/")[-1]

        response = self.request.get_tweet_detail(tweetId)

        if self.user is None:
            if find_objects(response, "tweetResult", None):
                return Tweet(self, response, response)
        else:
            _tweet_before = []
            entries = find_objects(response, "type", "TimelineAddEntries")

            if not entries or len(entries) == 0:
                raise InvalidTweetIdentifier(response=response)

            for entry in entries['entries']:
                if str(entry['entryId']).split("-")[0] == "tweet":
                    tweet = Tweet(self, entry, response)

                    if str(tweet.id) == str(tweetId):
                        tweet.threads.extend(_tweet_before)
                        return tweet
                    else:
                        _tweet_before.append(tweet)

        raise InvalidTweetIdentifier(response=response)

    def translate_tweet(self, tweet_id, language):
        response = self.http.get_tweet_translation(tweet_id, language)
        return TweetTranslate(self, response)

    def search_gifs(self, search_term, pages=1, cursor=None, wait_time=2):
        search = GifSearch(search_term, self, pages, cursor, wait_time)
        list(search.generator())
        return search

    def iter_search_gifs(self, search_term, pages=1, cursor=None, wait_time=2):
        search = GifSearch(search_term, self, pages, cursor, wait_time)
        return search.generator()
