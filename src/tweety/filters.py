
class SearchFilters:
    """
    This class can be used to filter the search results
    """
    @staticmethod
    def Users():
        return "users"

    @staticmethod
    def Latest():
        return "latest"

    @staticmethod
    def Photos():
        return "photos"

    @staticmethod
    def Videos():
        return "videos"


class TweetConversationFilters:
    """
    This class can be used to filter the audience of posted Tweet
    """
    @staticmethod
    def PeopleYouMention():
        return "ByInvitation"

    @staticmethod
    def PeopleYouFollow():
        return "Community"

