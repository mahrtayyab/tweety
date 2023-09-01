
class SearchFilters:
    """
    This class can be used to filter the search results
    """
    @staticmethod
    def Users():
        return "People"

    @staticmethod
    def Latest():
        return "Latest"

    @staticmethod
    def Media():
        return "Media"


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

