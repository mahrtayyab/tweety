__version__ = "0.9.9.1"
__author__ = "mahrtayyab"

from .bot import BotMethods
from .updates import UpdateMethods
from .auth import AuthMethods
from .user import UserMethods


class Twitter(
    UserMethods, BotMethods, UpdateMethods, AuthMethods
):
    pass



