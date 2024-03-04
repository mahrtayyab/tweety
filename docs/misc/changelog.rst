.. _changelog:

=============
Changelogs
=============

Update 0.8:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.4
* More clean Code
* Added ``UserProtected`` exception to identify if the user is private
* Added ``place`` attribute to the `Tweet`
* Added ``card`` attribute to the `Tweet`

Update 1.0:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.5
* All Data Objects are JSON Serializable now (mostly)
* UserTweets and Search has been reworked alot , more details :ref:`all-functions`
* Now you can pass an additional ``cursor`` parameter to get_tweets and search functions
* Whole directory structure has been reworked , please do check documentation before upgrading

Update 1.0.1:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.5.2
* Fixed the ``sheet not Found`` error in ``to_xlsx()`` method
* Fixed ``NoneType`` error when Card has no choices
* Added ``is_quoted`` attribute to `Tweet`
* Added ``quoted_tweet`` attribute to `Tweet`
* Added ``quote_counts`` attribute to `Tweet`
* Added ``vibe`` attribute to `Tweet`
* Added ``is_possibly_sensitive`` attribute to `Tweet`
* Added ``username`` attribute to `User`
* Added ``possibly_sensitive`` attribute to `User`
* Added ``pinned_tweets`` attribute to `User`
* Early Adaptation to Twitter 2.0

Update 1.1:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.6.0
* Moved from `requests` to `httpx`
* Lot of Bug Fixes

Update 1.2:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.6.1
* ``quoted_tweet`` has been fixed
* New Attribute ``bookmark_count`` has been added
* Bug Fixes

Update 1.3:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.7
* Early Cookies implementations
* Now `get_tweets` accept the individual usernames, check `get_user_info </basic/all-functions.html#get-user-info>`_
* As search now requires user to be logged in , it will not work without cookies
* Extended All Exceptions with some additional attributes , check `exceptions </basic/exceptions.html>`_
* Removed ``wget`` , and added a custom implementation for download
* Added ``tqdm`` for download progress
* Removed `to_dict` in most methods , and all will be removed in future
* **Please** do check the full documentation before upgrading

Update 1.4:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.7.1
* Fixed 'TypeError: Union[arg, ...]'
* Completely Removed ``wget``
* Completely removed `to_dict` method
* Added ``bio`` ``description`` ``entities`` ``date`` attributes to `User`
* Added ``date`` attribute to `Tweet`
* Added New ``iter_tweets`` methods to `Twitter` ,  check `iter_tweets </basic/all-functions.html#id4>`_
* Added New ``iter_search`` methods to `Twitter` ,  check `iter_search </basic/all-functions.html#id18>`_
* **Please** do check the full documentation before upgrading

Update 1.5:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.8
* Many bug fixes
* Added new ``get_mentions`` , ``get_inbox``, ``send_message`` methods
* Cookies are now necessary
* Added ``can_dm`` attributes to `User`
* Added `RateLimitReached` new Exception
* Added New `Inbox`, `Conversation`, `Message`, `Mention`
* Added Event Listener
* **Please do check the full documentation before upgrading**

Update 1.6:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.9
* Many bug fixes
* Updated the `Twitter` Class
* Added `sign_in` method with session support
* Added `load_cookies` method
* **Please do check the full documentation before upgrading**


Update 1.7:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.9.5
* Fixed sign in issues
* Session file can only be saved and loaded from different directory
* Fixed the Proxy support , it would now work as expected.
* `send_message` can now send files too (only images)
* Added `DeniedLogin` Exception
* Added `create_tweet` method
* Added `get_bookmarks` , `iter_bookmarks` method
* Added ``MozillaCookieJar`` support to `load_cookies` method
* Removed tqdm totally , you can now pass your own ``progress_callback`` function
* **Please do check the full documentation before upgrading**

Update 1.7.1:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.9.6
* Fixed sign in issues once again
* **Please do check the full documentation before upgrading**

Update 1.8:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.9.9
* Added interactive version of `sign_in` called `start`
* Added New Exception `ActionRequired`
* Reworked `tweet_detail` , it will be fixed now
* Added New `get_home_timeline`, `iter_home_timeline`, `get_tweet_likes`, `iter_tweet_likes`, `get_tweet_retweets`, `iter_tweet_retweets`, `like_tweet`, `retweet_tweet`, `follow_user`, `unfollow_user` Methods
* ``TweetThreads`` has been renamed to `SelfThreads`
* Added new `ConversationThread`, `TweetRetweets`, `TweetLikes` Types
* `comments` in `Tweet` now returns list of `ConversationThread` Object
* Session file format renamed to ``tw_session``
* ``photos``, ``videos`` SearchFilter has been merged and renamed to `Media`
* Added `reply_to` argument to `create_tweet`
* **Please do check the full documentation before upgrading**

Update 1.8.1:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.9.9.1
* Fixed the Import Errors
* Fixed the annotation Errors
* **Please do check the full documentation before upgrading**

Update 1.9:
-------------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.9.9.5
* Fixed tweet comments pagination
* Added Video Upload Support
* Fixed the `create_tweet` issue
* Fixed the tweet`text` length issue
* Added `alt_text` to `Media`
* Added `create_pool`
* Added `Pool`
* Reworked `Choice`
* `wait_time` now accepts iterable
* Added `RichText` , `RichTag`
* Added `rich_text` attribute to `Tweet`
* Fixed `SelfThread` not able to parse the tweet
* Added `load_auth_token` method to AuthMethods
* Added `get_community`, `get_community_tweets`, `iter_community_tweet`, `get_community_members`, `iter_community_members` method to BotMethods
* Added `get_tweet_notifications`, `iter_tweet_notifications`, `enable_user_notification`, `disable_user_notification`, method to UserMethods
* Added `Community`, `CommunityTweets`, `CommunityMembers`, `TweetNotifications` Data Types
* **Please do check the full documentation before upgrading**

Update 2.0:
------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 1.0
* Added many new methods to Base `Twitter` Class, do check full documentation
* Added `best_stream` method to `Media` Class
* Added video upload
* Many bug fixes
* **Please do check the full documentation before upgrading**

Update 2.1:
------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 1.0.2
* Lot of bug fixes and code improvements

...

Update 3.1
--------------
- Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 1.0.9.6
- Alot of Bug Fixes
- Added `ProtectedTweet` Exception
- Added `URL`, `Hashtag` Type
- Added "tweet_edit_history" method
- Fixed `Inbox` Class
- Added `EditControl` Type
- Added `Symbol` Type
- Added `get_user_media` method
- Added `iter_user_media` method
- Added `is_liked`, `is_retweeted` attributes to `Tweet` class
- Added `get_next_page` and `get_next_page` method to `Conversation` class
- Added user id cache
- Optimized the `BaseGeneratorClass`
- SelfThread not being parsed is fixed
- Fixed issue when no user returned in inbox requests
- Added `get_topic` method
- Added `get_topic_tweets` method
- Create Tweet now supports quoting a Tweet
- Added `get_user_id` method
- Added `user_mentions`, `urls`, `hashtags`, `symbols` in `Message` object
- Added `get_mutual_followers` method
- Added `get_blocked_users` method
- Added `get_tweet_analytics` method
- Added `unlike_tweet` method
- Added `translate_tweet` method
