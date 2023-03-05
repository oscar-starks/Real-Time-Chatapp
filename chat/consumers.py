from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        # this was added for the group
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, 
            self.channel_name
        )
        
        self.accept()
        
        # this was for single channels, above, I'll be implementing the group layers so that it works properly like a group
        
        # self.send(text_data=json.dumps({
        #     'type':'connection established',
        #     'message':'connection successful'
        # })
        # )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        print('Received message: {}'.format(message))
        
        # self.send(text_data=json.dumps({
        #     'type':'chat',
        #     'message':message
        # }))
        
        
        # this section is also for the group layer
        
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, 
            {
                'type':'chat_message',
                'message':message
            }
        )
        
        
    def chat_message(self, event):
        message = event["message"]
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
        }))
        
        
        
# class ChatRoomConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name

        
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )
        
#         await self.accept()
        
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type':'tester_message',
#                 'tester': self.room_group_name + "__"+ self.room_name,                
#             }
#         )
#     async def tester_message(self, event):
#         tester = event['tester']
        
#         await self.send(text_data=json.dumps({
#             'tester': tester
#         }))
        
#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         ) 
        
#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         print(text_data_json)
#         message = text_data_json['message']
        
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type':'chat_message',
#                 'message': message,
#             }
#         ) 
    
#     async def chatroom_send(self, event):
#         message = event['message']
#         await self.send(text_data=json.dumps({
#             'message': message,
#         }))   
#     pass

