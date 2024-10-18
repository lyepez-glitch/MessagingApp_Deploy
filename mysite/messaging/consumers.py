from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async


class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        from .models import Message  # Import your Message model
        self.group_name = 'chat_group'  # Use your own group name

        # Join group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave group
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        type_message = data.get('type')

        if type_message == 'update_message':
            print(type_message)
            content = data['content']
            message_id = data['message_id']
            sender_username = self.scope['user'].username  # Get the username from the request scope

            # Update the message in the database
            await self.update_message({
                'message_id': message_id,
                'new_content': content,
                'sender_username': sender_username,
})

            # Notify the group of the updated message
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message_id': message_id,
                    'content': content,
                    'sender_username': sender_username,  # Include sender's username
                }
            )
        elif type_message == 'create_message':  # Add this block for creating messages
            print(type_message)
            content = data['content']
            receiver_id = data['receiver_id']
            sender_username = self.scope['user'].username

            # Call create_message to save the message to the database
            message_id = await self.create_message(sender_username, receiver_id, content)



            # Send the message to the group
            await self.channel_layer.group_send(
                self.group_name,
                {
                    'type': 'chat_message',
                    'message_id': message_id,
                    'content': content,
                    'sender_username': sender_username,  # Include sender's username
                }
            )

    async def create_message(self, sender_username, receiver_id, content):
        # Fetch the User instance for the sender
        from django.contrib.auth.models import User
        from .models import Message
        sender = await database_sync_to_async(User.objects.get)(username=sender_username)

        # Create and save the message
        message = await database_sync_to_async(Message.objects.create)(
            sender=sender,
            receiver_id=receiver_id,
            content=content
        )
        return message.id  # Return the ID of the newly created message

    async def update_message(self, event):
        from .models import Message  # Import your Message model

        message_id = event['message_id']
        new_content = event['new_content']
        sender_username = event['sender_username']

        # Update the message in the database
        # Using database_sync_to_async to perform the database operation
        message = await database_sync_to_async(Message.objects.get)(id=message_id)  # Get the message by ID
        message.content = new_content  # Update the content
        await database_sync_to_async(message.save)()  # Save the updated message

        # Notify the group of the updated message
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',  # This should match the handler you have in the consumer
                'message_id': message_id,
                'content': new_content,
                'sender_username': sender_username,  # Include sender's username
            }
        )
        # Notify the user to redirect
        await self.send(text_data=json.dumps({
            'type': 'redirect',  # New message type for redirection
            'url': '/rooms/dashboard',  # URL to redirect to
        }))



    async def chat_message(self, event):
        content = event['content']
        sender_username = event['sender_username']
        message_id = event.get('message_id', None)  # Get message_id from the event if it exists

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'event': 'new_message',  # Differentiate between new and updated messages
            'message_id': message_id,  # Send message_id back
            'content': content,
            'sender_username': sender_username,
        }))

