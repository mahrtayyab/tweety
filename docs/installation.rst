Dependencies
------------

These distributions will be installed automatically when installing Tweety.

* `beautifulsoup4`_ - used to scrape some elements required for twitter headers
* `requests`_ - used to make http requests to Twitter
* `openpyxl`_ - used to convert the Twitter response to an Excel Sheet
* `dateutils`_ - used to parse the dates in Twitter response

.. _beautifulsoup4: https://pypi.org/project/beautifulsoup4/
.. _requests: https://pypi.org/project/requests/
.. _openpyxl: https://pypi.org/project/openpyxl/
.. _dateutils: https://pypi.org/project/dateutils/


Optional dependencies
~~~~~~~~~~~~~~~~~~~~~

These distributions will not be installed automatically. Tweety will detect and
use them if you install them.

* `wget`_ - used to download the media from tweet right inside the script

.. _wget: https://pypi.org/project/wget/


Install Tweety
-------------

On your Terminal use the following command to install Tweety:

.. code-block:: sh

    $ pip install tweety-ns

Tweety is now installed. Check out the :doc:`/quickstart` or go to the
:doc:`Documentation Overview </index>`.