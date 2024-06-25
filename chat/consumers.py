import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(" connected")
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        print("recieved message")
        await self.send(text_data=json.dumps({
            'message': text_data
        }))
