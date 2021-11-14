# tweety
Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Internet Connection
* Python 3.6+
* BeautifulSoup (Python Module)
* Requests (Python Module)
* openpyxl (Python Module)

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
* simplify : boolean (default is False) -> get simplifies tweets instead of Twitter's cultured results  
#### Output:
* Type -> TweetDict
* Structure
  * #### TweetDict
      - TweetDict is custom Object returned by get_tweet or search method
      - This object can be used to get dict or get an Excel Workbook containing the tweets
      - This Object has two methods:
        - to_xlsx -> this returns Nothing and create an Excel Sheet
          - to use this method _simplify_ parameter must be set to True
          - _filename_ parameter can be optionally pass to _to_xlsx_ method in order to set the filename of Excel file , if not passed the default name of Excel file will be _tweet.xlsx_
        - to_dict -> this is return a tweet dict
      > Not Simplified dict
      ```json
          {
            "tweets": [
              {
                "results": {
                  "tweets": []
                }
              },
              {
                "results": {
                  "tweets": []
                }
              }
            ]
          }
      ```
      > Simplified dict
      ```json
          {
            "tweets": [
              {
                "results": {
                  "tweets": [
                    {
                         "created_on":"Tue Oct 05 17:35:26 +0000 2021",
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
>>> from tweet import Twitter
>>> all_tweet = Twitter("Username or URL").get_tweets(pages=2).to_dict()
```

### Getting Trends:
#### Description:
Get 20 Locale Trends
#### Output:
* Type -> dictionary
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
>>> from tweet import Twitter
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
* simplify : boolean (Default is True) -> Simplify the Results instead of Twitter's cultured results
* pages : int (starts from 2 , default is 1) -> number of pages to get 
#### Output:
* Type -> TweetDict
* Structure -> Please check the structure of [get_tweets](#getting-tweets) function
#### Example:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweet import Twitter
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
* Type -> dict

#### Example:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweet import Twitter
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
>>> from tweet import Twitter
>>> trends = Twitter().tweet_detail("https://twitter.com/Microsoft/status/1442542812197801985")
```

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