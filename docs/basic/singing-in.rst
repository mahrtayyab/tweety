
.. _singing-in:

=============
Signing In
=============

The Twitter requires user to logged-in, in order to get any information. In this section you can check how can you sign to Twitter using tweety.

Before Singing In , please make sure you already have account on Twitter


Interactive Singing In
------------------------
Most of the time , `start` is the only method you will interact with to login and create a session
This Method will ask for `Username`,  `Password` or any other information or action required for completing the log-in process.

.. code-block:: python

    from tweety import Twitter

    app = Twitter("session")
    app.start(username, password, extra=extra)
    print(app.user)

- Arguments `username` , `password` and `extra` are optional

- Running the above code will first look for saved session, if found will resume that session
- If not found , it will ask for `Username` if not provided
- Then it will ask for `password` if not provided
- Then it will start the login Flow
- If any other information like 2-Factor Authentication Code , or Verification , it will ask for it

.. code-block:: bash

    Action Required :> Please Enter the 2-Factor Authentication from the Authenticator App : 000000


Singing In using Credentials
----------------------------
You can login to Twitter on Tweety using your `username` and `password`

.. code-block:: python

    from tweety import Twitter

    app = Twitter("session")
    app.sign_in(username, password)
    print(app.user)


- By running this code ,
- the Tweety will login to Twitter using the ``username`` and ``password`` provided ,
- and if the request was successful , the authentication cookies obtained from response will be saved in ``session.tw_session`` (filename is subject to the name of session) file.

- If any other information like 2-Factor Authenticated Code , or Verification id required , the `ActionRequired` will be raised
- In case of `ActionRequired` , you can pass the required information to `extra` argument of `sign_in` method

.. code-block:: python

    from tweety import Twitter

    app = Twitter("session")
    try:
        app.sign_in(username, password, extra=extra)
    except ActionRequired as e:
        action = input(f"Action Required :> {str(e.message)} : ")
        app.sign_in(username, password, extra=action)

Singing In using Cookies
----------------------------
you can also log-in to Twitter on Tweety using ``Cookies``.

.. code-block:: python

    from tweety import Twitter

    cookies_value = """guest_id=guest_id_value; guest_id_marketing=guest_id_marketing; guest_id_ads=guest_id_ads; kdt=kdt_value; auth_token=auth_token_value; ct0=ct0_value; twid=twid_value; personalization_id="personalization_id_value" """

    # Cookies can be a str or a dict

    app = Twitter("session")
    app.load_cookies(cookies_value)
    print(app.me)


- By running this code ,if the request was successful , the authentication cookies obtained from response will be saved in ``session.tw_session`` (filename is subject to the name of session) file.

Singing In using Auth Token
----------------------------
you can also log-in to Twitter on Tweety using ``auth_token``.

.. code-block:: python

    from tweety import Twitter

    auth_token = """auth_token_value"""

    # Cookies can be a str or a dict

    app = Twitter("session")
    app.load_auth_token(auth_token)
    print(app.me)


- By running this code ,if the request was successful , the authentication cookies obtained from response will be saved in ``session.tw_session`` (filename is subject to the name of session) file.



Singing In using previous session
----------------------------------

Signing in using previous session requires a session file in the current directory of the script. Either you run `sign_in` or `load_cookies` , it will save the session in the session file named as the `session` argument provided to `Twitter` class.

If the 'session' was passed as an argument of `session` to `Twitter` , your session will be save in `session.tw_session` file , if it is 'kharltayyab' , session will be saved in `kharltayyab.tw_session`

Now using the same session name ,you can load the previous session from file

.. attention:: If the session file is in different directory , make sure to provide the relative path.

.. code-block:: python

    from tweety import Twitter

    app = Twitter("session")
    app.connect()
    # as 'session.tw_session' is already a authenticated session file , the session can be loaded using  `connect` method

    print(app.me)


