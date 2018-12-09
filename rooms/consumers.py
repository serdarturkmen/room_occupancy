from channels.generic.websocket import AsyncJsonWebsocketConsumer

from rooms.models import Room


def resetRoomCount():
    try:
        room = Room.objects.get(pk=1)
        room.count = 0
        room.save()
    except Room.DoesNotExist:
        room = Room(id=1, name="sample room", count=1)
        room.save()


class Consumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        resetRoomCount()
        await self.accept()
        await self.channel_layer.group_add("occupancy", self.channel_name)
        print(f"Added {self.channel_name} channel to occupancy")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("occupancy", self.channel_name)
        print(f"Removed {self.channel_name} channel to occupancy")

    async def user_occupancy(self, event):
        await self.send_json(event)
        print(f"Got message {event} at {self.channel_name}")
