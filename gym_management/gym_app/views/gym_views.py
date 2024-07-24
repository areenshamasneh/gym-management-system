from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
from gym_app.components.gym_component import (
    fetch_all_gyms,
    fetch_gym_by_id,
    add_gym,
    modify_gym,
    remove_gym,
)


@method_decorator(csrf_exempt, name="dispatch")
class GymListView(View):
    def get(self, request):
        gyms = fetch_all_gyms()
        gym_list = [
            {
                "id": gym.id,
                "name": gym.name,
                "type": gym.type,
                "description": gym.description,
                "address_city": gym.address_city,
                "address_street": gym.address_street,
            }
            for gym in gyms
        ]
        return JsonResponse(gym_list, safe=False)


@method_decorator(csrf_exempt, name="dispatch")
class GymDetailView(View):
    def get(self, request, pk):
        gym = fetch_gym_by_id(pk)
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
        gym = add_gym(data)
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
        gym = modify_gym(pk, data)
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
        remove_gym(pk)
        return JsonResponse({"message": "Gym deleted"}, status=204)
