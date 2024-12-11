import json
from channels.generic.websocket import AsyncWebsocketConsumer
from meetlink.domain.call.call_service import CallService
from meetlink.domain.call.call_repository import CallRepository

class CallConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.EVENT_HANDLERS = "MANAGER_NEEDED", "MANAGER_ENTERING"
        self.room_name = "test_room"
        self.room_group_name = f"chat_{self.room_name}"
        
        self.call_repository = CallRepository()
        self.call_service = CallService(self.call_repository)

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
            event: str | None = data.event

            if event in self.EVENT_HANDLERS :
                await self.channel_layer.group_send(self.room_group_name, {
                    "event": event,
                    "type": event.lower()
                })

        except Exception as e :
            print(text_data)
            print("Erro ao decodificar JSON: ", e)


    async def manager_needed(self, event) :
        self.call_service.create()

        await self.send(text_data=json.dumps({
            "event": event["event"],
            "message": "Gerente necessário!"
        }))


    async def manager_entering(self, event) :
        await self.send(text_data=json.dumps({
            "event": event["event"],
            "message": "Gerente entrando!"
        }))