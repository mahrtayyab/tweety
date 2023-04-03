import functools
from .exceptions_ import *
from .http import Request
from .types.usertweet import UserTweets
from .types.search import Search
from .types.twDataTypes import User, Trends, Tweet


def valid_profile(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        if self.profile_url is None:
            raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")

        if self.user.protected:
            username = self.profile_url.split("/")[-1]
            raise UserProtected(f"User {username} is Protected")

        try:
            return f(self, *args, **kwargs)
        except (UserProtected, UserNotFound) as e:
            raise e
        except Exception as e:
            raise UnknownError(e)

    return wrapper


class Twitter:
    def __init__(self, profile_name: str = None, max_retires: int = 10, proxy: dict = None):
        """
        Initialize the Twitter Class

        :param profile_name: (`str`) Profile URL or The Username of the user you are dealing with
        :param max_retires: (`int`) Number of retries the script would make , if the guest token wasn't found
        :param proxy: (`dict`) Provide the proxy you want to use while making a request
        """
        if profile_name:
            if profile_name.startswith("https://"):
                self.profile_url = profile_name
            else:
                self.profile_url = f"https://twitter.com/{profile_name}"
        else:
            self.profile_url = None

        if proxy and proxy is not None:
            if proxy.get("http") and proxy.get("https"):
                self.proxy = dict(http=proxy['http'], https=proxy['https'])
            else:
                raise ProxyParseError()
        else:
            self.proxy = None

        self.request = Request(self.profile_url, max_retries=max_retires, proxy=self.proxy)
        self.user = self.get_user_info() if self.profile_url is not None else None

    def __verify_user(self):
        """
        Protected method to Verify the User

        :return: User Json
        """
        username = self.profile_url.split("/")[-1]
        return self.request.verify_user(username)

    def get_user_info(self, banner_extensions: bool = False, image_extensions: bool = False):
        """
        Get the user available info

        :param banner_extensions: (`boolean`) Get the Banner extension on the user page
        :param image_extensions: (`boolean`) Get the Image extension on the user page

        :return: .types.twDataTypes.User
        """
        if not self.profile_url:
            raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")

        user_raw = self.__verify_user()

        if not user_raw:
            raise UserNotFound("User {} not Found".format(self.profile_url.split("/")[-1]))

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

        return User(user_raw)

    @property
    def user_id(self):
        """
        Get the user unique twitter id

        :return: int
        """

        return self.user.rest_id

    @valid_profile
    def get_tweets(self, pages: int = 1, replies: bool = False, wait_time: int = 2, cursor: str = None):
        """
        Get the tweets from a user

        :param pages: (`int`) number of pages to be scraped
        :param replies: (`boolean`) get the replied tweets of the user too
        :param wait_time: (`int`) seconds to wait between multiple requests
        :param cursor: Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


        :return: .types.usertweet.UserTweets
        """
        if wait_time is None:
            wait_time = 0

        return UserTweets(self.user_id, self.request, pages, replies, wait_time, cursor)

    def get_trends(self):
        """
        Get the Trends from you locale

        :return:list of .types.twDataTypes.Trends
        """
        trends = []
        response = self.request.get_trends()
        for i in response.json()['timeline']['instructions'][1]['addEntries']['entries'][1]['content']['timelineModule']['items']:
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


        :return: .types.search.Search
        """
        if wait_time is None:
            wait_time = 0

        return Search(keyword, self.request, pages, filter_, wait_time, cursor)

    def tweet_detail(self, identifier: str):
        """
        Get Detail of a single tweet

        :param identifier: (`str`) The unique identifier of the tweet , either the `Tweet id` or `Tweet Link`

        :return: .types.twDataTypes.Tweet
        """

        if str(identifier).startswith("https://"):
            if str(identifier).endswith("/"):
                tweetId = str(identifier)[:-1].split("/")[-1]
            else:
                tweetId = str(identifier).split("/")[-1]
        else:
            tweetId = identifier

        r = self.request.get_tweet_detail(tweetId)

        try:
            for entry in r.json()['data']['threaded_conversation_with_injections_v2']['instructions'][0]['entries']:
                if str(entry['entryId']).split("-")[0] == "tweet":
                    raw_tweet = entry['content']['itemContent']['tweet_results']['result']
                    if raw_tweet['rest_id'] == str(identifier):
                        return Tweet(r, raw_tweet, self.request, True, False, True)

            raise InvalidTweetIdentifier()
        except KeyError:
            raise InvalidTweetIdentifier()
