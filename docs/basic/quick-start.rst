===========
Quick-Start
===========

Let's see a longer example to learn some of the methods that the library
has to offer.

.. code-block:: python

    from tweety import TwitterAsync

    async def main():
        app = TwitterAsync("session")
        await app.sign_in(username, password)
        target_username = "elonmusk"

        user = await app.get_user_info(target_username)
        all_tweets = await app.get_tweets(user)

        for tweet in all_tweets:
            print(tweet)



Here, we show how to get the user information and tweets from ``elonmusk`` user profile on Twitter
and then iterating over the Tweets

- Method ``get_user_info`` returns the instance of `User` class
- Method ``get_tweets`` returns the instance of `UserTweets` class

- Reference to all Classes :ref:`twDataTypes`!

