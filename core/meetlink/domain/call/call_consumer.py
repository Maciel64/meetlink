import json

from channels.generic.websocket import AsyncWebsocketConsumer


class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.EVENT_HANDLERS = (
            "MANAGER_NEEDED",
            "MANAGER_ENTERING",
            "INTERPRETER_ENTERING",
            "MANAGER_AND_INTERPRETER_NEEDED",
        )
        self.room_name = "test_room"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            event: str | None = data["event"]

            if event in self.EVENT_HANDLERS:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {"event": event, "type": event.lower(), "data": data},
                )

        except Exception as e:
            print(data)
            print("Erro ao decodificar JSON: ", e)

    async def manager_needed(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "event": event["event"],
                    "message": "Gerente necessário!",
                    "call": event["data"]["call"],
                }
            )
        )

    async def manager_entering(self, event):
        await self.send(
            text_data=json.dumps(
                {"event": event["event"], "message": "Gerente entrando!"}
            )
        )

    async def interpreter_entering(self, event):
        await self.send(
            text_data=json.dumps(
                {"event": event["event"], "message": "Intérprete entrando!"}
            )
        )

    async def manager_and_interpreter_needed(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "event": event["event"],
                    "message": "Gerente e interprete necessários!",
                    "call": event["data"]["call"],
                }
            )
        )
