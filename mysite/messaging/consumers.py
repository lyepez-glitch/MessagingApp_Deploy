import json
from channels.generic.websocket import AsyncWebsocketConsumer

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("Client connected")
        await self.accept()

    async def disconnect(self, close_code):
        print("Client disconnected")

    async def receive(self, text_data):
        print(f"Message received: {text_data}")
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
