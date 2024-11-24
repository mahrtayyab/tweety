__version__ = "2.0.3"
__author__ = "mahrtayyab"


import inspect
from .bot import BotMethods
from .updates import UpdateMethods
from .auth import AuthMethods
from .user import UserMethods
from .utils import get_running_loop


def SyncWrap(cls):
    def method_wrapper_decorator(method_):
        def wrapper(self, *args, **kwargs):
            coro = method_(self, *args, **kwargs)
            loop = get_running_loop()
            if loop.is_running():
                return coro
            else:
                return loop.run_until_complete(coro)

        return wrapper

    if inspect.isclass(cls):
        for name in dir(cls):
            if not name.startswith('_') or name != '__init__':
                if inspect.iscoroutinefunction(getattr(cls, name)):
                    setattr(cls, name, method_wrapper_decorator(getattr(cls, name)))

        return cls
    return method_wrapper_decorator(cls)


class TwitterAsync(
    UserMethods, BotMethods, UpdateMethods, AuthMethods
):
    pass


@SyncWrap
class Twitter(TwitterAsync):
    pass


