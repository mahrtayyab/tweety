import warnings
from typing import Union, Type
from .utils import (find_objects, AuthRequired, get_user_from_typehead, get_tweet_id, check_translation_lang,
                    is_tweet_protected, async_list)
from .types import (Proxy, TweetComments, UserTweets, Search, User, Tweet, Trends, Community, CommunityTweets,
                    CommunityMembers, UserFollowers, UserFollowings, TweetHistory, UserMedia, GifSearch,
                    ShortUser, TypeHeadSearch, TweetTranslate, AudioSpace, UserHighlights, UserLikes, Places,
                    UserSubscribers, UserCommunities)
from .exceptions import *
from .session import Session, MemorySession, FileSession
from .http import Request
from .captcha.base import BaseCaptchaSolver


class BotMethods:
    LOGIN_URL = "https://api.x.com/1.1/onboarding/task.json?flow_name=login"

    def __init__(self, session_name: Union[str, Session], proxy: Union[dict, Proxy] = None, captcha_solver: Type[BaseCaptchaSolver] = None, **httpx_kwargs):
        """
        Constructor of the Twitter Public class

        :param: session_name: (`str`, `Session`) This is the name of the session which will be saved and can be loaded later
        :param: proxy: (`dict` or `Proxy`) Provide the proxy you want to use while making a request
        :param: captcha_solver: (`BaseCaptchaSolver`) Provide the instance of captcha solver class
                                which has two mandatory methods named `unlock`, `__call__`.
                                - both mandatory methods should accept at least one argument
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
        self._captcha_solver = None

        if isinstance(session_name, MemorySession):
            self.session = session_name(self)
        elif isinstance(session_name, FileSession):
            self.session = session_name
        else:
            self.session = FileSession(self, session_name)

        if captcha_solver:
            if not hasattr(captcha_solver, "unlock"):
                raise AttributeError("captcha_solver instance '{}' doesn't have 'unlock' method".format(type(captcha_solver)))
            elif "__call__" not in dir(captcha_solver):
                raise AttributeError("captcha_solver instance '{}' doesn't have '__call__' method".format(type(captcha_solver)))

            # Captcha Solver is broken
            # self._captcha_solver = captcha_solver(self, self._proxy)

        self.cookies = None
        self.logged_in = False
        self.is_user_authorized = False
        self.request = self.http = Request(self, max_retries=10, proxy=self._proxy, captcha_solver=captcha_solver, **httpx_kwargs)
        self.user = None
    
    async def get_user_info(self, username: Union[str, int, list] = None):
        """
        Get the User Info of the specified username

        :param: username: (`str` | `int` | List[`str`, `int`]) username or user_id to get information of

        :return: .types.twDataTypes.User
        """

        if not username and self.user is not None:
            username = self.user.username

        if isinstance(username, list):
            for i in username:
                if not str(i).isdigit():
                    raise ValueError("Only Accept List of User IDs.")

        if isinstance(username, list) or str(username).isdigit() or isinstance(username, int):
            usernames = [username] if not isinstance(username, list) else username
            users_raw = await self.request.get_users_by_rest_id(usernames)
            users = find_objects(users_raw, "users", None, recursive=False, none_value=[])

            parsed_users = []
            for user in users:
                try:
                    this_user = User(self, user)
                    parsed_users.append(this_user)
                    self._cached_users[str(this_user.username).lower()] = this_user.id
                except Exception as e:
                    warnings.warn(f"UsersByRestId Error: {str(e)}")

            if len(usernames) == 1 and len(parsed_users) > 0:
                return parsed_users[0]
            elif len(usernames) == 1 and len(parsed_users) == 0:
                return None
            elif len(usernames) > 1 and len(parsed_users) == 0:
                return []
            else:
                return parsed_users
        else:
            user_raw = await self.request.get_user(username)
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
    
    async def get_user_id(self, username: str):
        return await self._get_user_id(username)

    async def _get_user_id(self, username):
        if not username:
            username = self.me

        if isinstance(username, (User, ShortUser)):
            user_id = username.id
        elif isinstance(username, int) or (isinstance(username, str) and str(username).isdigit()):
            user_id = username
        elif self._cached_users.get(username.lower()):
            user_id = self._cached_users[username.lower()]
        else:
            user = None
            try:
                all_users = await self.typehead_user_search(username)
                user = await get_user_from_typehead(username, all_users)
            except TwitterError as e:
                if str(e.__class__.__name__) == "AuthenticationRequired" or "[34]" in str(e):
                    # We can only get user using `typehead_user_search` when authenticated or if user is not suspended
                    pass

            if not user:
                user = await self.get_user_info(username)

            if user:
                user_id = user.id
            else:
                raise UserNotFound()
        return user_id

    async def get_tweets(
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

        user_id = await self._get_user_id(username)
        userTweets = UserTweets(user_id, self, pages, replies, wait_time, cursor)
        return await async_list(userTweets)

    async def iter_tweets(
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

        user_id = await self._get_user_id(username)

        userTweets = UserTweets(user_id, self, pages, replies, wait_time, cursor)

        async for result_tuple in userTweets.generator():
            yield result_tuple

    async def get_user_highlights(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            replies: bool = False,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """
         Get the tweets from a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: replies: (`boolean`) get the replied tweets of the user too
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.usertweet.userHighlights
        """

        user_id = await self._get_user_id(username)

        userHighlights = UserHighlights(user_id, self, pages, replies, wait_time, cursor)

        return await async_list(userHighlights)

    async def iter_user_highlights(
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

        :return: (.types.usertweet.UserHighlights, list[.types.twDataTypes.Tweet])
        """

        user_id = await self._get_user_id(username)

        userHighlights = UserHighlights(user_id, self, pages, replies, wait_time, cursor)

        async for result_tuple in userHighlights.generator():
            yield result_tuple

    async def get_user_likes(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            replies: bool = False,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):
        """
         Get the liked tweets of a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: replies: (`boolean`) get the replied tweets of the user too
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.usertweet.userLikes
        """

        user_id = await self._get_user_id(username)

        userLikes = UserLikes(user_id, self, pages, replies, wait_time, cursor)

        return await async_list(userLikes)

    async def iter_user_likes(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            replies: bool = False,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):

        """
         Generator for getting the liked tweets of a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the tweets of
        :param: pages: (`int`) number of pages to be scraped
        :param: replies: (`boolean`) get the replied tweets of the user too
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: (.types.usertweet.UserLikes, list[.types.twDataTypes.Tweet])
        """

        user_id = await self._get_user_id(username)

        userLikes = UserLikes(user_id, self, pages, replies, wait_time, cursor)

        async for result_tuple in userLikes.generator():
            yield result_tuple

    @AuthRequired
    async def get_user_media(
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

        user_id = await self._get_user_id(username)

        userMedia = UserMedia(user_id, self, pages, wait_time, cursor)

        return await async_list(userMedia)

    @AuthRequired
    async def iter_user_media(
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

        user_id = await self._get_user_id(username)

        userMedia = UserMedia(user_id, self, pages, wait_time, cursor)

        async for result_tuple in userMedia.generator():
            yield result_tuple

    @AuthRequired
    async def get_trends(self):
        """
        Get the Trends from you locale

        :return: list of .types.twDataTypes.Trends
        """
        trends = []
        response = await self.request.get_trends()

        entries = find_objects(response, "addEntries", None)
        if not entries or len(entries) == 0:
            return trends

        for entry in entries['entries']:
            if str(entry['entryId']) == "trends":
                for item in entry['content']['timelineModule']['items']:
                    trends.append(Trends(self, item))

        return trends

    @AuthRequired
    async def search(
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

        search = Search(keyword, self, pages, filter_, wait_time, cursor)

        return await async_list(search)

    @AuthRequired
    async def iter_search(
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

        search = Search(keyword, self, pages, filter_, wait_time, cursor)

        async for result_tuple in search.generator():
            yield result_tuple

    @AuthRequired
    async def typehead_user_search(self, keyword):
        type_head_search = TypeHeadSearch(self, keyword, "users")
        await type_head_search.get_results()
        return type_head_search

    @AuthRequired
    async def get_audio_space(self, space_id: Union[str, Tweet]) -> AudioSpace:
        """

        :param: space_id: ID of the Audio Space , or the Tweet Object that Space Audio is part of.
        :return: .types.twDataTypes.AudioSpace
        """

        if isinstance(space_id, Tweet):
            space_id = space_id.audio_space_id

        space = await self.request.get_audio_space(space_id)

        if not find_objects(space, "metadata", None):
            raise AudioSpaceNotFound(404, "BadRequest", response=space)

        return AudioSpace(self, space)

    @AuthRequired
    async def get_community(self, community_id):
        """

        :param: community_id: ID of the community to get
        :return:
        """

        response = await self.request.get_community(community_id)
        return Community(self, response)

    @AuthRequired
    async def get_user_communities(self, user_id=None):
        """
        Get Communities of a specific user is member of

        :param user_id: User Id of the User whom to get communities of
        :return:.types.community.UserCommunities
        """

        user_id = await self.get_user_id(user_id)

        userCommunities = UserCommunities(self, user_id)
        return await async_list(userCommunities)

    @AuthRequired
    async def iter_community_tweets(
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

        if isinstance(community_id, Community):
            community_id = community_id.id

        communityTweets = CommunityTweets(community_id, self, pages, filter_, wait_time, cursor)

        async for result_tuple in communityTweets.generator():
            yield result_tuple

    @AuthRequired
    async def get_community_tweets(
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

        if isinstance(community_id, Community):
            community_id = community_id.id

        communityTweets = CommunityTweets(community_id, self, pages, filter_, wait_time, cursor)

        return await async_list(communityTweets)

    @AuthRequired
    async def get_community_members(
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

        if isinstance(community_id, Community):
            community_id = community_id.id

        communityTweets = CommunityMembers(community_id, self, pages, filter_, wait_time, cursor)

        return await async_list(communityTweets)

    @AuthRequired
    async def iter_community_members(
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

        if isinstance(community_id, Community):
            community_id = community_id.id

        communityTweets = CommunityMembers(community_id, self, pages, filter_, wait_time, cursor)

        async for result_tuple in communityTweets.generator():
            yield result_tuple

    @AuthRequired
    async def get_user_followers(
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

        user_id = await self._get_user_id(username)

        userFollowers = UserFollowers(user_id, self, pages, wait_time, cursor)

        return await async_list(userFollowers)

    @AuthRequired
    async def iter_user_followers(
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

        user_id = await self._get_user_id(username)

        userFollowers = UserFollowers(user_id, self, pages, wait_time, cursor)

        async for result_tuple in userFollowers.generator():
            yield result_tuple

    @AuthRequired
    async def get_user_followings(
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

        user_id = await self._get_user_id(username)

        userFollowings = UserFollowings(user_id, self, pages, wait_time, cursor)

        return await async_list(userFollowings)

    @AuthRequired
    async def iter_user_followings(
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

        user_id = await self._get_user_id(username)

        userFollowings = UserFollowings(user_id, self, pages, wait_time, cursor)

        async for result_tuple in userFollowings.generator():
            yield result_tuple

    @AuthRequired
    async def get_user_subscribers(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ) -> UserSubscribers:
        """
         Get the Subscribers of a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the followings of
        :param: pages: (`int`) number of pages to be scraped
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: .types.follow.UserSubscribers
        """

        user_id = await self._get_user_id(username)

        userSubscribers = UserSubscribers(user_id, self, pages, wait_time, cursor)

        return await async_list(userSubscribers)

    @AuthRequired
    async def iter_user_subscribers(
            self,
            username: Union[str, int, User],
            pages: int = 1,
            wait_time: Union[int, list, tuple] = 2,
            cursor: str = None
    ):

        """
         Generator for getting the Subscribers from a user

        :param: username: (`str` | `int` | `User`) username of the user whom to get the followings of
        :param: pages: (`int`) number of pages to be scraped
        :param: wait_time: (`int`, `list`, `tuple`) seconds to wait between multiple requests
        :param: cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

        :return: (.types.follow.UserSubscribers, list[.types.twDataTypes.User])
        """

        user_id = await self._get_user_id(username)

        userSubscribers = UserSubscribers(user_id, self, pages, wait_time, cursor)

        async for result_tuple in userSubscribers.generator():
            yield result_tuple

    @AuthRequired
    async def get_tweet_comments(
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

        tweetId = get_tweet_id(tweet_id)

        comments = TweetComments(tweetId, self, get_hidden, pages, wait_time, cursor)
        return await async_list(comments)

    @AuthRequired
    async def iter_tweet_comments(
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

        tweetId = get_tweet_id(tweet_id)

        comments = TweetComments(tweetId, self, get_hidden, pages, wait_time, cursor)

        async for result_tuple in comments.generator():
            yield result_tuple

    @AuthRequired
    async def tweet_edit_history(self, identifier) -> TweetHistory:
        """
        Get Edit History of a Tweet

        :param identifier: (`str`) The unique identifier of the tweet , either the `Tweet id` or `Tweet Link`

        :return: .types.usertweet.TweetHistory
        """

        tweetId = get_tweet_id(identifier)
        tweet_history = TweetHistory(tweetId, self)
        await tweet_history.get_history()
        return tweet_history

    async def tweet_detail(self, identifier: str) -> Tweet:
        """
        Get Detail of a single tweet

        :param: identifier: (`str`) The unique identifier of the tweet , either the `Tweet id` or `Tweet Link`

        :return: .types.twDataTypes.Tweet
        """

        tweetId = get_tweet_id(identifier)

        response = await self.request.get_tweet_detail(tweetId)

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
                    # ignore these protected tweets that are not what we are looking for
                    # otherwise it will throw exception
                    if not (is_tweet_protected(entry) and str(entry['entryId'].split("-")[1]) != str(tweetId)):
                        tweet = Tweet(self, entry, response)

                        if str(tweet.id) == str(tweetId):
                            tweet.threads.extend(_tweet_before)
                            return tweet
                        else:
                            _tweet_before.append(tweet)

        raise InvalidTweetIdentifier(response=response)

    async def translate_tweet(self, tweet_id, language):
        """
            Translate Tweet in another Language

            :param tweet_id: Tweet ID of the Tweet to be translated
            :param language: In which Language you want to translate the Tweet (see tweety.filters.Language)
            :return: .types.twDataTypes.TweetTranslate
        """

        tweetId = get_tweet_id(tweet_id)
        language = check_translation_lang(language)
        response = await self.request.get_tweet_translation(tweetId, language)
        return TweetTranslate(self, response)

    async def search_gifs(self, search_term, pages=1, cursor=None, wait_time=2):
        search = GifSearch(search_term, self, pages, cursor, wait_time)
        return await async_list(search)

    async def iter_search_gifs(self, search_term, pages=1, cursor=None, wait_time=2):
        search = GifSearch(search_term, self, pages, cursor, wait_time)
        async for result_tuple in search.generator():
            yield result_tuple

    async def search_place(self, lat=None, long=None, search_term=None):
        """
        Search Place either using `search_term` , or `latitude` and `longitude`

        :param lat: Latitude of Place
        :param long: Longitude of Place
        :param search_term: Search Term of Place
        :return: .type.places.Places
        """

        places = Places(self, lat, long, search_term)
        await places.get_page()
        return places
