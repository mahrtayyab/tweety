import base64
import datetime
import hashlib
import inspect
import json
import os.path
import random
import re
import string
import subprocess
import sys
import uuid
from typing import Union
from dateutil import parser as date_parser
from urllib.parse import urlparse, parse_qs
from .exceptions import AuthenticationRequired
from .filters import Language

GUEST_TOKEN_REGEX = re.compile("gt=(.*?);")
MIME_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jfif": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "webp": "image/webp",
    "mp4": "video/mp4",
    "mov": "video/quicktime",
    "m4v": "video/x-m4v"
}

WORKBOOK_HEADERS = ['Date', 'Author', 'id', 'text', 'is_retweet', 'is_reply', 'language', 'likes',
                    'retweet_count', 'source', 'medias', 'user_mentioned', 'urls', 'hashtags', 'symbols']

SENSITIVE_MEDIA_TAGS = ['adult_content', 'graphic_violence', 'other']


def AuthRequired(cls):
    def method_wrapper_decorator(func):
        def wrapper(self, *args, **kwargs):
            if self.me is None:
                raise AuthenticationRequired(200, "GenericForbidden", None)

            return func(self, *args, **kwargs)

        return wrapper

    if inspect.isclass(cls):
        for name, method in vars(cls).items():
            if name != "__init__" and callable(method):
                setattr(cls, name, method_wrapper_decorator(method))
        return cls
    return method_wrapper_decorator(cls)


def replace_between_indexes(original_string, from_index, to_index, replacement_text):
    new_string = original_string[:from_index] + replacement_text + original_string[to_index:]
    return new_string


def decodeBase64(encoded_string):
    return base64.b64decode(encoded_string).decode("utf-8")


def bar_progress(filename, total, current, width=80):
    progress_message = f"[{filename}] Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


def parse_wait_time(wait_time):
    if not wait_time:
        return 0

    if isinstance(wait_time, (tuple, list)):

        if len(wait_time) == 1:
            return int(wait_time[0])

        wait_time = [int(i) for i in wait_time[:2]]
        return random.randint(*wait_time)

    return int(wait_time)


def get_next_index(iterable, current_index, __default__=None):
    try:
        _ = iterable[current_index + 1]
        return current_index + 1
    except IndexError:
        return __default__


def custom_json(self, **kwargs):
    try:
        return json.loads(self.content, **kwargs)
    except:
        return None


def create_request_id():
    return str(uuid.uuid1())


def create_conversation_id(sender, receiver):
    sender = int(sender)
    receiver = int(receiver)

    if sender > receiver:
        return f"{receiver}-{sender}"
    else:
        return f"{sender}-{receiver}"


def create_query_id():
    return get_random_string(22)


def check_if_file_is_supported(file):
    if not str(file).startswith("https://") and not os.path.exists(file):
        raise ValueError("Path {} doesn't exists".format(file))

    file = file.split("?")[0]
    file_extension = file.split(".")[-1]

    if file_extension not in list(MIME_TYPES.keys()):
        raise ValueError("File Extension '{}' is not supported. Use any of {}".format(
            file_extension, list(MIME_TYPES.keys())
        ))

    return MIME_TYPES[file_extension]


def get_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=int(length)))


def calculate_md5(file_path):
    if str(file_path).startswith("https://"):
        return None

    md5_hash = hashlib.md5()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()


def create_media_entities(files):
    entities = []
    for file in files:
        media_id = file.media_id if hasattr(file, "media_id") else file
        entities.append({
            "media_id": media_id,
            "tagged_users": []
        })

    return entities


def check_sensitive_media_tags(tags):
    return [tag for tag in tags if tag in SENSITIVE_MEDIA_TAGS]


def find_objects(obj, key, value, recursive=True, none_value=None):
    results = []

    def find_matching_objects(_obj, _key, _value):
        if isinstance(_obj, dict):
            if _key in _obj:
                found = False
                if _value is None:
                    found = True
                    results.append(_obj[_key])
                elif (isinstance(_value, list) and _obj[_key] in _value) or _obj[_key] == _value:
                    found = True
                    results.append(_obj)

                if not recursive and found:
                    return results[0]

            for sub_obj in _obj.values():
                find_matching_objects(sub_obj, _key, _value)
        elif isinstance(_obj, list):
            for item in _obj:
                find_matching_objects(item, _key, _value)

    find_matching_objects(obj, key, value)

    if len(results) == 1:
        return results[0]

    if len(results) == 0:
        return none_value

    if not recursive:
        return results[0]

    return results


def create_pool(duration: int, *choices):
    data = {
        "twitter:long:duration_minutes": duration,
        "twitter:api:api:endpoint": "1",
        "twitter:card": f"poll{len(choices)}choice_text_only"
    }

    for index, choice in enumerate(choices, start=1):
        key = f"twitter:string:choice{index}_label"
        data[key] = choice

    return data


def parse_time(time):
    if not time:
        return None

    if isinstance(time, int) or str(time).isdigit():
        try:
            return datetime.datetime.fromtimestamp(int(time))
        except (OSError, ValueError):
            return datetime.datetime.fromtimestamp(int(time) / 1000)

    return date_parser.parse(time)


def get_user_from_typehead(target_username, users):
    for user in users:
        if str(user.username).lower() == str(target_username).lower():
            return user
    return None


def get_tweet_id(tweet_identifier):
    if str(tweet_identifier.__class__.__name__) == "Tweet":
        return tweet_identifier.id
    else:
        return urlparse(str(tweet_identifier)).path.split("/")[-1]


def is_tweet_protected(raw):
    return find_objects(raw, "__typename", ["TweetUnavailable", "TweetTombstone"], recursive=False)


def check_translation_lang(lang):
    for k, v in vars(Language).items():
        if not str(k).startswith("_"):
            if str(k).lower() == str(lang).lower() or str(v).lower() == str(lang).lower():
                return v

    raise ValueError(f"Language {lang} is not supported")


def iterable_to_string(__iterable__: Union[list, tuple], __delimiter__: str = ",", __attr__: str = None):
    if not isinstance(__iterable__, (list, tuple)) or len(__iterable__) == 0:
        return ""

    if __attr__:
        __iterable__ = [str(getattr(i, __attr__)) for i in __iterable__]

    return __delimiter__.join(__iterable__)


def dict_to_string(__dict__: dict, __object_delimiter__: str = "=", __end_delimiter__: str = ";"):
    actual_string = ""
    for key, value in __dict__.items():
        actual_string += f"{key}{__object_delimiter__}{value}{__end_delimiter__}"

    return actual_string


def get_url_parts(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    url_parts = {
        "scheme": parsed_url.scheme,
        "netloc": parsed_url.netloc,
        "path": parsed_url.path,
        "params": parsed_url.params,
        "query": query_params,
        "fragment": parsed_url.fragment,
        "host": f"{parsed_url.scheme}://{parsed_url.netloc}"
    }

    return url_parts


def unpack_proxy(proxy_dict):
    username, password, host, port = None, None, None, None
    if str(proxy_dict.__class__.__name__) == "Proxy":
        proxy_dict = proxy_dict.get_dict()

    proxy = proxy_dict.get("http://") or proxy_dict.get("https://")
    scheme, url = proxy.split("://")
    creds, host_with_port = None, None
    url_split = url.split("@")
    if len(url_split) == 2:
        creds, host_with_port = url_split
    else:
        host_with_port = url_split[0]

    host, port = host_with_port.split(":")
    if creds is not None:
        username, password = creds.split(":")

    return {
        "type": scheme,
        "host": host,
        "port": port,
        "username": username,
        "password": password
    }


def run_command(command):
    try:
        if isinstance(command, (list, tuple)):
            command = " ".join(command)

        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8')
    except subprocess.CalledProcessError as e:
        raise Exception(f"Command '{command}' failed with error: {e.stderr.decode('utf-8')}")


def encode_audio_message(input_filename, ffmpeg_path=None):
    """
    Encode the mp3 or audio file to Twitter Audio Message Format

    :param input_filename: Filename of mp3/ogg or audio file
    :param ffmpeg_path: Path of 'ffmpeg' binary for your platform
    :return: str (`encoded_filename`)
    """

    if not ffmpeg_path:
        ffmpeg_path = "ffmpeg"

    _input_filename = f'"{input_filename}"'
    _output_aac_filename = f'"{input_filename}.aac"'
    output_filename = f'"{input_filename}.mp4"'

    commands = [
        [ffmpeg_path, "-y", "-i", _input_filename, "-c:a", "aac", "-b:a", "65k", "-ar", "44100", "-ac", "1", _output_aac_filename],
        [ffmpeg_path, "-y", "-f", "lavfi", "-i", "color=c=black:s=854x480", "-i", _output_aac_filename, "-c:v", "libx264", "-c:a", "copy", "-shortest", output_filename]
    ]

    for command in commands:
        run_command(command)

    try:
        # Attempt to delete aac audio file in order to save disk space
        os.remove(_output_aac_filename)
    except:
        pass

    return output_filename[1:-1]

