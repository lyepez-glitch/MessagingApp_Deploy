from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = 'chat_group'  # Use your own group name

        # Join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        content = data['content']
        receiver_id = data['receiver_id']
        sender_username = self.scope['user'].username  # Get the username from the request scope

        # Send the message to the group
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'content': content,
                'sender_username': sender_username,  # Include sender's username
            }
        )

    async def chat_message(self, event):
        content = event['content']
        sender_username = event['sender_username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'content': content,
            'sender_username': sender_username,  # Send sender's username back
        }))
