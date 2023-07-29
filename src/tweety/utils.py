import base64
import hashlib
import os.path
import random
import string
import sys
import uuid
from typing import Callable, Any

MIME_TYPES = {
    "png": "image/png",
    "jpg": "image/jpeg",
    "jfif": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "webp": "image/webp"
}
# "mp4": "video/mp4",
# "mov": "video/quicktime",
# "m4v": "video/x-m4v"


WORKBOOK_HEADERS = ['Date', 'Author', 'id', 'text', 'is_retweet', 'is_reply', 'language', 'likes',
                    'retweet_count', 'source', 'medias', 'user_mentioned', 'urls', 'hashtags', 'symbols']

SENSITIVE_MEDIA_TAGS = ['adult_content', 'graphic_violence', 'other']


def decodeBase64(encoded_string):
    return str(base64.b64decode(bytes(encoded_string, "utf-8")))[2:-1]


def bar_progress(current, total, width=80):
    progress_message = "Downloading: %d%% [%d / %d] bytes" % (current / total * 100, current, total)
    sys.stdout.write("\r" + progress_message)
    sys.stdout.flush()


def custom_json(self):
    try:
        return self.json()
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


def check_if_file_is_image(file):
    if not os.path.exists(file):
        raise ValueError("Path {} doesn't exists".format(file))

    file_extension = file.split(".")[-1]

    if file_extension not in list(MIME_TYPES.keys()):
        raise ValueError("File Extension '{}' is not supported. Use any of {}".format(
            file_extension, list(MIME_TYPES.keys())
        ))

    return MIME_TYPES[file_extension]


def get_random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=int(length)))


def calculate_md5(file_path):
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


def find_object(obj: dict, fn: Callable[[dict], bool]) -> Any | None:
    if not isinstance(obj, dict):
        return None

    if fn(obj):
        return obj

    for _, v in obj.items():
        if isinstance(v, dict):
            if res := find_object(v, fn):
                return res
        elif isinstance(v, list):
            for x in v:
                if res := find_object(x, fn):
                    return res

    return None

