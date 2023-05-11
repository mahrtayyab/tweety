
.. _all-functions:

=============
All Available Functions
=============

This page contains all the public method available to work with

Get User Info
---------------------

- .. py:method:: Twitter().get_user_info(username: str = None, banner_extensions: bool = False, image_extensions: bool = False)

    Get the User Info of the specified username or ``self`` if user is authenticated using ``cookies``

    .. py:data:: Arguments

        .. py:data:: username (optional) (Required if not authenticated)
            :type: str
            :value: None

            Username of the user you want to get info of.

        .. py:data:: banner_extensions (optional)
            :type: bool
            :value: False


        .. py:data:: image_extensions (optional)
            :type: bool
            :value: False



    .. py:data:: Return

        :return: `User`


    .. code-block:: python

       from tweety.bot import Twitter

       user = Twitter().get_user_info('elonmusk')


Get Tweets
---------------------

- .. py:method:: Twitter().get_tweets(username: str , pages: int = 1, replies: bool = False, wait_time: int = 2, cursor: str = None)

    Get the Tweets of the specified username

    .. py:data:: Arguments

        .. py:data:: username (Required)
            :type: str

            Username of the user you want to get Tweets of.

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get


        .. py:data:: replies (optional)
            :type: bool
            :value: False

            Fetch the Replied Tweets of the User

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: `UserTweets`


    .. code-block:: python

       from tweety.bot import Twitter

       tweets = Twitter().get_tweets('elonmusk')
       for tweet in tweets:
           print(tweet)


- .. py:method:: Twitter().iter_tweets(username: str , pages: int = 1, replies: bool = False, wait_time: int = 2, cursor: str = None)

    Get the Tweets of the specified username as a generator

    .. py:data:: Arguments

        .. py:data:: username (Required)
            :type: str

            Username of the user you want to get Tweets of.

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get


        .. py:data:: replies (optional)
            :type: bool
            :value: False

            Fetch the Replied Tweets of the User

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: Generator : (`UserTweets` , list[`Tweet`])


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter()
       for userTweetsObj, tweet in tweets.iter_tweets('elonmusk'):
           print(tweet)


Searching a Keyword
---------------------

.. py:decorator:: AuthRequired

- .. py:method:: Twitter().search(keyword: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)

    Search for a keyword or hashtag on Twitter

    .. attention:: This method requires user to be authenticated

    .. py:data:: Arguments

        .. py:data:: keyword (Required)
            :type: str

            The keyword which is supposed to be searched

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get


        .. py:data:: filter_ (optional)
            :type: str | SearchFilter
            :value: None

            Filter you would like to apply on the search. More about :ref:`filter`

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: `Search`


    .. code-block:: python

       from tweety.bot import Twitter

       cookies = "cookies_value"
       tweets = Twitter(cookies=cookies).search('elonmusk')
       for tweet in tweets:
           print(tweet)

- .. py:method:: Twitter().iter_search(keyword: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)

    Search for a keyword or hashtag on Twitter as a generator

    .. attention:: This method requires user to be authenticated

    .. py:data:: Arguments

        .. py:data:: keyword (Required)
            :type: str

            The keyword which is supposed to be searched

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get


        .. py:data:: filter_ (optional)
            :type: str | SearchFilter
            :value: None

            Filter you would like to apply on the search. More about :ref:`filter`

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: Generator: (`Search`, list[`Tweet`])


    .. code-block:: python

       from tweety.bot import Twitter

       cookies = "cookies_value"
       app = Twitter(cookies=cookies)
       for search_obj, tweet in tweets.iter_search('elonmusk'):
           print(tweet)


Get Trends
---------------------

- .. py:method:: Twitter().get_trends()

    Get 20 Local Trends


    .. py:data:: Return

        :return: list[`Trends`]


    .. code-block:: python

       from tweety.bot import Twitter

       all_trends = app.get_trends()
       for trend in all_trends:
           print(trend)


Get a Tweet Detail
---------------------

- .. py:method:: Twitter().tweet_detail(identifier: str)

    Search for a keyword or hashtag on Twitter

    .. py:data:: Arguments

        .. py:data:: identifier (Required)
            :type: str

            Either ID of the Tweet of URL of the Tweet you want to detail of.

    .. py:data:: Return

        :return: `Tweet`


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter()

       tweet = app.tweet_detail("https://twitter.com/Microsoft/status/1442542812197801985")
