__version__ = "1.0.9.5"
__author__ = "mahrtayyab"

from .bot import BotMethods
from .updates import UpdateMethods
from .auth import AuthMethods
from .user import UserMethods


class Twitter(
    UserMethods, BotMethods, UpdateMethods, AuthMethods
):
    pass



