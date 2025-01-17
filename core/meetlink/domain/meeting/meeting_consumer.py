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

        if type == "offer" or type == "answer":
            receiver_channel = data.get("channel")
            channel_name = self.channel_name

            await self.channel_layer.send(
                receiver_channel,
                {
                    "type": type,
                    "sdp": data["sdp"],
                    "channel": channel_name,
                    "senderId": data["senderId"],
                },
            )

        elif type == "join":
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "join",
                    "channel": self.channel_name,
                    "senderId": data["senderId"],
                },
            )

    async def offer(self, event):
        if self.channel_name != event["channel"]:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "offer",
                        "sdp": event["sdp"],
                        "channel": event["channel"],
                        "senderId": event["senderId"],
                    }
                )
            )

    async def answer(self, event):
        if self.channel_name != event["channel"]:
            await self.send(
                text_data=json.dumps(
                    {
                        "type": "answer",
                        "sdp": event["sdp"],
                        "channel": event["channel"],
                        "senderId": event["senderId"],
                    }
                )
            )

    async def join(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "type": "join",
                    "channel": event["channel"],
                    "senderId": event["senderId"],
                }
            )
        )
