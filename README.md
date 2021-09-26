# tweety
Twitter's API is annoying to work with, and has lots of limitations — luckily their frontend (JavaScript) has it's own API, which I reverse–engineered. No API rate limits. No restrictions. Extremely fast.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* Internet Connection
* Python 3.6+
* BeautifulSoup (Python Module)
* Requests (Python Module)

## Using tweety

### Getting Tweets:
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

## All Functions
* get_tweets()
* get_user_info()
* get_trends() (can be used without username)

# Coming Soon
* Getting Multiple Tweet Pages
* Searching Tweets for specific Keyword and hashtags