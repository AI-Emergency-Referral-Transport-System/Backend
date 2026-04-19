import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.gis.geos import Point
from ambulances.models import Ambulance

class AmbulanceTrackingConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.emergency_id = self.scope['url_route']['kwargs']['emergency_id']
        self.room_group_name = f'emergency_{self.emergency_id}'

        # Only allow authenticated users to join a tracking room
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive data from the DRIVER app
    async def receive(self, text_data):
        data = json.loads(text_data)
        
        # Grounded logic: Extract the GPS data
        lat = data.get('lat')
        lon = data.get('lon')
        heading = data.get('heading', 0)

        # UPDATE THE DATABASE (Sync operation)
        await self.update_ambulance_location(lat, lon)

        # Broadcast the update to the PATIENT app (and anyone in the group)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'ambulance_location_update',
                'lat': lat,
                'lon': lon,
                'heading': heading
            }
        )

    @database_sync_to_async
    def update_ambulance_location(self, lat, lon):
        # This updates the actual PostGIS field in your Ambulance model
        new_point = Point(lon, lat, srid=4326)

        # Only update the ambulance belonging to the logged-in driver
        Ambulance.objects.filter(driver=self.user).update(current_location=new_point)

    # This method is triggered by the group_send above
    async def ambulance_location_update(self, event):
        # Push the data to the WebSocket (to the patient's screen)
        await self.send(text_data=json.dumps({
            'lat': event['lat'],
            'lon': event['lon'],
            'heading': event['heading']
        }))

class DispatchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Grab ambulance_id from the URL (from the regex named group)
        self.ambulance_id = self.scope['url_route']['kwargs']['ambulance_id']
        self.personal_group = f"ambulance_driver_{self.ambulance_id}"

        # Join their unique private group
        await self.channel_layer.group_add(self.personal_group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.personal_group, 
            self.channel_name
        )
    
    async def new_emergency_alert(self, event):
        # This only fires for the nearby drivers targeted by the view
        await self.send(text_data=json.dumps(event["data"]))
        