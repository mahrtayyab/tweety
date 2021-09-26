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
Get 20 Tweets of a Twitter User , More Coming Soon
#### Required Parameter:
* Username or User profile URL while initiating the Twitter Object
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import tweet
>>> tweet = Twitter("Twitter").get_tweets()
>>> for i in tweet['result']:
...   print(i)
```
### Getting Trends:
#### Description:
Get 20 Locale Trends
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import tweet
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

```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import tweet
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
```bash
python
Python 3.7.3 (default, Mar 26 2019, 21:43:19) 
[GCC 8.2.1 20181127] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import tweet
>>> trends = Twitter("Twitter").get_user_info()
```


# Coming Soon
* Getting Multiple Tweet Pages