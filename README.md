# tweety
Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Internet Connection
* Python 3.6+
* BeautifulSoup (Python Module)
* Requests (Python Module)
* openpyxl (Python Module)

## Installation:
```bash
pip install tweety-ns
```
## All Functions
* get_tweets()
* get_user_info()
* get_trends() (can be used without username)
* search() (can be used without username)
* tweet_detail() (can be used without username)


## Using tweety

### Getting Tweets:
#### Description:
Get 20 Tweets of a Twitter User
#### Required Parameter:
* Username or User profile URL while initiating the Twitter Object
#### Optional Parameter:
* pages : int (default is 1,starts from 2) -> Get the mentioned number of pages of tweets
* include_extras : boolean (default is False) -> Get different extras on the page like Topics etc 
* replies : boolean (default is False) - > should get replies from tweets too
#### Output:
* Type -> [class UserTweets](#usertweets)
    > Simplified dict
    ```json
        {
          "tweets": [
            {
              "results": {
                "tweets": [
                  {
                       "created_on":"Tue Oct 05 17:35:26 +0000 2021",
                       "author": "<class User>",
                       "is_retweet":true,
                       "is_reply": true,
                       "tweet_id":"1445442518301163521",
                       "tweet_body":"Hello, world. #Windows11 https://t.co/pg3d6EsreQ https://t.co/wh6InmfngF",
                       "language":"en",
                       "likes":"",
                       "retweet_counts":442,
                       "source":"Twitter Web App",
                       "media":[],
                       "user_mentions":[],
                       "urls":[],
                       "hashtags":[],
                       "symbols":""
                  }     
                ]
              }
            }
          ]
        }
        
    ```
#### Example:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweety.bot import Twitter
>>> all_tweet = Twitter("Username or URL").get_tweets(pages=2).to_dict()
```

### Getting Trends:
#### Description:
Get 20 Locale Trends
#### Output:
* Type -> [class Trends](#trends)
- Structure
```json
  {
    "trends":[
      {
        "name":"<Trend-name>",
        "url":"<Trend-URL>"
      },
      {
        "name":"<Trend-name>",
        "url":"<Trend-URL>"
      }
    ]
  } 
```
#### Example :
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweety.bot import Twitter
>>> trends = Twitter().get_trends()
>>> for i in trends['trends']:
...   print(i['name'])
```

### Searching a keyword:
#### Description:
Get 20 Tweets for a specific Keyword or Hashtag
#### Required Parameter:
* keyword : str -> Keyword begin search
#### Optional Parameter:
* latest : boolean (Default is False) -> Get the latest tweets
* pages : int (starts from 2 , default is 1) -> number of pages to get 
#### Output:
* Type -> [class Search](#search)
#### Example:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweety.bot import Twitter
>>> trends = Twitter().search("Pakistan").to_xlsx(filename="searches.xlsx")
```

### Getting USER Info:
#### Description:
Get the information about the user
#### Required Parameter:
* Username or User profile URL while initiating the Twitter Object
#### Optional Parameter:
* banner_extensions : boolean (Default is False) -> get more information about user banner image
* image_extensions : boolean (Default is False) -> get more information about user profile image
#### Output:
* Type -> [class User](#user--userlegacy)

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
Get the detail of a tweet including its reply
#### Required Parameter:
* Identifier of the Tweet -> Either Tweet URL  OR Tweet ID

#### Output:
* Type -> dict
* Structure
```json
  {
    "conversation_threads":[],
    "tweet": {}
  }
```
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
    #### Representation:
        <UserTweets (user=username) (count=number_of_results)>
    #### Methods:
    * to_xlsx -> this returns Nothing and create an Excel Sheet
        - '_filename_' parameter can be optionally pass to _to_xlsx_ method in order to set the filename of Excel file , if not passed the default name of Excel file will be _tweet-{username}.xlsx_
    * to_csv -> this returns Nothing and create an CSV Sheet
        - '_filename_' parameter can be optionally pass to _to_csv_ method in order to set the filename of CSV file , if not passed the default name of Excel file will be _tweet-{username}.csv_
    * to_dict -> this is return a tweet dict
    #### Attributes:
    * user -> User ID of the queried user
    * dict -> Dictionary of Tweet Results
    * NOTE: All the Tweets included in the result are of class [Tweet](#tweet)
    
* ### Tweet
    #### Representation
      <Tweet (id=id_of_tweet) (author=author_of_tweet) (created_on=tweet_creation_time)>
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

* ### Media
    #### Representation
      <Media (id=id_of_media) (type=type_of_media)>
    #### Methods:
    * to_dict -> this is return a list of dict
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
    
* ### ShortUser
    #### Representation
      <ShortUser (id=id_of_user) (name=name_of_user)>
    #### Methods:
    * to_dict -> this is return a list of dict
    #### Attributes:
    * id -> id of the user
    * name -> name of the user
    * screen_name -> screen name of the user

* ### User & UserLegacy
   #### Representation
      <User (id=id_of_user) (name=name_of_user) (followers=follower_count_of_user) (verified=is_user_verified)>
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
    #### Representation:
        <Search (keyword=keyword_begin_searched) (count=number_of_tweets_in_result)>
    #### Methods:
    * to_xlsx -> this returns Nothing and create an Excel Sheet
        - '_filename_' parameter can be optionally pass to _to_xlsx_ method in order to set the filename of Excel file , if not passed the default name of Excel file will be _search-{keyword}.xlsx_
    * to_csv -> this returns Nothing and create an CSV Sheet
        - '_filename_' parameter can be optionally pass to _to_csv_ method in order to set the filename of CSV file , if not passed the default name of Excel file will be _search-{keyword}.csv_
    * to_dict -> this is return a tweet dict
    #### Attributes:
    * keyword -> Keyword which is being queried
    * dict -> Dictionary of Tweet Results
    All the Tweets included in the result are of class [Tweet](#tweet)

* ### Trends
    #### Representation:
        <Trends (name=name_of_trend)>
    #### Methods:
    * to_dict -> this is return a tweet dict
    #### Attributes:
    * name -> Name of the trend
    * url -> URL of the trend
    * tweet_count -> Number of tweets of the trend

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