.. _filter:

===============
Search Filters
===============

You can filter the `Search` function using these methods


Filter Latest Tweets
---------------------

.. py:class:: SearchFilters.Latest()

    :reference: `tweety.filters.SearchFilters.Latest`

    .. code-block:: python

        from tweety.bot import Twitter
        from tweety.filters import SearchFilters

        cookies = cookies_value
        tweets = Twitter(cookies=cookies).search("#pakistan", filter_=SearchFilters.Latest())
        from tweet in tweets:
            print(tweet)

Filter Only Photos Tweets
---------------------------

.. py:class:: SearchFilters.Photos()

    :reference: `tweety.filters.SearchFilters.Photos`

    .. code-block:: python

        from tweety.bot import Twitter
        from tweety.filters import SearchFilters

        cookies = cookies_value
        tweets = Twitter(cookies=cookies).search("#pakistan", filter_=SearchFilters.Photos())
        from tweet in tweets:
            print(tweet.media)


Filter Only Videos Tweets
---------------------------

.. py:class:: SearchFilters.Videos()

    :reference: `tweety.filters.SearchFilters.Videos`

    .. code-block:: python

        from tweety.bot import Twitter
        from tweety.filters import SearchFilters

        cookies = cookies_value
        tweets = Twitter(cookies=cookies).search("#pakistan", filter_=SearchFilters.Videos())
        from tweet in tweets:
            print(tweet.media)


Filter Only Users
---------------------

.. py:class:: SearchFilters.Users()

    :reference: `tweety.filters.SearchFilters.Users`

    .. code-block:: python

        from tweety.bot import Twitter
        from tweety.filters import SearchFilters

        cookies = cookies_value
        users = Twitter(cookies=cookies).search("#pakistan", filter_=SearchFilters.Users())
        from user in users:
            print(user)
