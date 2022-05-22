import time
import traceback
from .utils import *
from .exceptions_ import *
from .http import Request


class Twitter:
    def __init__(self, profile_name: str = None, max_retires: int = 10):
        if profile_name:
            if profile_name.startswith("https://"):
                self.profile_url = profile_name
            else:
                self.profile_url = f"https://twitter.com/{profile_name}"
        else:
            self.profile_url = None
        self.request = Request(self.profile_url,max_retries=max_retires)

    def __verify_user(self):
        """
        Private method to Verify the User

        :return: User Json
        """
        user = self.profile_url.split("/")[-1]
        data = str(get_graph_ql_query(3, user))
        return self.request.verify_user(data)

    def get_user_info(self, banner_extensions: bool = False, image_extensions:bool = False):
        """
        Get the user available info

        :param banner_extensions: (`boolean`) Get the Banner extension on the user page
        :param image_extensions: (`boolean`) Get the Image extension on the user page

        :return: _types.User
        """
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
        """
        Get the user unique twitter id

        :return: int
        """
        if self.profile_url:
            user = self.__verify_user()
            if user == 0:
                raise UserNotFound()
            else:
                return User(user).rest_id
        else:
            raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")

    def get_tweets(self,pages: int = 1, replies:bool = False, wait_time:int = 2):
        """
        Get the tweets from a user

        :param pages: (`int`) number of pages to be scraped
        :param replies: (`boolean`) get the replied tweets of the user too
        :param wait_time: (`int`) seconds to wait between multiple requests

        :return:_type.UserTweets
        """
        try:
            if self.profile_url:
                user_id = self.get_user_id()
                result = []
                __nextCursor = None
                for page in range(0,int(pages)):
                    if replies:
                        data = str(get_graph_ql_query(2, user_id,__nextCursor))
                        response = self.request.get_tweets(data,replies=True)
                    else:
                        data = str(get_graph_ql_query(1, user_id,__nextCursor))
                        response = self.request.get_tweets(data,replies=False)
                    tweet,__Cursor = format_tweet_json(response)
                    for i in tweet:
                        result.append(i)
                    if __nextCursor != __Cursor:
                        __nextCursor = __Cursor[0]
                        time.sleep(wait_time)
                    else:
                        break
                return UserTweets(result,user_id)
            else:
                raise ValueError("No Username Provided , Please initiate the class using a username or profile URL")
        except:
            error = traceback.format_exc().splitlines()[-1]
            raise UnknownError(str(error))

    def get_trends(self):
        """
        Get the Trends from you locale

        :return:list of _types.Trends
        """
        trends = []
        response = self.request.get_trends()
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
            trends.append(Trends(data))
        return trends

    def search(self, keyword:str, pages:int = 1, filter_:str = None, wait_time:int = 2):
        """
        Search for a keyword or hashtag on Twitter

        :param keyword: (`str`) The keyword which is supposed to be searched
        :param pages: (`int`) The number of pages to get
        :param filter_: (
        `str`| `filters.SearchFilters.Users()`| `filters.SearchFilters.Latest()` | `filters.SearchFilters.Photos()` | `filters.SearchFilters.Videos()`
        )
        :param wait_time : (`int`) seconds to wait between multiple requests

        :return: _types.Search
        """
        result = []
        nextCursor = None
        for page in range(0,int(pages)):
            r = self.request.perform_search(keyword,nextCursor,filter_)
            if filter_ and filter_.lower() == "users":
                results_,__cursor = formatUserSearch(r)
            elif filter_ and filter_.lower() == "photos":
                results_,__cursor = format_search(r,True)
            elif filter_ and filter_.lower() == "videos":
                results_,__cursor = format_search(r,True)
            else:
                results_, __cursor = format_search(r, True)
            for i in results_:
                result.append(i)
            if __cursor != nextCursor:
                nextCursor = __cursor[0]
                time.sleep(wait_time)
            else:
                break
        return Search(result,keyword,filter_)

    def tweet_detail(self,identifier:str):
        """
        Get Detail of a single tweet

        :param identifier: (`str`) The unique identifier of the tweet , either the `Tweet id` or `Tweet Link`

        :return: _types.Tweet
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
            result_ = formatThreadedTweet(r)
            result = Tweet(result_.get("tweet"))
            result.threads = [Tweet(i) for i in result_.get("threads")]

            return result
        except KeyError:
            raise InvalidTweetIdentifier("The Identifier provided of the tweet is either invalid or the tweet is "
                                         "private")
