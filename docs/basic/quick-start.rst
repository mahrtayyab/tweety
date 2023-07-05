===========
Quick-Start
===========

Let's see a longer example to learn some of the methods that the library
has to offer.

.. code-block:: python

    from tweety.bot import Twitter

    cookies = "cookies_value"
    app = Twitter(cookies=cookies)
    username = "elonmusk"

    user = app.get_user_info(username)
    all_tweets = app.get_tweets(username)

    for tweet in all_tweets:
        print(tweet)



Here, we show how to get the user information and tweets from ``elonmusk`` user profile on Twitter
and then iterating over the Tweets

- Method ``get_user_info`` returns the instance of `User` class
- Method ``get_tweets`` returns the instance of `UserTweets` class

- Reference to all Classes :ref:`twDataTypes`!

