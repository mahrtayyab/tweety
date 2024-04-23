
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

    @staticmethod
    def Lists():
        return "Lists"


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

class CommunityTweets:
    @staticmethod
    def Top():
        return "Top"


class CommunityMembers:
    @staticmethod
    def Moderators():
        return "Mods"


class Language:
    Urdu = URDU = "ur"
    Russian = RUSSIAN = "ru"
    Danish = DANISH = "da"
    Filipino = FILIPINO = "fil"
    Irish = IRISH = "ga"
    TraditionalChinese = TRADITIONAL_CHINESE = "zh-tw"
    Hungarian = HUNGARIAN = "hu"
    Spanish = SPANISH = "es"
    Arabic_Feminine = ARABIC_FEMININE = "ar-x-fm"
    Croatian = CROATIAN = "hr"
    French = FRENCH = "fr"
    Kannada = KANNADA = "kn"
    Italian = ITALIAN = "it"
    Marathi = MARATHI = "mr"
    Japanese = JAPANESE = "ja"
    Indonesian = INDONESIAN = "id"
    Gujarati = GUJARATI = "gu"
    Romanian = ROMANIAN = "ro"
    Turkish = TURKISH = "tr"
    Basque = BASQUE = "eu"
    Swedish = SWEDISH = "sv"
    Tamil = TAMIL = "ta"
    Thai = THAI = "th"
    Ukrainian = UKRAINIAN = "uk"
    Bangla = BANGLA = "bn"
    German = GERMAN = "de"
    Vietnamese = VIETNAMESE = "vi"
    Catalan = CATALAN = "ca"
    Arabic = ARABIC = "ar"
    Dutch = DUTCH = "nl"
    SimplifiedChinese = SIMPLIFIED_CHINESE = "zh-cn"
    Slovak = SLOVAK = "sk"
    Czech = CZECH = "cs"
    Greek = GREEK = "el"
    Finnish = FINNISH = "fi"
    English = ENGLISH = "en"
    Norwegian = NORWEGIAN = "no"
    Polish = POLISH = "pl"
    Portuguese = PORTUGUESE = "pt"
    Persian = PERSIAN = "fa"
    Galician = GALICIAN = "gl"
    Korean = KOREAN = "ko"
    Serbian = SERBIAN = "sr"
    BritishEnglish = BRITISH_ENGLISH = "en-gb"
    Hindi = HINDI = "hi"
    Hebrew = HEBREW = "he"
    Malay = MALAY = "msa"
    Bulgarian = BULGARIAN = "bg"