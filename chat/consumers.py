from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync

# class ChatConsumer(WebsocketConsumer):
#     def connect(self):
#         self.room_group_name = 'test'
#         # this was added for the group
        
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name, 
#             self.channel_name
#         )
        
#         self.accept()
        
#         # this was for single channels, above, I'll be implementing the group layers so that it works properly like a group
        
#         # self.send(text_data=json.dumps({
#         #     'type':'connection established',
#         #     'message':'connection successful'
#         # })
#         # )

#     def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json['message']
        
#         print('Received message: {}'.format(message))
        
#         # self.send(text_data=json.dumps({
#         #     'type':'chat',
#         #     'message':message
#         # }))
        
        
#         # this section is also for the group layer
        
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name, 
#             {
#                 'type':'chat_message',
#                 'message':message
#             }
#         )
        
        
#     def chat_message(self, event):
#         message = event["message"]
#         self.send(text_data=json.dumps({
#             'type':'chat',
#             'message':message
#         }))
        
    
#     def disconnect(self, code):
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name, self.channel_name
#         )
        
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'test'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name)
        await self.accept()
        
        await self.send(text_data=json.dumps({
            'type':'connection established',
            'message':'connection successful'
        })
        )
        
        
    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        
        print('Received message: {}'.format(message))

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat_message", "message": message}
        )
    
    async def chat_message(self, event):
        message = event["message"]
        
        await self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))
        