.. _installation:

============
Installation
============

Tweety is a Python library, which means you need to download and install
Python from https://www.python.org/downloads/ if you haven't already. Once
you have Python installed, `upgrade pip`__ and run:

.. code-block:: sh

    python3 -m pip install --upgrade pip
    python3 -m pip install --upgrade tweety-ns

.. __: https://pythonspeed.com/articles/upgrade-pip/

**Please** do check the full documentation before upgrading if upgrading to new version

Dependencies
=====================

httpx_ : The library will be used to make the http/2 requests to Twitter

dateutil_ : The library will be used to parse the dates in the http response

openpyxl_ : The library will be used to save the responses as an Excel Sheet


.. _httpx: https://github.com/encode/httpx
.. _dateutil: https://github.com/dateutil/dateutil
.. _openpyxl: https://github.com/theorchard/openpyxl