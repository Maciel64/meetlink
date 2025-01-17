import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MeetingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "meeting_room"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data.get("type")

        if type == "offer":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "offer",
                    "sdp": data["sdp"],
                    "sender": self.channel_name,
                },
            )
        elif type == "answer":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "answer",
                    "sdp": data["sdp"],
                    "sender": self.channel_name,
                },
            )
        elif type == "candidate":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "candidate",
                    "candidate": data["candidate"],
                    "sender": self.channel_name,
                },
            )

    async def offer(self, event):
        if self.channel_name != event["sender"]:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "offer",
                        "sdp": event["sdp"],
                        "sender": event["sender"],
                    }
                )
            )

    async def answer(self, event):
        if self.channel_name != event["sender"]:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "answer",
                        "sdp": event["sdp"],
                        "sender": event["sender"],
                    }
                )
            )

    async def candidate(self, event):
        if self.channel_name != event["sender"]:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "candidate",
                        "candidate": event["candidate"],
                        "sender": event["sender"],
                    }
                )
            )
