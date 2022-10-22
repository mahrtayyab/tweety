Quickstart
==========

Follow :doc:`installation` to  install Tweety first.


A Quick scraper
---------------------

A minimal Tweety script to get Tweets from `elonmusk` looks something like this:

.. code-block:: python

    from tweety.bot import Twitter

    app = Twitter("elonmusk")

    all_tweets = app.get_tweets()
    for tweet in tweets:
        print(tweet)

So what did that code do?

1.  First we imported the :class:`~tweety.bot.Twitter` class.
2.  Next we create an instance of this class. The first argument is the
    username of the target Twitter User
3.  We then use the :meth:`~tweety.bot.Twitter` method to get the first 20 Tweets of the user
4.  The function returns an instance of :class:`~tweety.types.usertweets.UserTweets` class, more info about :class:`~tweety.types.usertweets.UserTweets`  at :doc:`twDataTypes`

