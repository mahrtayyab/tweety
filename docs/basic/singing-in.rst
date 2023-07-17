
.. _singing-in:

=============
Signing In
=============

The Twitter requires user to logged-in, in order to get any information. In this section you can check how can you sign to Twitter using tweety.

Before Singing In , please make sure you already have account on Twitter


Singing In using Credentials
----------------------------
You can login to Twitter on Tweety using your `username` and `password`

.. code-block:: python

    from tweety import Twitter

    app = Twitter("session")
    app.sign_in(username, password)
    print(app.user)


- By running this code , the Tweety will login to Twitter using the ``username`` and ``password`` provided , and if the request was successful , the authentication cookies obtained from response will be saved in ``session.json`` (filename is subject to the name of session) file in your current directory

Singing In using Cookies
----------------------------
you can also log-in to Twitter on Tweety using ``Cookies``.

.. code-block:: python

    from tweety import Twitter

    cookies_value = """guest_id=guest_id_value; guest_id_marketing=guest_id_marketing; guest_id_ads=guest_id_ads; kdt=kdt_value; auth_token=auth_token_value; ct0=ct0_value; twid=twid_value; personalization_id="personalization_id_value" """

    # Cookies can be a str or a dict

    app = Twitter("session")
    app.load_cookies(cookies_value)
    print(app.user)


- By running this code ,if the request was successful , the authentication cookies obtained from response will be saved in ``session.json`` (filename is subject to the name of session) file in your current directory


Singing In using previous session
----------------------------------

Signing in using previous session requires a session file in the current directory of the script. Either you run `sign_in` or `load_cookies` , it will save the session in the session file named as the `session` argument provided to `Twitter` class.

If the 'session' was passed as an argument of `session` to `Twitter` , your session will be save in `session.json` file , if it is 'kharltayyab' , session will be saved in `kharltayyab.json`

Now using the same session name ,you can load the previous session from file


.. code-block:: python

    from tweety import Twitter

    app = Twitter("session")
    app.connect()
    # as 'session.json' is already a authenticated session file , the session can be loaded using  `connect` method

    print(app.user)

