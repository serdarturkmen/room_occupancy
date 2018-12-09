# Create your views here.
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rooms.models import Room
from rooms.serializers import RoomSerializer


def enter_occupant(request):
    if request.method == 'GET' and 'name' in request.GET:
        room = Room.objects.get(pk=1)
        room.count = room.count + 1
        room.save()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "occupancy", {"type": "user.occupancy",
                       "event": "Enter Occupant",
                       "count": room.count})

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


def exit_occupant(request):
    if request.method == 'GET' and 'name' in request.GET:
        room = Room.objects.get(pk=1)
        room.count = room.count - 1
        room.save()
        name =  request.GET["name"]
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "occupancy", {"type": "user.occupancy",
                       "event": "Exit Occupant",
                       "count": room.count})
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=404)


@csrf_exempt
def room_list(request):
    """
    List all code rooms, or create a new room.
    """
    if request.method == 'GET':
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def room_detail(request, pk):
    """
    Retrieve, update or delete a code room.
    """
    try:
        room = Room.objects.get(pk=pk)
    except Room.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = RoomSerializer(room)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = RoomSerializer(room, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        room.delete()
        return HttpResponse(status=204)

