from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print(self.scope)

        self.group_name = 'chat_group'
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        from .models import Message  # Import here to avoid AppRegistryNotReady error

        data = json.loads(text_data)
        message_content = data['content']
        receiver_id = data.get('receiver_id')  # Get the receiver ID if it's provided

        # Get the actual User instance from the scope
        user = self.scope['user']

        if user.is_authenticated:
            # Save the message to your database
            await database_sync_to_async(Message.objects.create)(
                content=message_content,
                sender=user,  # Use the User instance
                receiver_id=receiver_id
            )

            # Broadcast the message to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'content': message_content
                }
            )
        else:
            # Handle unauthenticated user case if necessary
            await self.send(text_data=json.dumps({
                'error': 'User not authenticated'
            }))

    async def chat_message(self, event):
        message = event['content']
        await self.send(text_data=json.dumps({
            'content': message
        }))
