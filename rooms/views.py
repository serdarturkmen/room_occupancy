# Create your views here.
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status

from rooms.models import Room
from rooms.serializers import RoomSerializer


@api_view(['GET'])
def enter_occupant(request):
    if request.method == 'GET' and 'name' in request.GET:
        room = increaseOcuppant()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "occupancy", {"type": "user.occupancy",
                       "event": "Enter Occupant",
                       "count": room.count})

        return Response(status=200)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def exit_occupant(request):
    if request.method == 'GET' and 'name' in request.GET:
        room = decreaseOccuppant()
        name = request.GET["name"]
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "occupancy", {"type": "user.occupancy",
                       "event": "Exit Occupant",
                       "count": room.count})
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


def increaseOcuppant():
    room = Room.objects.get(pk=1)
    room.count = room.count + 1
    room.save()
    return room


def decreaseOccuppant():
    room = Room.objects.get(pk=1)
    room.count = room.count - 1
    room.save()
    return room


@csrf_exempt
@api_view(['GET', 'POST'])
def room_list(request):
    """
    List all code rooms, or create a new room.
    """
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def room_detail(request, pk):
    """
    Retrieve, update or delete a code room.
    """
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RoomSerializer(room, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        room.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

