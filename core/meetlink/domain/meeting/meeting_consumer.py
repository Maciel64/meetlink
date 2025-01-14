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
                    "offer": data["offer"],
                    "sender": self.channel_name,
                    "userId": data["userId"],
                },
            )
        elif type == "answer":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "answer",
                    "answer": data["answer"],
                    "sender": self.channel_name,
                    "userId": data["userId"],
                },
            )
        elif type == "candidate":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "candidate",
                    "candidate": data["candidate"],
                    "sender": self.channel_name,
                    "userId": data["userId"],
                },
            )

    async def offer(self, event):
        if self.channel_name != event["sender"]:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "offer",
                        "offer": event["offer"],
                        "sender": event["sender"],
                        "userId": event["userId"],
                    }
                )
            )

    async def answer(self, event):
        if self.channel_name != event["sender"]:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "answer",
                        "answer": event["answer"],
                        "sender": event["sender"],
                        "userId": event["userId"],
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
                        "userId": event["userId"],
                    }
                )
            )
