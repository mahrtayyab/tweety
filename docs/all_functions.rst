All Available Functions
=====================
This page contains all the public method available to work with


Get Tweets
---------------------

Get 20 Tweets of a user

* Required Parameters:
^^^^^^^^^^^^^^^^^^^

    :profile_name: (`str`) Username or User profile URL while initiating the Twitter Object

* Optional Parameters:
^^^^^^^^^^^^^^^^^^^

    :pages: (`int`) number of pages to be scraped

    :replies: (`boolean`) get the replied tweets of the user too

    :wait_time: (`int`) seconds to wait between multiple requests

    :cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

* Return Type:
^^^^^^^^^^^^^^^^^^^

    The function returns an instance of `UserTweets <twDataTypes.html#usertweets>`_ class

* Example:
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tweety.bot import Twitter

    app = Twitter("elonmusk")

    all_tweets = app.get_tweets()

Get Trends
---------------------

Get 20 Locale Trends


* Return Type:
^^^^^^^^^^^^^^^^^^^

    The function returns the list of `Trends <twDataTypes.html#trends-section>`_  class instances


* Example:
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tweety.bot import Twitter

    app = Twitter()

    all_trends = app.get_trends()
    for trend in all_trends:
        print(trend)

Searching a Keyword
---------------------

Get 20 Tweets for a specific Keyword or Hashtag


* Required Parameters:
^^^^^^^^^^^^^^^^^^^

    :keyword: (`str`) Keyword to search


* Optional Parameters:
^^^^^^^^^^^^^^^^^^^

    :pages: (`int`) number of pages to be scraped

    :filter\_: (`str`) filter your search results for different types

    :wait_time: (`int`) seconds to wait between multiple requests

    :cursor: (`str`) Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


* Return Type:
^^^^^^^^^^^^^^^^^^^

    The function returns an instance of `Search <twDataTypes.html#search>`_  class


* Example:
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tweety.bot import Twitter

    app = Twitter()

    all_searches = app.search("Pakistan")


* Example With Filter:
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tweety.bot import Twitter
    from tweety.filters import SearchFilters

    app = Twitter()

    all_searches = app.search("Pakistan",filter_=SearchFilters.Videos())

More about `Filters <filters.html>`_


Getting USER Info
---------------------

Get the information about the user


* Required Parameters:
^^^^^^^^^^^^^^^^^^^

    :profile_name: (`str`) Username or User profile URL while initiating the Twitter Object


* Return Type:
^^^^^^^^^^^^^^^^^^^

    The function returns an instance of `User <twDataTypes.html#user-userlegacy-section>`_  class


* Example:
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tweety.bot import Twitter

    app = Twitter("elonmusk")

    user = app.get_user_info()

Getting a Tweet Detail
---------------------

Get the detail of a Tweet including its threads and comments


* Required Parameters:
^^^^^^^^^^^^^^^^^^^

    :identifier: (`str`) Either Tweet URL OR Tweet ID


* Return Type:
^^^^^^^^^^^^^^^^^^^

    The function returns an instance of `Tweet <twDataTypes.html#tweet-section>`_  class


* Example:
^^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from tweety.bot import Twitter

    app = Twitter()

    user = app.tweet_detail("https://twitter.com/Microsoft/status/1442542812197801985")
