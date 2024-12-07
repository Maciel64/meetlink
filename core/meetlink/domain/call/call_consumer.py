import json
from channels.generic.websocket import AsyncWebsocketConsumer

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = "test_room"
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        try :
            data = json.loads(text_data)

            if data["event"] == "MANAGER_NEEDED" :
                await self.channel_layer.group_send(self.room_group_name, {
                    "event": "MANAGER_NEEDED",
                    "type": "manager_needed"
                })

            if data["event"] == "MANAGER_ENTERING" :
                await self.channel_layer.group_send(self.room_group_name, {
                    "event": "MANAGER_ENTERING",
                    "type": "manager_entering"
                })

        except Exception as e :
            print(text_data)
            print("Erro ao decodificar JSON: ", e)


    async def manager_needed(self, event) :
        await self.send(text_data=json.dumps({
            "event": event["event"],
            "message": "Gerente necessário!"
        }))


    async def manager_entering(self, event) :
        await self.send(text_data=json.dumps({
            "event": event["event"],
            "message": "Gerente entrando!"
        }))


    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({
            "message": message
        }))