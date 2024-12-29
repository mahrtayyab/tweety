
.. _all-functions:

=============
All Available Functions
=============

This page contains all the public method available to work with

.. attention:: All methods requires user to be authenticated
.. attention:: All methods are async supported
.. attention:: All method's examples assumes `app` is authenticated instance of `TwitterAsync`


Get User Info
---------------------

- .. py:method:: TwitterAsync.get_user_info(username: Union[str, int, list] = None)
    :async:


    Get the User Info of the specified username

    .. py:data:: Arguments

        .. py:data:: username (optional)
            :type: str
            :value: None

            Username, User ID or List of User IDs of the user you want to get info of.


    .. py:data:: Return

        :return: `User` | list[`User`]


    .. code-block:: python

       user = await app.get_user_info('elonmusk')


Get User ID
-------------------
- .. py:method:: TwitterAsync.get_user_id(username: str)
    :async:

    Get User ID of a specific Username

    .. tip::  (in case you only want User ID, you must be using this method)

    .. py:data:: Arguments

        .. py:data:: username
            :type: str

            Username of the user you want to get ID of.


        .. py:data:: Return

            :return: str


        .. code-block:: python

           user = await app.get_user_id('elonmusk')



Get User Tweets
---------------------

- .. py:method:: TwitterAsync.get_tweets(username: Union[str, int, User] , pages: int = 1, replies: bool = False, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_tweets(username: Union[str, int, User] , pages: int = 1, replies: bool = False, wait_time: int = 2, cursor: str = None)
    :async:

    Get the Tweets of the specified username (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: username
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
        :return: Generator : (`UserTweets` , list[`Tweet`])


    .. code-block:: python

       tweets = await app.get_tweets('elonmusk')
       for tweet in tweets:
           print(tweet)


Get User Medias
---------------------

- .. py:method:: TwitterAsync.get_user_media(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_user_media(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get the User Media of the specified username (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: username
            :type: str

            Username of the user you want to get Tweets of.

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

        :return: `UserMedia`
        :return: Generator : (`UserMedia` , list[`Tweet`])


    .. code-block:: python

       tweets = await app.get_user_media('elonmusk')
       for tweet in tweets:
           print(tweet.media)

Get User Highlights
---------------------

- .. py:method:: TwitterAsync.get_user_highlights(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_user_highlights(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get the User Highlights of the specified username (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: username
            :type: str

            Username of the user you want to get Tweets of.

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

        :return: `UserHighlights`
        :return: Generator : (`UserHighlights` , list[`Tweet`])


    .. code-block:: python

       tweets = await app.get_user_highlights('elonmusk')
       for tweet in tweets:
           print(tweet)

Searching a Keyword
---------------------

- .. py:method:: TwitterAsync.search(keyword: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_search(keyword: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)
    :async:

    Search for a keyword or hashtag on Twitter (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: keyword (Required)
            :type: str

            The keyword which is supposed to be searched

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get


        .. py:data:: filter_ (optional)
            :type: str
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
        :return: Generator: (`Search`, list[`Tweet`])


    .. code-block:: python

       tweets = await app.search('elonmusk')
       for tweet in tweets:
           print(tweet)


Get Trends
---------------------

- .. py:method:: TwitterAsync.get_trends()
    :async:

    Get 20 Local Trends


    .. py:data:: Return

        :return: list[`Trends`]


    .. code-block:: python

       from tweety import Twitter

       app = Twitter("session")
       all_trends = await app.get_trends()
       for trend in all_trends:
           print(trend)


Get a Tweet Detail
---------------------

- .. py:method:: TwitterAsync.tweet_detail(identifier: str)
    :async:

    Search for a keyword or hashtag on Twitter

    .. py:data:: Arguments

        .. py:data:: identifier
            :type: str

            Either ID of the Tweet of URL of the Tweet you want to detail of.

    .. py:data:: Return

        :return: `Tweet`


    .. code-block:: python

       tweet = await app.tweet_detail("https://twitter.com/Microsoft/status/1442542812197801985")


Getting Home Timeline
---------------------

- .. py:method:: TwitterAsync.get_home_timeline(timeline_type: str = "HomeTimeline", pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_home_timeline(timeline_type: str = "HomeTimeline", pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:


    Getting the Tweets from Home Page of Authenticated User (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: timeline_type (optional)
            :type: str
            :value: "HomeTimeline"

            The type of Timeline to Get ("HomeTimeline", "HomeLatestTimeline")

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

        :return: `SelfTimeline`
        :return: Generator: (`SelfTimeline`, list[`Tweet`])


    .. code-block:: python

       from tweety.types import HOME_TIMELINE_TYPE_FOR_YOU, HOME_TIMELINE_TYPE_FOLLOWING

       ...

       tweets = await app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOR_YOU)
       for tweet in tweets:
           print(tweet)


Getting Tweet Likes
---------------------

- .. py:method:: TwitterAsync.get_tweet_likes(tweet_id: Union[str, Tweet] ,pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_tweet_likes(tweet_id: Union[str, Tweet] ,pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:


    Getting the Users who have Likes of Tweet (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | Tweet
            :value: 1

            ID of the Tweet

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

        :return: `TweetLikes`
        :return: Generator: (`TweetLikes`, list[`Tweet`])


    .. code-block:: python

       tweet = await app.tweet_detail("1232515235253352")
       likes = await app.get_tweet_likes(tweet)
       for like in likes:
           print(like)


Getting Tweet Retweets
---------------------

- .. py:method:: TwitterAsync.get_tweet_retweets(tweet_id: Union[str, Tweet] ,pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_tweet_retweets(tweet_id: Union[str, Tweet] ,pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Getting the Users who have Retweeted the Tweet (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | Tweet
            :value: 1

            ID of the Tweet

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

        :return: `TweetRetweets`
        :return: Generator: (`TweetRetweets`, list[`User`])


    .. code-block:: python

       tweet = await app.tweet_detail("1232515235253352")
       users = await app.get_tweet_retweets(tweet)
       for user in users:
           print(user)

Getting Tweet Quotes
---------------------

- .. py:method:: TwitterAsync.get_tweet_quotes(tweet_id: Union[str, Tweet] ,pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_tweet_quotes(tweet_id: Union[str, Tweet] ,pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Getting the Users who have Quoted the Tweet (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | Tweet
            :value: 1

            ID of the Tweet

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

        :return: `Search`
        :return: Generator: (`Search`, list[`User`])


    .. code-block:: python

       tweet = await app.tweet_detail("1232515235253352")
       users = await app.get_tweet_quotes(tweet)
       for user in users:
           print(user)


Getting Mentioned Tweets
---------------------

- .. py:method:: TwitterAsync.get_mentions(pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_mentions(pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:


    Getting the Tweets in which the authenticated user is mentioned (`iter` for generator)

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
        :return: Generator: (`Mention`, list[`Tweet`])


    .. code-block:: python

       tweets = await app.get_mentions()
       for tweet in tweets:
           print(tweet)


Getting Bookmarks
---------------------

- .. py:method:: TwitterAsync.get_bookmarks(pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_bookmarks(pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:


    Getting the Bookmarked Tweets of authenticated user (`iter` for generator)

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
        :return: Generator: (`Bookmarks`, list[`Tweet`])


    .. code-block:: python

       tweets = await app.get_bookmarks()
       for tweet in tweets:
           print(tweet)


Getting Inbox
---------------------

- .. py:method:: TwitterAsync.get_inbox(user_id: Union[int, str, User] = None, pages: int = 1, wait_time: int = 2)
    :async:
- .. py:method:: TwitterAsync.iter_inbox(user_id: Union[int, str, User] = None, pages: int = 1, wait_time: int = 2)
    :async:

    Getting the inbox of authenticated user (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: user_id (optional)
            :type: Union[int, str, User]
            :value: None

            User ID of the user whom to get the conversation of (coming soon)

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Inbox Pages you want to get

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests


    .. py:data:: Return

        :return: `Inbox`


    .. code-block:: python

       inbox = await app.get_inbox()
       for conversation in inbox:
           print(conversation)

Get a Conversation
---------------------

- .. py:method:: TwitterAsync.get_conversation(conversation_id: Union[int, str, Conversation, User], max_id=None)
    :async:

    Sending Message to a User

    .. py:data:: Arguments

        .. py:data:: conversation_id
            :type: Union[int, str, Conversation, User]

            ID of the conversation

        .. py:data:: max_id
            :type: str

            Max ID from upto which the messages will be ignored in the conversation


    .. py:data:: Return

        :return: `Conversation`


    .. code-block:: python

       message = await app.get_conversation("kharltayyab")

Sending Message
---------------------

- .. py:method:: TwitterAsync.send_message(username: Union[str, int, User], text: str, file: Union[str, UploadedMedia] = None, in_group:bool = False, reply_to_message_id: Union[int, str, Message] = None, audio_only: bool = False, quote_tweet_id : Union[str, int, Tweet] = None,)
    :async:

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

        .. py:data:: in_group
            :type: bool

            Either Message is begin sent in group or not

        .. py:data:: reply_to_message_id
            :type: Union[int, str, Message]

            Reply to which message id

        .. py:data:: audio_only
            :type: bool

            Send media in message as audio only

        .. py:data:: quote_tweet_id
            :type: Union[int, str, Tweet]

            Quote a specific tweet in your message


    .. py:data:: Return

        :return: `Message`


    .. code-block:: python

       message = await app.send_message("user", "Hi")

Sending Message Reaction
---------------------

- .. py:method:: TwitterAsync.send_message_reaction(reaction_emoji: str, message_id: Union[str, int, Message], conversation_id: Union[str, int, User, Conversation] = None)
    :async:

    Sending Message to a User

    .. py:data:: Arguments

        .. py:data:: reaction_emoji
            :type: str

            Emoji to react with

        .. py:data:: message_id
            :type: Union[str, int, Message]

            ID of the Message to which reaction will be sent

        .. py:data:: conversation_id
            :type: Union[str, int, User, Conversation]

            ID of conversation in which reaction will be sent (Required if `message_id` isn't instance `Message`)

    .. py:data:: Return

        :return: bool


    .. code-block:: python

       await app.send_message_reaction("❤️", "123", "123-345")

Creating a Tweet
---------------------

- .. py:method:: TwitterAsync.create_tweet(text: str, files: list[Union[str, UploadedMedia, tuple[str, str]]] = None, filter_: str = None, reply_to: str = None, quote: str = None, place: Union[str, Place] = None, batch_compose: bool = False, community_id: Union[int, str, Community] = None, post_on_timeline: bool = False)
    :async:

    Create a Tweet using the authenticated user

    .. py:data:: Arguments

        .. py:data:: text
            :type: str

            Content of the message to be sent

        .. py:data:: files(optional)
            :type: list[Union[str, UploadedMedia, tuple[str, str]]]

            List of Filepath of the files to be sent

        .. py:data:: filter_ (optional)
            :type: str |  TweetConversationFilters

           Filter to be applied for Tweet Audience. More about :ref:`filter`

        .. py:data:: reply_to (optional)
            :type: str | Tweet

            ID of tweet to reply to

        .. py:data:: quote
            :type: str | Tweet

            ID of tweet to Quote

        .. py:data:: pool
            :type: dict

            Add a pool in tweet

        .. py:data:: place
            :type: str | Place

            Add a place in tweet

        .. py:data:: batch_compose
            :type: bool

            This tweet is part of a thread

        .. py:data:: community_id
            :type: str | int | Community

            Tweet in a specific community

        .. py:data:: post_on_timeline
            :type: bool

            Post it on your main timeline (only used if posting in a community)

    .. py:data:: Return

        :return: `Tweet`


    .. code-block:: python

       message = await app.create_tweet("user", reply_to="1690430294208483322")

Liking the Tweet
---------------------

- .. py:method:: TwitterAsync.like_tweet(tweet_id: Union[str, int , Tweet])
    :async:

    Post a Like on a Tweet

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Id of the Tweet


    .. py:data:: Return

        :return: bool


    .. code-block:: python

       await app.like_tweet("123456789")

Un-Liking the Tweet
---------------------

- .. py:method:: TwitterAsync.unlike_tweet(tweet_id: Union[str, int , Tweet])
    :async:

    UnLike a Posted a Like on a Tweet

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Id of the Tweet


    .. py:data:: Return

        :return: bool


    .. code-block:: python

       await app.unlike_tweet("123456789")

Retweeting the Tweet
---------------------

- .. py:method:: TwitterAsync.retweet_tweet(tweet_id: Union[str, int , Tweet])
    :async:

    Post a Retweet on a Tweet

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Id of the Tweet


    .. py:data:: Return

        :return: bool


    .. code-block:: python

       await app.retweet_tweet("123456789")

Delete a Retweet
---------------------

- .. py:method:: TwitterAsync.delete_retweet(tweet_id: Union[str, int , Tweet])
    :async:

    Delete a Retweet on a Tweet

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Id of the Tweet


    .. py:data:: Return

        :return: bool


    .. code-block:: python

       await app.delete_retweet("123456789")

Follow a User
---------------------

- .. py:method:: TwitterAsync.follow_user(user_id: Union[str, int , User])
    :async:

    Follow a User

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: `User`


    .. code-block:: python

       await app.follow_user("123456789")

UnFollow a User
---------------------

- .. py:method:: TwitterAsync.unfollow_user(user_id: Union[str, int , User])
    :async:

    Un-Follow a User

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: `User`


    .. code-block:: python

       await app.unfollow_user("123456789")

Block a User
---------------------

- .. py:method:: TwitterAsync.block_user(user_id: Union[str, int , User])
    :async:

    Block a User

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: `User`


    .. code-block:: python

       await app.block_user("123456789")

Un-Block a User
---------------------

- .. py:method:: TwitterAsync.unblock_user(user_id: Union[str, int , User])
    :async:

    Block a User

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: `User`


    .. code-block:: python

       await app.unblock_user("123456789")

Get Community
---------------------

- .. py:method:: TwitterAsync.get_community(community_id: Union[str, int])
    :async:

    Get a Community Details

    .. py:data:: Arguments

        .. py:data:: community_id
            :type: str | int

            Id of the Community

    .. py:data:: Return

        :return: `Community`


    .. code-block:: python

       from tweety import Twitter

       app = Twitter("session")
       await app.get_community("123456789")

Get Community Tweets
---------------------

- .. py:method:: TwitterAsync.get_community_tweets(community_id: Union[str, int, Community] , pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_community_tweets(community_id: Union[str, int, Community], pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)
    :async:

    Get the Tweets of the specified community (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: community_id (Required)
            :type: int | str | Community

            ID of the community you want to get Tweets of.

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get


        .. py:data:: filter_ (optional)
            :type: str
            :value: None

            Filter you would like to apply on the tweets. More about :ref:`filter`

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: `CommunityTweets`
        :return: Generator: (`CommunityTweets`, list[`Tweet`])


    .. code-block:: python

       from tweety import Twitter

       app = Twitter("session")
       tweets = await app.get_community_tweets(12345678)
       for tweet in tweets:
           print(tweet)

Get Community Members
---------------------

- .. py:method:: TwitterAsync.get_community_members(community_id: Union[str, int, Community] , pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_community_members(community_id: Union[str, int, Community], pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)
    :async:

    Get the Members of the specified community (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: community_id (Required)
            :type: int | str | Community

            ID of the community you want to get Tweets of.

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Tweet Pages you want to get


        .. py:data:: filter_ (optional)
            :type: str
            :value: None

            Filter you would like to apply on the tweets. More about :ref:`filter`

        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: `CommunityMembers`
        :return: Generator: (`CommunityMembers`, list[`User`])


    .. code-block:: python

       from tweety import Twitter

       app = Twitter("session")
       users = await app.get_community_members(12345678)
       for user in users:
           print(user)

Delete Tweet
--------------
- .. py:method:: TwitterAsync.delete_tweet(tweet_id: Union[str, int, Tweet])
    :async:

    Delete a Tweet posted by authenticated user

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Id of the Tweet

    .. py:data:: Return

        :return: Bool


    .. code-block:: python

       await app.delete_tweet("123456789")

Enable User Notifications
--------------------------
- .. py:method:: TwitterAsync.enable_user_notification(user_id: Union[str, int, User])
    :async:

     Enable user notification on new tweet from specific user

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: Bool


    .. code-block:: python

       await app.enable_user_notification("123456789")

Disable User Notifications
--------------------------
- .. py:method:: TwitterAsync.disable_user_notification(user_id: Union[str, int, User])
    :async:

     Disable user notification on new tweet from specific user

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: Bool


    .. code-block:: python

       await app.disable_user_notification("123456789")

Get Notified Tweets
---------------------

- .. py:method:: TwitterAsync.get_tweet_notifications(pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_tweet_notifications(pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:


    Get the Tweets of the user whom the authenticated user has enabled the New Tweet Notification , (use `iter` for generator)

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

        :return: `TweetNotifications`
        :return: Generator: (`TweetNotifications`, list[`Tweet`])

    .. code-block:: python

       tweets = await app.get_tweet_notifications()
       for tweet in tweets:
           print(tweet)

Get User Followers
---------------------

- .. py:method:: TwitterAsync.get_user_followers(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_user_followers(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get the Followers of specified User , (use `iter` for generator)

    .. py:data:: Arguments

        .. py:data:: username
            :type: Union[str, int, User]

            Username of the target user

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

        :return: `UserFollowers`
        :return: Generator: (`UserFollowers`, list[`User`])


    .. code-block:: python

       from tweety import Twitter

       app = Twitter("session")
       users = await app.get_user_followers()
       for user in users:
           print(user)

Get User Followings
---------------------

- .. py:method:: TwitterAsync.get_user_followings(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_user_followings(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get the Followings of specified User , (use `iter` for generator)

    .. py:data:: Arguments

        .. py:data:: username
            :type: Union[str, int, User]

            Username of the target user

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

        :return: `UserFollowings`
        :return: Generator: (`UserFollowings`, list[`User`])


    .. code-block:: python

       from tweety import Twitter

       app = Twitter("session")
       users = await app.get_user_followings()
       for user in users:
           print(user)

Get User Subscribers
---------------------

- .. py:method:: TwitterAsync.get_user_subscribers(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_user_subscribers(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get the Subscribers of specified User , (use `iter` for generator)

    .. py:data:: Arguments

        .. py:data:: username
            :type: Union[str, int, User]

            Username of the target user

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of Pages you want to get


        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: `UserSubscribers`
        :return: Generator: (`UserSubscribers`, list[`User`])


    .. code-block:: python

       from tweety import Twitter

       app = Twitter("session")
       users = await app.get_user_subscribers()
       for user in users:
           print(user)

Get Tweet Comments
---------------------

- .. py:method:: TwitterAsync.get_tweet_comments(tweet_id: Union[int, str, Tweet] , pages: int = 1, wait_time: int = 2, cursor: str = None, get_hidden: bool = False)
    :async:
- .. py:method:: TwitterAsync.iter_tweet_comments(tweet_id: Union[int, str, Tweet] , pages: int = 1, wait_time: int = 2, cursor: str = None, get_hidden: bool = False)
    :async:

    Get the Comments of specified Tweet , (use `iter` for generator)

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Target Tweet

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

        .. py:data:: get_hidden (optional)
            :type: bool
            :value: False

            Get hidden comments or not

    .. py:data:: Return

        :return: `TweetComments`
        :return: Generator: (`TweetComments`, list[`ConversationThread`])


    .. code-block:: python

       from tweety import Twitter

       app = Twitter("session")
       threads = await app.get_tweet_comments("123456789")
       for thread in threads:
           print(thread)

Get Lists
---------------------

- .. py:method:: TwitterAsync.get_lists(pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_lists(pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get lists of `Authenticated User`

    .. py:data:: Arguments

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of  Pages you want to get


        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)

    .. py:data:: Return

        :return: `Lists`
        :return: Generator: (`Lists`, list[`TwList`])


    .. code-block:: python

       lists = await app.get_lists()
       for _list in lists:
           print(_list)

Create List
---------------------

- .. py:method:: TwitterAsync.create_list(name: str, description: str = "", is_private: bool = False)
    :async:

    Create a List on Twitter

    .. py:data:: Arguments

        .. py:data:: name
            :type: str

            Name of List

        .. py:data:: description
            :type: str
            :value: ""

            Description of List

        .. py:data:: is_private
            :type: bool

            Either to create the list private or not

    .. py:data:: Return

        :return: `TwList`


    .. code-block:: python

       _list = await app.create_list("list_name")
       print(_list)

Delete List
---------------------

- .. py:method:: TwitterAsync.delete_list(list_id: Union[str, int, TwList])
    :async:

    Delete a List using List ID if authenticated user is Admin

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str | TwList

            ID of Target List

    .. py:data:: Return

        :return: bool


    .. code-block:: python

       _list = await app.delete_list("123515")
       print(_list)

Get List
---------------------

- .. py:method:: TwitterAsync.get_list(list_id: int)
    :async:

    Get a List using List ID

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str

            ID of Target List

    .. py:data:: Return

        :return: `TwList`


    .. code-block:: python

       _list = await app.get_list("123515")
       print(_list)

Get List Tweets
---------------------

- .. py:method:: TwitterAsync.get_list_tweets(list_id: Union[str, int, TwList] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_list_tweets(list_id: Union[str, int, TwList] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get Tweets of specific List (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str | TwList

            ID of Target List

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of  Pages you want to get


        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: `ListTweets`
        :return: Generator: (`ListTweets`, list[`Tweet`])


    .. code-block:: python

       tweets = await app.get_list_tweets("123515")
       for tweet in tweets:
           print(tweet)


Get List Members
---------------------

- .. py:method:: TwitterAsync.get_list_member(list_id: Union[str, int, TwList] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_list_member(list_id: Union[str, int, TwList] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get Tweets of specific List (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str | TwList

            ID of Target List

        .. py:data:: pages (optional)
            :type: int
            :value: 1

            Number of  Pages you want to get


        .. py:data:: wait_time (optional)
            :type: int
            :value: 2

            Number of seconds to wait between multiple requests

        .. py:data:: cursor (optional)
            :type: str
            :value: None

             Pagination cursor if you want to get the pages from that cursor up-to (This cursor is different from actual API cursor)


    .. py:data:: Return

        :return: `ListMembers`
        :return: Generator: (`ListMembers`, list[`User`])


    .. code-block:: python

       users = await app.get_list_member("123515")
       for user in users:
           print(user)

Add List Member
---------------------

- .. py:method:: TwitterAsync.add_list_member(list_id: Union[str, int, TwList], user_id: Union[str, int, User])
    :async:

    Add a specific user from List

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str | TwList

            ID of Target List

        .. py:data:: user_id
            :type: int | str | User

            ID of User to be added

    .. py:data:: Return

        :return: `TwList`


    .. code-block:: python

       _list = await app.add_list_member("123515", "elonmusk")
       print(_list)

Remove List Member
---------------------

- .. py:method:: TwitterAsync.remove_list_member(list_id: Union[str, int, TwList], user_id: Union[str, int, User])
    :async:

    Remove a specific user from List

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str | TwList

            ID of Target List

        .. py:data:: user_id
            :type: int | str | User

            ID of User to be added

    .. py:data:: Return

        :return: `TwList`


    .. code-block:: python

       _list = await app.remove_list_member("123515", "elonmusk")
       print(_list)

Get Topic
---------------------

- .. py:method:: TwitterAsync.get_topic(topic_id: Union[str, int])
    :async:

    Get a topic using ID

    .. py:data:: Arguments

        .. py:data:: topic_id
            :type: int | str

            ID of Topic

    .. py:data:: Return

        :return: `Topic`


    .. code-block:: python

       topic = await app.get_topic("123515")
       print(topic)

Get Topic Tweets
---------------------

- .. py:method:: TwitterAsync.get_topic_tweets(topic_id: Union[str, int, Topic] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_topic_tweets(topic_id: Union[str, int, Topic] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get the Tweets of the specified Topic (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: topic_id
            :type: Union[str, int, Topic]

            ID of the Topic

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

        :return: `TopicTweets`
        :return: Generator : (`TopicTweets` , list[`Tweet`])


    .. code-block:: python

       tweets = await app.get_topic_tweets('123456')
       for tweet in tweets:
           print(tweet)

Get Tweet Analytics
---------------------

- .. py:method:: TwitterAsync.get_tweet_analytics(tweet_id: Union[str, int, Tweet])
    :async:

    Get Analytics of a Tweet (made by authenticated user)

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: int | str | Tweet

            ID of Tweet

    .. py:data:: Return

        :return: `TweetAnalytics`


    .. code-block:: python

       tweet = await app.get_tweet_analytics("123515")
       print(tweet)

Get Mutual Friends/Followers
---------------------

- .. py:method:: TwitterAsync.get_mutual_followers(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_mutual_followers(username: Union[str, int, User] , pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get the Mutual Followers/Friends of a User (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: username
            :type: Union[str, int, User]

            Username of the user you want to get Tweets of.

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

        :return: `MutualFollowers`
        :return: Generator : (`MutualFollowers` , list[`User`])


    .. code-block:: python

       users = await app.get_mutual_followers('elonmusk')
       for user in users:
           print(user)

Get Blocked Users
---------------------

- .. py:method:: TwitterAsync.get_blocked_users(pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:
- .. py:method:: TwitterAsync.iter_blocked_users(pages: int = 1, wait_time: int = 2, cursor: str = None)
    :async:

    Get the users blocked by authenticated user (`iter` for generator)

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

        :return: `BlockedUsers`
        :return: Generator : (`BlockedUsers` , list[`User`])


    .. code-block:: python

       users = await app.get_blocked_users()
       for user in users:
           print(user)

Get Translated Tweet
---------------------

- .. py:method:: TwitterAsync.translate_tweet(tweet_id: Union[str, int, Tweet], language: str)
    :async:

    Get specific Tweet in a specific Language

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: int | str | Tweet

            ID of Tweet

        .. py:data:: language
            :type: str

            Language to which you want to translate


    .. py:data:: Return

        :return: `TweetTranslate`


    .. code-block:: python

       from tweety.filters import Language

       ...

       tweet = await app.translate_tweet("123515", Language.English)
       print(tweet)

Get Tweet History
---------------------

- .. py:method:: TwitterAsync.tweet_edit_history(identifier: Union[str, int, Tweet])
    :async:

    Get the Edit History of a Tweet

    .. py:data:: Arguments

        .. py:data:: identifier
            :type: int | str | Tweet

            ID of Tweet

    .. py:data:: Return

        :return: `TweetHistory`

    .. code-block:: python

       tweet = await app.tweet_edit_history("123515")
       print(tweet)

Search Gifs
---------------------

- .. py:method:: TwitterAsync.search_gifs(search_term: str, pages: int = 1, cursor: str = None, wait_time: int = 2)
    :async:
- .. py:method:: TwitterAsync.iter_search_gifs(search_term: str, pages: int = 1, cursor: str = None, wait_time: int = 2)
    :async:

    Search Gifs Available on Twitter (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: search_term
            :type: str

            Search Term against which gifs to be searched

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

        :return: `GifSearch`
        :return: Generator : (`GifSearch` , list[`Gif`])


    .. code-block:: python

       gifs = await app.search_gifs("Happy")
       for gif in gifs:
           print(gif)

Get Scheduled Tweets
---------------------

- .. py:method:: TwitterAsync.get_scheduled_tweets()
    :async:

    Get the Scheduled Tweets of authenticated User

    .. py:data:: Return

        :return: `ScheduledTweets`

    .. code-block:: python

       tweets = await app.get_scheduled_tweets()
       print(tweets)

Delete Scheduled Tweets
---------------------

- .. py:method:: TwitterAsync.delete_scheduled_tweet(tweet_id: Union[str, int, ScheduledTweet])
    :async:

    Get the Scheduled Tweets of authenticated User

     .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | ScheduledTweet

            ID of scheduled Tweet

    .. py:data:: Return

        :return: bool

    .. code-block:: python

       await app.delete_scheduled_tweet("12345")

Pin a Tweet
---------------------

- .. py:method:: TwitterAsync.pin_tweet(tweet_id: Union[str, int, Tweet])
    :async:

    Pin a Specific Tweet on your Timeline

     .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            ID of Tweet

    .. py:data:: Return

        :return: bool

    .. code-block:: python

       await app.pin_tweet("12345")

Un-Pin a Tweet
---------------------

- .. py:method:: TwitterAsync.unpin_tweet(tweet_id: Union[str, int, Tweet])
    :async:

    Un-Pin a Specific Tweet on your Timeline

     .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            ID of Tweet

    .. py:data:: Return

        :return: bool

    .. code-block:: python

       await app.unpin_tweet("12345")


New Grok Conversation
---------------------

- .. py:method:: TwitterAsync.create_grok_conversation()
    :async:

    Create a New Grok Conversation

    .. py:data:: Return

        :return: str

    .. code-block:: python

       await app.create_grok_conversation()

Get Grok Conversation
---------------------

- .. py:method:: TwitterAsync.get_grok_conversation(conversation_id: Union[str, int])
    :async:

    Get a New Grok Conversation using its ID

    .. py:data:: Arguments

        .. py:data:: conversation_id
            :type: str | int

            ID of Conversation

    .. py:data:: Return

        :return: GrokConversation

    .. code-block:: python

       await app.get_grok_conversation("1232")

Get Grok Response
---------------------

- .. py:method:: TwitterAsync.get_grok_response(text: str, conversation_id: Union[str, int, GrokConversation] =None)
    :async:

    Get Response against your prompt from GROK

    .. py:data:: Arguments

        .. py:data:: text
            :type: str

            Message / text to get response against

        .. py:data:: conversation_id
            :type: Union[str, int, GrokConversation]

            Continuing previous conversation

    .. py:data:: Return

        :return: (GrokMessage, GrokConversation)

    .. code-block:: python

       await app.get_grok_response("Hi , draw a robot")

Get Suggested Users
---------------------

- .. py:method:: TwitterAsync.get_suggested_users()
    :async:

    Get Users suggested to you by Twitter

    .. py:data:: Return

        :return: list[`User`]

    .. code-block:: python

       await app.get_suggested_users()