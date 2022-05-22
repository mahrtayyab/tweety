# tweety
Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

[![Downloads](https://static.pepy.tech/personalized-badge/tweety-ns?period=total&units=international_system&left_color=orange&right_color=blue&left_text=Downloads)](https://pepy.tech/project/tweety-ns)
## Prerequisites

Before you begin, ensure you have met the following requirements:

* Internet Connection
* Python 3.6+
* BeautifulSoup (Python Module)
* Requests (Python Module)
* openpyxl (Python Module)
* wget (Python Module) [Optional , you need to install it manually]

## Table of Contents
- [Installation](#installation)
- All Functions
  * [Get Tweets](#getting-tweets)
  * [Get User Info](#getting-user-info)
  * [Get Trends](#getting-trends)
  * [Search Keywords](#searching-a-keyword)
    * [Search Filters](#search-filters)
  * [Get Tweet Detail](#getting-a-tweet-detail)
- [Exceptions](#exceptions)
- [Result Class Objects](#objects-type-classes)
  * [UserTweets](#usertweets)
  * [Tweet](#tweet)
  * [User](#user--userlegacy)
  * [ShortUser](#shortuser)
  * [Trend](#trends)
  * [Search](#search)
  * [Media](#media)
  * [Stream](#stream)
  
## Installation:
```bash
pip install tweety-ns
```

## Exceptions
* ```UserNotFound```       : Raised when the queried user not Found
* ```GuestTokenNotFound``` : Raised when the script is unable to get the guest token from Twitter
* ```InvalidTweetIdentifier``` : Raised when the getting the standalone tweet detail and the tweet identifier is invalid
* ```UnknownError``` : Raised when the error occurs which is unknown to the module

## Using tweety

### Getting Tweets:

#### Description:
_Get 20 Tweets of a Twitter User_
#### Required Parameter:
* ```Username``` or ```User profile URL``` while initiating the Twitter Object
#### Optional Parameter:
* ```pages``` : int (default is 1,starts from 2) -> Get the mentioned number of pages of tweets
* ```replies``` : boolean (default is False) - > should get replies from tweets too
* ```wait_time``` : int (default is 2) - > seconds to wait between multiple requests

#### Output:
[class UserTweets](#usertweets) (iterable)

#### Example:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweety.bot import Twitter
>>> all_tweet = Twitter("Username or URL").get_tweets(pages=2)
```

### Getting Trends:
#### Description:
_Get 20 Locale Trends_
#### Output:
List of [class Trends Object](#trends)

#### Example :
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweety.bot import Twitter
>>> trends = Twitter().get_trends()
>>> for i in trends:
...   print(i.name)
```

### Searching a keyword:
#### Description:
_Get 20 Tweets for a specific Keyword or Hashtag_
#### Required Parameter:
* ```keyword``` : str -> Keyword begin search
#### Optional Parameter:
* ```pages``` : int (starts from 2 , default is 1) -> number of pages to get
* ```filter_``` : str -> filter your search results for different types , check [Search Filters](#search-filters)
* ```wait_time``` : int (default is 2) - > seconds to wait between multiple requests

#### Output:
[class Search](#search) (iterable)
#### Example:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweety.bot import Twitter
>>> trends = Twitter().search("Pakistan")
```
#### Example with filter:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweety.bot import Twitter
>>> from tweety.filters import SearchFilters
>>> trends = Twitter().search("Pakistan",filter_=SearchFilters.Videos())
```

### Getting USER Info:
#### Description:
_Get the information about the user_
#### Required Parameter:
* ```Username``` or ```User profile URL``` while initiating the Twitter Object
#### Optional Parameter:
* ```banner_extensions``` : boolean (Default is False) -> get more information about user banner image
* ```image_extensions``` : boolean (Default is False) -> get more information about user profile image
#### Output:
[class User](#user--userlegacy)

#### Example:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweety.bot import Twitter
>>> trends = Twitter("Username or URL").get_user_info()
```


### Getting a Tweet Detail:
#### Description:
_Get the detail of a tweet including its replies_
#### Required Parameter:
* ```Identifier of the Tweet```: Either Tweet URL OR Tweet ID

#### Output:
class [Tweet](#tweet)

#### Example:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweety.bot import Twitter
>>> trends = Twitter().tweet_detail("https://twitter.com/Microsoft/status/1442542812197801985")
```

## Objects Type Classes
* ### UserTweets
  ```This Object is Iterable and Subscriptable```
    #### Representation:
      UserTweets(user=username, count=number_of_results)
    #### Methods:
    * to_xlsx -> this returns Nothing and create an Excel Sheet
        - '_filename_' parameter can be optionally pass to _to_xlsx_ method in order to set the filename of Excel file , if not passed the default name of Excel file will be _tweet-{username}.xlsx_
    * to_csv -> this returns Nothing and create an CSV Sheet
        - '_filename_' parameter can be optionally pass to _to_csv_ method in order to set the filename of CSV file , if not passed the default name of Excel file will be _tweet-{username}.csv_
    * to_dict -> this is return a tweet dict
    #### Attributes:
    * user -> User ID of the queried user
    * dict -> List of Tweet Results
  
  All the Tweets included in the result are of class [Tweet](#tweet)


* ### Tweet
    #### Representation
      Tweet(id=id_of_tweet , author=author_of_tweet, created_on=tweet_creation_time)
    #### Methods:
    * to_dict -> this is return a tweet dict
    #### Attributes:
    * id -> id of the tweet
    * author -> author of the tweet (class [User](#user--userlegacy))
    * created_on -> creation time of tweet
    * is_retweet -> is the tweet is retweet
    * is_reply -> is the tweet is reply
    * tweet_body -> content of tweet
    * language -> language of the tweet
    * retweet_counts -> number of retweets on the tweet
    * media -> list of media (class [Media](#media)) add to the tweet
    * user_mentions -> list of users (class [ShortUser](#shortuser)) mentioned in the tweet 
    * urls -> list of urls in the tweet
    * hashtags -> list of hashtags in the tweet
    * symbols -> list of symbols in the tweet
    * reply_to -> username of the user to which this tweet was reply to (if is_reply is true)
    * threads -> list of class [Tweet](#tweet) associated with the tweet or None

    This Object is Iterable if the ```threads``` attribute is not None
    

* ### Media
    #### Representation
      Media(id=id_of_media , type=type_of_media)
    #### Methods:
    * to_dict -> this is return a list of dict
    * download -> download the given media in the disk
      > download method requires parameter _filename_
    #### Attributes:
    * id -> id of the media
    * display_url -> url of the media which is used for preview
    * expanded_url -> full url of the media which is used for preview
    * indices -> list of indices of tweet body at which the link was found
    * media_url_https -> full https url of the media
    * type -> type of the media
    * url -> url of the media
    * features -> features of the media
    * sizes -> size of the media
    * original_info -> original dimensions of the media preview 
    * media_key -> internal key of the following media
    * mediaStats -> stats of the media (usually available only when the type of media is video)
    * file_format -> file format of the media if the type of media is photo else None
    * streams -> list of all the video types available [class Stream](#stream) (if the type of media is video)
        

* ### ShortUser
    #### Representation
      ShortUser(id=id_of_user , name=name_of_user)
    #### Methods:
    * to_dict -> this is return a list of dict
    #### Attributes:
    * id -> id of the user
    * name -> name of the user
    * screen_name -> screen name of the user

* ### User & UserLegacy 
   #### Representation
      User(id=id_of_user , name=name_of_user , followers=follower_count_of_user , verified=is_user_verified)
   #### Methods:
    * to_dict -> this is return a list of dict
   #### Attributes:
   * id -> Alpha-Id of the user
   * rest_id -> Numeric id of the user
   * name -> name of the user
   * screen_name -> screen name of the user
   * created_at -> time to user creation
   * default_profile -> is this default_profile of the user
   * default_profile_image -> image of default_profile
   * description -> description of the user
   * entities -> entities of the user
   * fast_followers_count -> number of fast followers
   * favourites_count -> number of favourites of user
   * followers_count -> number of followers of the user
   * friends_count -> number of friends of the user
   * has_custom_timelines -> do user have custom_timelines
   * listed_count -> number of lists of user
   * location -> location of the user
   * media_count -> number of medias posted by the user
   * normal_followers_count -> number of normal_followers
   * protected -> is profile protected
   * statuses_count -> number of statuses posted by the user
   * verified -> is user verified
      
* ### Search 
  ```This Object is Iterable and Subscriptable```
    #### Representation:
        Search(keyword=keyword_begin_searched , count=number_of_tweets_in_result)>
    #### Methods:
    * to_xlsx -> this returns Nothing and create an Excel Sheet
        - '_filename_' parameter can be optionally pass to _to_xlsx_ method in order to set the filename of Excel file , if not passed the default name of Excel file will be _search-{keyword}.xlsx_
    * to_csv -> this returns Nothing and create an CSV Sheet
        - '_filename_' parameter can be optionally pass to _to_csv_ method in order to set the filename of CSV file , if not passed the default name of Excel file will be _search-{keyword}.csv_
      > to_csv and to_xlsx is not available when using filter
    >You can check filters here [Filters](#search-filters)
    * to_dict -> this is return a tweet dict
    #### Attributes:
    * keyword -> Keyword which is being queried
    * dict -> Dictionary of Tweet Results
  
    All the Tweets included in the result are of class [Tweet](#tweet)
    
    If used User Filter , All the Users included in the result are of class [User](#user--userlegacy)

  

* ### Trends
    #### Representation:
        Trends(name=name_of_trend)
    #### Methods:
    * to_dict -> this is return a tweet dict
    #### Attributes:
    * name -> Name of the trend
    * url -> URL of the trend
    * tweet_count -> Number of tweets of the trend

* ### Stream
    #### Representation:
        Stream(content_type=content_type_of_media, length=length_of_media, bitrate=bitrate_of_media, res=resolution_of_media)
    #### Methods:
    * download -> Download the stream in the disk
      > download method requires parameter _filename_
    #### Attributes:
    * bitrate -> Audio bitrate of stream
    * content_type -> Content Type of stream
    * url -> URL of stream
    * length -> Length of the stream in milliseconds
    * aspect_ratio -> Aspect Ratio of the stream
    * res -> Resolution of the stream


### Search Filters
#### Description 
_You can filter your search results using these filters_
#### Filter Types
* Filter Latest Tweet
  > Get the latest tweets for the keyword instead of Twitter Default Popular Tweets
  
  > To use this filter you can pass ```latest``` directly to ```filter_``` parameter of search OR pass ```SearchFilters.Latest()``` method from filters module
* Filter Users
  > Search only Users with corresponding keyword
  
  > To use this filter you can pass ```users``` directly to ```filter_``` parameter of search OR pass ```SearchFilters.Users()``` method from filters module
* Filter Only Photos
  > Search only Tweets has photo in it with corresponding keyword
  
  > To use this filter you can pass ```photos``` directly to ```filter_``` parameter of search OR pass ```SearchFilters.Photos()``` method from filters module
* Filter Only Videos
  > Search only Tweets has video in it with corresponding keyword
  
  > To use this filter you can pass ```videos``` directly to ```filter_``` parameter of search OR pass ```SearchFilters.Videos()``` method from filters module
  
# Updates:
## Update 0.1:
* Get Multiple Pages of tweets using pages parameter in get_tweets() function
* output of [get_tweets](#getting-tweets) has been reworked.

## Update 0.2:
* Again reworked and simplified tweets in [get_tweets](#getting-tweets) function :stuck_out_tongue_winking_eye:
* Added [tweet_detail function](#getting-a-tweet-detail) for getting details about a tweet including replies to it

## Update 0.2.1:
* Fixed Hashtag Search

## Update 0.2.2:
* Fixed get_tweets() with multiple pages
* Added Simplify Parameter in get_tweets() , to get simplified results instead of Twitter's cluttered results

## Update 0.3:
* Added getting multiple pages while searching keyword
* [searching a keyword](#searching-a-keyword) now supports simplify parameter

## Update 0.3.1:
* Fixed the issue when searching more than 2 pages of keyword's tweet gives empty dict
* Fixed the issue when using [get_tweet](#getting-tweets) with a username through an exception if the tweets of the user are less than the mentioned number of pages

## Update 0.3.5:
* Again reworked and simplified tweets in [get_tweets](#getting-tweets)  and [search](#searching-a-keyword) function :stuck_out_tongue_winking_eye:
* [get_tweets](#getting-tweets)  and [search](#searching-a-keyword) now returns TweetDict object , more about TweetDict [here](#TweetDict)
* Tweets can now be imported as Excel Workbook

## Update 0.3.9:
* Tweets can now be imported s CSV too
* The Project is Live at [PYPI Repository](https://pypi.org/project/tweety-ns/)

## Update 0.4:
* Module version on [PYPI Repository](https://pypi.org/project/tweety-ns/) is bumped to 0.1.2
* Fixed the issue of 'No Guest Token Found'

## Update 0.4.1:
* Module version on [PYPI Repository](https://pypi.org/project/tweety-ns/) is bumped to 0.1.3
* Fixed Tweet Formatting Issues

## Update 0.5:
* Module version on [PYPI Repository](https://pypi.org/project/tweety-ns/) is bumped to 0.2
* Now every function by default returns its own type of object class , check here [classes](#objects-type-classes)
* Reworked and more simplified results of [get_tweet](#getting-tweets) and [searches](#search)

## Update 0.5.1:
* Module version on [PYPI Repository](https://pypi.org/project/tweety-ns/) is bumped to 0.2.1
* A simple but important update , fixed the issue of KeyError while looking for tweets

## Update 0.5.2:
* Module version on [PYPI Repository](https://pypi.org/project/tweety-ns/) is bumped to 0.2.11
* Fixed the issue of multiple pages not being scraped for user tweets

## Update 0.5.3:
* Module version on [PYPI Repository](https://pypi.org/project/tweety-ns/) is bumped to 0.2.21
* Results of [get_tweet](#getting-tweets) and [searches](#search) are now iterable even without calling to_dict() method
* tweet_details method returns [Tweet](#tweet) object

## Update 0.6:
* Module version on [PYPI Repository](https://pypi.org/project/tweety-ns/) is bumped to 0.3
* Fixed some minor Bugs
* _to_dict()_ method of resultSet classes ([Search](#searching-a-keyword), [UserTweet](#usertweets)) now return list
* [get_trends](#getting-trends) now return list of [Trend Class](#trends)
* [search](#searching-a-keyword) now supports [filters](#search-filters)
* [Media Class](#media) now supports _download()_ method

## Update 0.7:
* Module version on [PYPI Repository](https://pypi.org/project/tweety-ns/) is bumped to 0.3.5
* ```wait_time``` parameter added to wait between multiple requests on resultSet classes ([Search](#searching-a-keyword), [UserTweet](#usertweets)) 
* Fixed a bug of getting replies where the module was getting the first page replies of Elon Musk only
* Structural Improvements
* ResultSet classes ([Search](#searching-a-keyword), [UserTweet](#usertweets)) are now subscriptable