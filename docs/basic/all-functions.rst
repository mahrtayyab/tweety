
.. _all-functions:

=============
All Available Functions
=============

This page contains all the public method available to work with

.. attention:: All methods requires user to be authenticated
.. attention:: All method's examples assumes `app` is authenticated instance of `Twitter`


Get User Info
---------------------

- .. py:method:: Twitter().get_user_info(username: Union[str, int, list] = None)

    Get the User Info of the specified username

    .. py:data:: Arguments

        .. py:data:: username (optional)
            :type: str
            :value: None

            Username, User ID or List of User IDs of the user you want to get info of.


    .. py:data:: Return

        :return: `User` | list[`User`]


    .. code-block:: python

       user = app.get_user_info('elonmusk')


Get User ID
-------------------
- .. py:method:: Twitter().get_user_id(username: str)

    Get User ID of a specific Username

    .. tip::  (in case you only want User ID, you must be using this method)

    .. py:data:: Arguments

        .. py:data:: username
            :type: str

            Username of the user you want to get ID of.


        .. py:data:: Return

            :return: str


        .. code-block:: python

           user = app.get_user_id('elonmusk')



Get User Tweets
---------------------

- .. py:method:: Twitter().get_tweets(username: str , pages: int = 1, replies: bool = False, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_tweets(username: str , pages: int = 1, replies: bool = False, wait_time: int = 2, cursor: str = None)

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

       tweets = app.get_tweets('elonmusk')
       for tweet in tweets:
           print(tweet)


Get User Medias
---------------------

- .. py:method:: Twitter().get_user_media(username: str , pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_user_media(username: str , pages: int = 1, wait_time: int = 2, cursor: str = None)

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

       tweets = app.get_user_media('elonmusk')
       for tweet in tweets:
           print(tweet.media)



Searching a Keyword
---------------------

- .. py:method:: Twitter().search(keyword: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_search(keyword: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)

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

       tweets = app.search('elonmusk')
       for tweet in tweets:
           print(tweet)


Get Trends
---------------------

- .. py:method:: Twitter().get_trends()

    Get 20 Local Trends


    .. py:data:: Return

        :return: list[`Trends`]


    .. code-block:: python

       from tweety import Twitter

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

       tweet = app.tweet_detail("https://twitter.com/Microsoft/status/1442542812197801985")


Getting Home Timeline
---------------------

- .. py:method:: Twitter().get_home_timeline(timeline_type: str = "HomeTimeline", pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_home_timeline(timeline_type: str = "HomeTimeline", pages: int = 1, wait_time: int = 2, cursor: str = None)


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

       tweets = app.get_home_timeline(timeline_type=HOME_TIMELINE_TYPE_FOR_YOU)
       for tweet in tweets:
           print(tweet)


Getting Tweet Likes
---------------------

- .. py:method:: Twitter().get_tweet_likes(tweet_id: Union[str, Tweet] ,pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_tweet_likes(tweet_id: Union[str, Tweet] ,pages: int = 1, wait_time: int = 2, cursor: str = None)


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

       tweet = app.tweet_detail("1232515235253352")
       likes = app.get_tweet_likes(tweet)
       for like in likes:
           print(like)


Getting Tweet Retweets
---------------------

- .. py:method:: Twitter().get_tweet_retweets(tweet_id: Union[str, Tweet] ,pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_tweet_retweets(tweet_id: Union[str, Tweet] ,pages: int = 1, wait_time: int = 2, cursor: str = None)

    Getting the Users who have Retweeted of Tweet (`iter` for generator)

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
        :return: Generator: (`TweetRetweets`, list[`Tweet`])


    .. code-block:: python

       tweet = app.tweet_detail("1232515235253352")
       users = app.get_tweet_retweets(tweet)
       for user in users:
           print(user)


Getting Mentioned Tweets
---------------------

- .. py:method:: Twitter().get_mentions(pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_mentions(pages: int = 1, wait_time: int = 2, cursor: str = None)


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

       tweets = app.get_mentions()
       for tweet in tweets:
           print(tweet)


Getting Bookmarks
---------------------

- .. py:method:: Twitter().get_bookmarks(pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_bookmarks(pages: int = 1, wait_time: int = 2, cursor: str = None)


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

       tweets = app.get_bookmarks()
       for tweet in tweets:
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

       inbox = app.get_inbox()
       for conversation in inbox:
           print(conversation)

Sending Message
---------------------

- .. py:method:: Twitter().send_message(username: Union[str, int, User], text: str, file: Union[str, UploadedMedia] = None, in_group:bool = False)

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


    .. py:data:: Return

        :return: `Message`


    .. code-block:: python

       message = app.send_message("user", "Hi")

Creating a Tweet
---------------------

- .. py:method:: Twitter().create_tweet(text: str, files: list[Union[str, UploadedMedia, tuple[str, str]]] = None, filter_: str = None, reply_to: str = None, quote: str = None)

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

    .. py:data:: Return

        :return: `Tweet`


    .. code-block:: python

       message = app.create_tweet("user", reply_to="1690430294208483322")

Liking the Tweet
---------------------

- .. py:method:: Twitter().like_tweet(tweet_id: Union[str, int , Tweet])

    Post a Like on a Tweet

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Id of the Tweet


    .. py:data:: Return

        :return: bool


    .. code-block:: python

       app.like_tweet("123456789")

Un-Liking the Tweet
---------------------

- .. py:method:: Twitter().unlike_tweet(tweet_id: Union[str, int , Tweet])

    UnLike a Posted a Like on a Tweet

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Id of the Tweet


    .. py:data:: Return

        :return: bool


    .. code-block:: python

       app.unlike_tweet("123456789")

Retweeting the Tweet
---------------------

- .. py:method:: Twitter().retweet_tweet(tweet_id: Union[str, int , Tweet])

    Post a Retweet on a Tweet

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Id of the Tweet


    .. py:data:: Return

        :return: bool


    .. code-block:: python

       app.retweet_tweet("123456789")

Delete a Retweet
---------------------

- .. py:method:: Twitter().delete_retweet(tweet_id: Union[str, int , Tweet])

    Delete a Retweet on a Tweet

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Id of the Tweet


    .. py:data:: Return

        :return: bool


    .. code-block:: python

       app.delete_retweet("123456789")

Follow a User
---------------------

- .. py:method:: Twitter().follow_user(user_id: Union[str, int , User])

    Follow a User

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: `User`


    .. code-block:: python

       app.follow_user("123456789")

UnFollow a User
---------------------

- .. py:method:: Twitter().unfollow_user(user_id: Union[str, int , User])

    Un-Follow a User

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: `User`


    .. code-block:: python

       app.unfollow_user("123456789")

Block a User
---------------------

- .. py:method:: Twitter().block_user(user_id: Union[str, int , User])

    Block a User

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: `User`


    .. code-block:: python

       app.block_user("123456789")

Un-Block a User
---------------------

- .. py:method:: Twitter().unblock_user(user_id: Union[str, int , User])

    Block a User

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: `User`


    .. code-block:: python

       app.unblock_user("123456789")

Get Community
---------------------

- .. py:method:: Twitter().get_community(community_id: Union[str, int])

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
       app.get_community("123456789")

Get Community Tweets
---------------------

- .. py:method:: Twitter().get_community_tweets(community_id: str , pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_community_tweets(community_id: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)

    Get the Tweets of the specified community (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: community_id (Required)
            :type: str | Community

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
       tweets = app.get_community_tweets(12345678)
       for tweet in tweets:
           print(tweet)

Get Community Members
---------------------

- .. py:method:: Twitter().get_community_members(community_id: str , pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_community_members(community_id: str, pages: int = 1, filter_: str = None, wait_time: int = 2, cursor: str = None)

    Get the Members of the specified community (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: community_id (Required)
            :type: str | Community

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
       users = app.get_community_members(12345678)
       for user in users:
           print(user)

Delete Tweet
--------------
- .. py:method:: Twitter().delete_tweet(tweet_id: Union[str, int, Tweet])

    Delete a Tweet posted by authenticated user

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: str | int | Tweet

            Id of the Tweet

    .. py:data:: Return

        :return: Bool


    .. code-block:: python

       app.delete_tweet("123456789")

Enable User Notifications
--------------------------
- .. py:method:: Twitter().enable_user_notification(user_id: Union[str, int, User])

     Enable user notification on new tweet from specific user

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: Bool


    .. code-block:: python

       app.enable_user_notification("123456789")

Disable User Notifications
--------------------------
- .. py:method:: Twitter().disable_user_notification(user_id: Union[str, int, User])

     Disable user notification on new tweet from specific user

    .. py:data:: Arguments

        .. py:data:: user_id
            :type: str | int | User

            Id of the User

    .. py:data:: Return

        :return: Bool


    .. code-block:: python

       app.disable_user_notification("123456789")

Get Notified Tweets
---------------------

- .. py:method:: Twitter().get_tweet_notifications(pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_tweet_notifications(pages: int = 1, wait_time: int = 2, cursor: str = None)


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

       tweets = app.get_tweet_notifications()
       for tweet in tweets:
           print(tweet)

Get User Followers
---------------------

- .. py:method:: Twitter().get_user_followers(username: str , pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_user_followers(username: str , pages: int = 1, wait_time: int = 2, cursor: str = None)

    Get the Followers of specified User , (use `iter` for generator)

    .. py:data:: Arguments

        .. py:data:: username
            :type: str

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
       users = app.get_user_followers()
       for user in users:
           print(user)

Get User Followings
---------------------

- .. py:method:: Twitter().get_user_followings(username: str , pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_user_followings(username: str , pages: int = 1, wait_time: int = 2, cursor: str = None)

    Get the Followings of specified User , (use `iter` for generator)

    .. py:data:: Arguments

        .. py:data:: username
            :type: str

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
       users = app.get_user_followings()
       for user in users:
           print(user)

Get Tweet Comments
---------------------

- .. py:method:: Twitter().get_tweet_comments(tweet_id: int , pages: int = 1, wait_time: int = 2, cursor: str = None, get_hidden: bool = False)
- .. py:method:: Twitter().iter_tweet_comments(tweet_id: int , pages: int = 1, wait_time: int = 2, cursor: str = None, get_hidden: bool = False)

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
       threads = app.get_tweet_comments("123456789")
       for thread in threads:
           print(thread)

Get Lists
---------------------

- .. py:method:: Twitter().get_lists(pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_lists(pages: int = 1, wait_time: int = 2, cursor: str = None)

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

       lists = app.get_lists()
       for _list in lists:
           print(_list)

Create List
---------------------

- .. py:method:: Twitter().create_list(name: str, description: str = "", is_private: bool = False)

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

       _list = app.create_list("list_name")
       print(_list)

Delete List
---------------------

- .. py:method:: Twitter().delete_list(list_id: int)

    Delete a List using List ID if authenticated user is Admin

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str

            ID of Target List

    .. py:data:: Return

        :return: bool


    .. code-block:: python

       _list = app.delete_list("123515")
       print(_list)

Get List
---------------------

- .. py:method:: Twitter().get_list(list_id: int)

    Get a List using List ID

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str

            ID of Target List

    .. py:data:: Return

        :return: `TwList`


    .. code-block:: python

       _list = app.get_list("123515")
       print(_list)

Get List Tweets
---------------------

- .. py:method:: Twitter().get_list_tweets(list_id: int , pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_list_tweets(list_id: int , pages: int = 1, wait_time: int = 2, cursor: str = None)

    Get Tweets of specific List (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str

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

       tweets = app.get_list_tweets("123515")
       for tweet in tweets:
           print(tweet)


Get List Members
---------------------

- .. py:method:: Twitter().get_list_member(list_id: int , pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_list_member(list_id: int , pages: int = 1, wait_time: int = 2, cursor: str = None)

    Get Tweets of specific List (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str

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

       users = app.get_list_member("123515")
       for user in users:
           print(user)

Add List Member
---------------------

- .. py:method:: Twitter().add_list_member(list_id: int, user_id: int)

    Add a specific user from List

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str

            ID of Target List

        .. py:data:: user_id
            :type: int | str | User

            ID of User to be added

    .. py:data:: Return

        :return: `TwList`


    .. code-block:: python

       _list = app.add_list_member("123515", "elonmusk")
       print(_list)

Remove List Member
---------------------

- .. py:method:: Twitter().remove_list_member(list_id: int, user_id: int)

    Remove a specific user from List

    .. py:data:: Arguments

        .. py:data:: list_id
            :type: int | str

            ID of Target List

        .. py:data:: user_id
            :type: int | str | User

            ID of User to be added

    .. py:data:: Return

        :return: `TwList`


    .. code-block:: python

       _list = app.remove_list_member("123515", "elonmusk")
       print(_list)

Get Topic
---------------------

- .. py:method:: Twitter().get_topic(topic_id: Union[str, int])

    Get a topic using ID

    .. py:data:: Arguments

        .. py:data:: topic_id
            :type: int | str

            ID of Topic

    .. py:data:: Return

        :return: `Topic`


    .. code-block:: python

       topic = app.get_topic("123515")
       print(topic)

Get Topic Tweets
---------------------

- .. py:method:: Twitter().get_topic_tweets(topic_id: str , pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_topic_tweets(topic_id: str , pages: int = 1, wait_time: int = 2, cursor: str = None)

    Get the Tweets of the specified Topic (`iter` for generator)

    .. py:data:: Arguments

        .. py:data:: topic_id
            :type: str

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

       tweets = app.get_topic_tweets('123456')
       for tweet in tweets:
           print(tweet)

Get Tweet Analytics
---------------------

- .. py:method:: Twitter().get_tweet_analytics(tweet_id: Union[str, int, Tweet])

    Get Analytics of a Tweet (made by authenticated user)

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: int | str

            ID of Tweet

    .. py:data:: Return

        :return: `TweetAnalytics`


    .. code-block:: python

       tweet = app.get_tweet_analytics("123515")
       print(tweet)

Get Mutual Friends/Followers
---------------------

- .. py:method:: Twitter().get_mutual_followers(username: str , pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_mutual_followers(username: str , pages: int = 1, wait_time: int = 2, cursor: str = None)

    Get the Mutual Followers/Friends of a User (`iter` for generator)

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

        :return: `MutualFollowers`
        :return: Generator : (`MutualFollowers` , list[`User`])


    .. code-block:: python

       users = app.get_mutual_followers('elonmusk')
       for user in users:
           print(user)

Get Blocked Users
---------------------

- .. py:method:: Twitter().get_blocked_users(pages: int = 1, wait_time: int = 2, cursor: str = None)
- .. py:method:: Twitter().iter_blocked_users(pages: int = 1, wait_time: int = 2, cursor: str = None)

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

       users = app.get_blocked_users()
       for user in users:
           print(user)

Get Translated Tweet
---------------------

- .. py:method:: Twitter().translate_tweet(tweet_id: Union[str, int, Tweet], language: str)

    Get specific Tweet in a specific Language

    .. py:data:: Arguments

        .. py:data:: tweet_id
            :type: int | str

            ID of Tweet

        .. py:data:: language
            :type: str

            Language to which you want to translate


    .. py:data:: Return

        :return: `TweetTranslate`


    .. code-block:: python

       from tweety.filters import Language

       ...

       tweet = app.translate_tweet("123515", Language.English)
       print(tweet)