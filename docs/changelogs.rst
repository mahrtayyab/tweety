ChangeLogs
=====================

Updates:
------------

Update 0.8:
^^^^^^^^^^^

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.4
* More clean Code
* Added ``UserProtected`` exception to identify if the user is private
* Added ``place`` attribute to the `Tweet Object <twDataTypes.html#tweet-section>`_
* Added ``card`` attribute to the `Tweet Object <twDataTypes.html#tweet-section>`_

Update 1.0:
^^^^^^^^^^^

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.5
* All Data Objects are JSON Serializable now (mostly)
* UserTweets and Search has been reworked alot , more details `here <twDataTypes.html>`_
* Now you can pass an additional ``cursor`` parameter to get_tweets and search functions
* Whole directory structure has been reworked , please do check documentation before upgrading

Update 1.0.1:
^^^^^^^^^^^

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.5.2
* Fixed the ``sheet not Found`` error in ``to_xlsx()`` method
* Fixed ``NoneType`` error when Card has no choices
* Added ``is_quoted`` attribute to `Tweet Object <twDataTypes.html#tweet-section>`_
* Added ``quoted_tweet`` attribute to `Tweet Object <twDataTypes.html#tweet-section>`_
* Added ``quote_counts`` attribute to `Tweet Object <twDataTypes.html#tweet-section>`_
* Added ``vibe`` attribute to `Tweet Object <twDataTypes.html#tweet-section>`_
* Added ``is_possibly_sensitive`` attribute to `Tweet Object <twDataTypes.html#tweet-section>`_
* Added ``username`` attribute to `User Object <#user-userlegacy-section>`_
* Added ``possibly_sensitive`` attribute to `User Object <#user-userlegacy-section>`_
* Added ``pinned_tweets`` attribute to `User Object <#user-userlegacy-section>`_
* Early Adaptation to Twitter 2.0
