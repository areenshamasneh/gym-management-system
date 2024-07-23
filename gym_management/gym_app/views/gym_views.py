from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
from ..models import Gym


@method_decorator(csrf_exempt, name="dispatch")
class GymListView(View):
    def get(self, request):
        gyms = Gym.objects.all().values()
        return JsonResponse(list(gyms), safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class GymDetailView(View):
    def get(self, request, pk):
        gym = get_object_or_404(Gym, pk=pk)
        gym_data = {
            "id": gym.id,
            "name": gym.name,
            "type": gym.type,
            "description": gym.description,
            "address_city": gym.address_city,
            "address_street": gym.address_street,
        }
        return JsonResponse(gym_data)


@method_decorator(csrf_exempt, name="dispatch")
class GymCreateView(View):
    def post(self, request):
        data = json.loads(request.body)
        gym = Gym.objects.create(
            name=data.get("name"),
            type=data.get("type"),
            description=data.get("description"),
            address_city=data.get("address_city"),
            address_street=data.get("address_street"),
        )
        gym_data = {
            "id": gym.id,
            "name": gym.name,
            "type": gym.type,
            "description": gym.description,
            "address_city": gym.address_city,
            "address_street": gym.address_street,
        }
        return JsonResponse(gym_data, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class GymUpdateView(View):
    def put(self, request, pk):
        data = json.loads(request.body)
        gym = get_object_or_404(Gym, pk=pk)
        gym.name = data.get("name", gym.name)
        gym.type = data.get("type", gym.type)
        gym.description = data.get("description", gym.description)
        gym.address_city = data.get("address_city", gym.address_city)
        gym.address_street = data.get("address_street", gym.address_street)
        gym.save()
        gym_data = {
            "id": gym.id,
            "name": gym.name,
            "type": gym.type,
            "description": gym.description,
            "address_city": gym.address_city,
            "address_street": gym.address_street,
        }
        return JsonResponse(gym_data)


@method_decorator(csrf_exempt, name="dispatch")
class GymDeleteView(View):
    def delete(self, request, pk):
        gym = get_object_or_404(Gym, pk=pk)
        gym.delete()
        return JsonResponse({"message": "Gym deleted"}, status=204)
