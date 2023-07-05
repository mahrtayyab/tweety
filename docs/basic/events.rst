.. _events:

===============
Events
===============

Using Tweety you can also listen to the events and respond to them.

Listen for new Message
-----------------------

.. attention:: Each triggered event will call the callback function in a new thread for time begin , in later versions , full async supprt will be added

.. py:class:: NewMessageUpdate

    :reference: `tweety.events.newmessage.NewMessageUpdate`

    You can listen to new messages using this method. Check the example below for reference

    .. code-block:: python

        from tweety.bot import Twitter


        cookies = cookies_value
        client = Twitter(cookies=cookies)
        @client.on(events.NewMessageUpdate)
        def newMessage(event):
             event.respond("OKAY")

        client.run_until_disconnected()

    The user will register a new event handler `NewMessageUpdate` which will start listening for new messages. When this event triggers
    the function `newMessage` will be called when one positional argument `event`. The class of this `event` is `NewMessage`


