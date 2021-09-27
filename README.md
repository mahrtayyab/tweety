# tweety
Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Internet Connection
* Python 3.6+
* BeautifulSoup (Python Module)
* Requests (Python Module)

## All Functions
* get_tweets()
* get_user_info()
* get_trends() (can be used without username)
* search() (can be used without username)


## Using tweety

### Getting Tweets:
#### Description:
Get 20 Tweets of a Twitter User
#### Required Parameter:
* Username or User profile URL while initiating the Twitter Object
#### Optional Parameter:
* pages : int (starts from 2) -> Get the mentioned number of pages of tweets
#### Output:
* Type -> dictionary
- Structure
```bash
    {
      "p-1" : {
        "result": {
            "tweets": []
        }
      },
      "p-2":{
        "result": {
            "tweets": []
        }
      }
    }
```
#### Example:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweet import Twitter
>>> all_tweet = Twitter("Username or URL").get_tweets(pages=2)
>>> for i in all_tweet:
...   print(all_tweet[i])
```
### Getting Trends:
#### Description:
Get 20 Locale Trends
#### Output:
* Type -> dictionary
- Structure
```bash
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
* latest : boolean -> Get the latest tweets
#### Output:
* Type -> list

#### Example:
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from tweet import Twitter
>>> trends = Twitter().search("Pakistan")
```

### Getting USER Info:
#### Description:
Get the information about the user
#### Required Parameter:
* Username or User profile URL while initiating the Twitter Object
#### Optional Parameter:
* banner_extensions : boolean -> get more information about user banner image
* image_extensions : boolean -> get more information about user profile image
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


# Update 0.1:
* Get Multiple Pages of tweets using pages parameter in get_tweets() function
* output of get_tweets() has been reworked.