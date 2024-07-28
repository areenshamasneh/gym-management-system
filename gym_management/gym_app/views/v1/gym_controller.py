from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
from gym_app.components.gym_component import GymComponent
from gym_app.models import Gym


@method_decorator(csrf_exempt, name="dispatch")
class GymController(View):
    def get(self, request, pk=None):
        if pk is None:
            # Handle GET request for list of gyms
            gyms = GymComponent.fetch_all_gyms()
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
        else:
            # Handle GET request for a single gym by pk
            try:
                gym = GymComponent.fetch_gym_by_id(pk)
                gym_data = {
                    "id": gym.id,
                    "name": gym.name,
                    "type": gym.type,
                    "description": gym.description,
                    "address_city": gym.address_city,
                    "address_street": gym.address_street,
                }
                return JsonResponse(gym_data)
            except Gym.DoesNotExist:
                return JsonResponse({"error": "Gym not found"}, status=404)

    def post(self, request):
        try:
            data = json.loads(request.body)
            gym = GymComponent.add_gym(data)
            gym_data = {
                "id": gym.id,
                "name": gym.name,
                "type": gym.type,
                "description": gym.description,
                "address_city": gym.address_city,
                "address_street": gym.address_street,
            }
            return JsonResponse(gym_data, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "Creation failed", "details": str(e)}, status=500
            )

    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            gym = GymComponent.modify_gym(pk, data)
            gym_data = {
                "id": gym.id,
                "name": gym.name,
                "type": gym.type,
                "description": gym.description,
                "address_city": gym.address_city,
                "address_street": gym.address_street,
            }
            return JsonResponse(gym_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Gym.DoesNotExist:
            return JsonResponse({"error": "Gym not found"}, status=404)
        except Exception as e:
            return JsonResponse(
                {"error": "Update failed", "details": str(e)}, status=500
            )

    def delete(self, request, pk):
        try:
            GymComponent.remove_gym(pk)
            return JsonResponse({"message": "Gym deleted"}, status=204)
        except Gym.DoesNotExist:
            return JsonResponse({"error": "Gym not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
