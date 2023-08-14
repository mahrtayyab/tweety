
.. _all-functions:

=============
All Available Functions
=============

This page contains all the public method available to work with

.. attention:: All methods requires user to be authenticated


Get User Info
---------------------

- .. py:method:: Twitter().get_user_info(username: str = None)

    Get the User Info of the specified username or ``self``

    .. py:data:: Arguments

        .. py:data:: username (optional) (Required if not authenticated)
            :type: str
            :value: None

            Username of the user you want to get info of.


    .. py:data:: Return

        :return: `User`


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter("session")
       user = app.get_user_info('elonmusk')


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

       app = Twitter("session")
       tweets = app.get_tweets('elonmusk')
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

       app = Twitter("session")
       for userTweetsObj, tweet in app.iter_tweets('elonmusk'):
           print(tweet)


Searching a Keyword
---------------------

- .. py:method:: Twitter().search(keyword: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)

    Search for a keyword or hashtag on Twitter

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

       app = Twitter("session")
       tweets = app.search('elonmusk')
       for tweet in tweets:
           print(tweet)

- .. py:method:: Twitter().iter_search(keyword: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)

    Search for a keyword or hashtag on Twitter as a generator

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

       app = Twitter("session")
       for search_obj, tweet in app.iter_search('elonmusk'):
           print(tweet)


Get Trends
---------------------

- .. py:method:: Twitter().get_trends()

    Get 20 Local Trends


    .. py:data:: Return

        :return: list[`Trends`]


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter("session")
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

       app = Twitter("session")
       tweet = app.tweet_detail("https://twitter.com/Microsoft/status/1442542812197801985")


Getting Mentioned Tweets
---------------------

- .. py:method:: Twitter().get_mentions(pages: int = 1, wait_time: int = 2, cursor: str = None)

    Getting the Tweets in which the authenticated user is mentioned

    .. attention:: This method requires user to be authenticated

    .. py:data:: Arguments

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: `Mention`


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter("session")
       tweets = app.get_mentions()
       for tweet in tweets:
           print(tweet)


- .. py:method:: Twitter().iter_mentions(pages: int = 1, wait_time: int = 2, cursor: str = None)

    Getting the Tweets in which the authenticated user is mentioned as a generator

    .. py:data:: Arguments

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: Generator: (`Mention`, list[`Tweet`])


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter("session")
       for mention_obj, tweet in app.iter_mentions():
           print(tweet)

Getting Bookmarks
---------------------

- .. py:method:: Twitter().get_bookmarks(pages: int = 1, wait_time: int = 2, cursor: str = None)

    Getting the Bookmarked Tweets of authenticated user

    .. py:data:: Arguments

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: `Bookmarks`


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter("session")
       tweets = app.get_bookmarks()
       for tweet in tweets:
           print(tweet)


- .. py:method:: Twitter().iter_bookmarks(pages: int = 1, wait_time: int = 2, cursor: str = None)

    Getting the Bookmarked Tweets of authenticated user as a generator

    .. py:data:: Arguments

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: Generator: (`Bookmarks`, list[`Tweet`])


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter("session")
       for bookmark_obj, tweet in app.iter_bookmarks():
           print(tweet)

Getting Inbox
---------------------

- .. py:method:: Twitter().get_inbox(user_id: Union[int, str, User] = None, cursor: str = None)

    Getting the inbox of authenticated user

    .. py:data:: Arguments

        .. py:data:: user_id (optional)
            :type: Union[int, str, User]
            :value: None

            User ID of the user whom to get the conversation of (coming soon)

        .. py:data:: cursor (optional)
            :type: str
            :value: None

            Pagination cursor of inbox which will be used to get the new messages


    .. py:data:: Return

        :return: `Inbox`


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter("session")
       inbox = app.get_inbox()
       for conversation in inbox:
           print(conversation)

Sending Message
---------------------

- .. py:method:: Twitter().send_message(username: Union[str, int, User], text: str, file: Union[str, UploadedMedia] = None)

    Sending Message to a User

    .. py:data:: Arguments

        .. py:data:: username
            :type: Union[int, str, User]

            Username of User ID of the user whom to send the message

        .. py:data:: text
            :type: str

            Content of the message to be sent

        .. py:data:: file
            :type: str

            Filepath of the file to be sent


    .. py:data:: Return

        :return: `Message`


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter("session")
       message = app.send_message("user", "Hi")

Creating a Tweet
---------------------

- .. py:method:: Twitter().create_tweet(text: str, files: list[Union[str, UploadedMedia, tuple[str, str]]] = None, filter_: str = None, reply: str = None)

    Create a Tweet using the authenticated user

    .. py:data:: Arguments

        .. py:data:: text
            :type: str

            Content of the message to be sent

        .. py:data:: files
            :type: list[Union[str, UploadedMedia, tuple[str, str]]]

            List of Filepath of the files to be sent

        .. py:data:: filter_
            :type: Union[str, TweetConversationFilters]

           Filter to be applied for Tweet Audience. More about :ref:`filter`

        .. py:data:: reply
            :type: str

            ID of tweet to reply to


    .. py:data:: Return

        :return: `Tweet`


    .. code-block:: python

       from tweety.bot import Twitter

       app = Twitter("session")
       message = app.create_tweet("user", reply="1690430294208483322")


