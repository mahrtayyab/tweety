import datetime
import json

from .base import BaseGeneratorClass
from . import GrokMessage
from ..utils import find_objects


class GrokConversation(BaseGeneratorClass):
    _RESULT_ATTR = "messages"

    def __init__(self, conversation_id, client, pages=1, wait_time=2, cursor=None):
        super().__init__()
        self.messages = []
        self.cursor = cursor
        self.cursor_top = cursor
        self.is_next_page = True
        self.client = client
        self.conversation_id = self.id = conversation_id
        self.pages = pages
        self.wait_time = wait_time

    async def get_page(self, cursor):
        this_items = []
        response = await self.client.http.get_grok_conversation_by_id(self.conversation_id, cursor)

        items = find_objects(response, "items", None, recursive=False)
        for item in items:
            this_items.append(GrokMessage(self.client, item))

        cursor = find_objects(response, "cursor", None, recursive=False, none_value=None)

        return this_items, cursor, None

    def __repr__(self):
        return "GrokConversation(id={}, messages={})".format(
            self.id, len(self.messages)
        )

    async def get_new_response(self, prompt_text):
        responses = []
        for i in self.messages:
            this_response = {
                "message": i.text,
                "sender": 2 if i.is_grok_response() else 1,
            }
            # if not i.is_grok_response():
            #     this_response["fileAttachments"] = i.attachments

            responses.append(this_response)

        responses.append({
            "message": prompt_text,
            "sender": 1
        })

        response = await self.client.http.get_new_grok_response(self.id, responses)

        grok_message_object = {
            "grok_mode": "Normal",
            "sender_type": "Agent",
            "file_attachments": []
        }

        message = ""
        lines = [i for i in response.content.split(b"\n") if i]
        for line in lines:
            json_data = json.loads(line)
            if json_data.get("result", {}).get("message"):
                message += json_data.get("result", {}).get("message", "")
            elif json_data.get("userChatItemId"):
                grok_message_object["chat_item_id"] = json_data["userChatItemId"]
            elif json_data.get("result", {}).get("webResults"):
                grok_message_object["cited_web_results"] = json_data["result"]["cited_web_results"]
            elif json_data.get("result", {}).get("xPostIds"):
                grok_message_object["tweet_ids"] = json_data["result"]["xPostIds"]
            elif json_data.get("result", {}).get("imageAttachment"):
                image = json_data["result"]["imageAttachment"]
                grok_message_object["file_attachments"].append(image)

        grok_message_object["message"] = message
        grok_message_object["created_at_ms"] = datetime.datetime.now(datetime.UTC)
        grok_message_object_parsed = GrokMessage(self.client, grok_message_object)
        self.messages.append(grok_message_object_parsed)
        return grok_message_object_parsed




