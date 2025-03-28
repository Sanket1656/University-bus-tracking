import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BusLocationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()  # Accept the WebSocket connection

    async def disconnect(self, close_code):
        pass  # No special handling on disconnect

    async def receive(self, text_data):
        data = json.loads(text_data)
        latitude = data.get("latitude")
        longitude = data.get("longitude")

        # Send the received location back to the client
        await self.send(text_data=json.dumps({
            "latitude": latitude,
            "longitude": longitude
        }))
