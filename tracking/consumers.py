from channels.generic.websocket import AsyncJsonWebsocketConsumer


class TrackingConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.ambulance_id = self.scope["url_route"]["kwargs"]["ambulance_id"]
        self.group_name = f"ambulance_{self.ambulance_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "tracking.update",
                "payload": content,
            },
        )

    async def tracking_update(self, event):
        await self.send_json(event["payload"])
