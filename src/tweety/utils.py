import random
import string


def custom_json(self):
    try:
        return self.json()
    except:
        return None


def create_request_id():
    i = "________-____-____-_____-_____________"
    result = ""
    for index, p in enumerate(i):
        if p == "_":
            j = random.choice([n for n in string.ascii_lowercase + string.digits])
        else:
            j = "-"
        result = result + j
    return result


def create_conversation_id(sender, receiver):
    sender = int(sender)
    receiver = int(receiver)

    if sender > receiver:
        return f"{receiver}-{sender}"
    else:
        return f"{sender}-{receiver}"
