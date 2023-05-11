.. _changelog:

=============
Changelogs
=============

Update 0.8:
------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.4
* More clean Code
* Added ``UserProtected`` exception to identify if the user is private
* Added ``place`` attribute to the `Tweet`
* Added ``card`` attribute to the `Tweet`

Update 1.0:
-----------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.5
* All Data Objects are JSON Serializable now (mostly)
* UserTweets and Search has been reworked alot , more details :ref:`all-functions`
* Now you can pass an additional ``cursor`` parameter to get_tweets and search functions
* Whole directory structure has been reworked , please do check documentation before upgrading

Update 1.0.1:
-------------

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
-----------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.6.0
* Moved from `requests` to `httpx`
* Lot of Bug Fixes

Update 1.2:
------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.6.1
* ``quoted_tweet`` has been fixed
* New Attribute ``bookmark_count`` has been added
* Bug Fixes

Update 1.3:
------------

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
------------

* Module version on `PYPI Repository <https://pypi.org/project/tweety-ns/>`_ is bumped to 0.7.1
* Fixed 'TypeError: Union[arg, ...]'
* Completely Removed ``wget``
* Completely removed `to_dict` method
* Added ``bio`` ``description`` ``entities`` ``date`` attributes to `User`
* Added ``date`` attribute to `Tweet`
* Added New ``iter_tweets`` methods to `Twitter` ,  check `iter_tweets </basic/all-functions.html#id4>`_
* Added New ``iter_search`` methods to `Twitter` ,  check `iter_search </basic/all-functions.html#id18>`_
* **Please** do check the full documentation before upgrading