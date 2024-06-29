
class _CallableString(str):
    """

    For backward compatibility where user can still call the attributes as method

    """
    def __init__(self, __value__):
        super().__init__()

    def __call__(self, *args, **kwargs):
        return self


class SearchFilters:
    """
    This class can be used to filter the search results
    """
    Users = _CallableString("People")
    Latest = _CallableString("Latest")
    Media = _CallableString("Media")
    Lists = _CallableString("Lists")


class TweetConversationFilters:
    """
    This class can be used to filter the audience of posted Tweet
    """

    PeopleYouMention = _CallableString("ByInvitation")
    PeopleYouFollow = _CallableString("Community")
    Subscribers = _CallableString("Subscribers")
    VerifiedUsers = _CallableString("Verified")


class CommunityTweets:
    Top = _CallableString("Top")


class CommunityMembers:
    Moderators = _CallableString("Mods")


class Language:
    Urdu = URDU = _CallableString("ur")
    Russian = RUSSIAN = _CallableString("ru")
    Danish = DANISH = _CallableString("da")
    Filipino = FILIPINO = _CallableString("fil")
    Irish = IRISH = _CallableString("ga")
    TraditionalChinese = TRADITIONAL_CHINESE = _CallableString("zh-tw")
    Hungarian = HUNGARIAN = _CallableString("hu")
    Spanish = SPANISH = _CallableString("es")
    Arabic_Feminine = ARABIC_FEMININE = _CallableString("ar-x-fm")
    Croatian = CROATIAN = _CallableString("hr")
    French = FRENCH = _CallableString("fr")
    Kannada = KANNADA = _CallableString("kn")
    Italian = ITALIAN = _CallableString("it")
    Marathi = MARATHI = _CallableString("mr")
    Japanese = JAPANESE = _CallableString("ja")
    Indonesian = INDONESIAN = _CallableString("id")
    Gujarati = GUJARATI = _CallableString("gu")
    Romanian = ROMANIAN = _CallableString("ro")
    Turkish = TURKISH = _CallableString("tr")
    Basque = BASQUE = _CallableString("eu")
    Swedish = SWEDISH = _CallableString("sv")
    Tamil = TAMIL = _CallableString("ta")
    Thai = THAI = _CallableString("th")
    Ukrainian = UKRAINIAN = _CallableString("uk")
    Bangla = BANGLA = _CallableString("bn")
    German = GERMAN = _CallableString("de")
    Vietnamese = VIETNAMESE = _CallableString("vi")
    Catalan = CATALAN = _CallableString("ca")
    Arabic = ARABIC = _CallableString("ar")
    Dutch = DUTCH = _CallableString("nl")
    SimplifiedChinese = SIMPLIFIED_CHINESE = _CallableString("zh-cn")
    Slovak = SLOVAK = _CallableString("sk")
    Czech = CZECH = _CallableString("cs")
    Greek = GREEK = _CallableString("el")
    Finnish = FINNISH = _CallableString("fi")
    English = ENGLISH = _CallableString("en")
    Norwegian = NORWEGIAN = _CallableString("no")
    Polish = POLISH = _CallableString("pl")
    Portuguese = PORTUGUESE = _CallableString("pt")
    Persian = PERSIAN = _CallableString("fa")
    Galician = GALICIAN = _CallableString("gl")
    Korean = KOREAN = _CallableString("ko")
    Serbian = SERBIAN = _CallableString("sr")
    BritishEnglish = BRITISH_ENGLISH = _CallableString("en-gb")
    Hindi = HINDI = _CallableString("hi")
    Hebrew = HEBREW = _CallableString("he")
    Malay = MALAY = _CallableString("msa")
    Bulgarian = BULGARIAN = _CallableString("bg")