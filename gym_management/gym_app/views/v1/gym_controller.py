from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json
from gym_app.components import GymComponent
from gym_app.logging import CustomLogger
from gym_app.models.system_models import Gym
from gym_app.repositories.gym_repository import GymRepository
from gym_app.forms import GymForm


@method_decorator(csrf_exempt, name="dispatch")
class GymController(View):
    def __init__(self, *args, **kwargs):
        self.logger = CustomLogger()
        self.gym_repository = GymRepository()
        self.gym_component = GymComponent(self.gym_repository, self.logger)
        super().__init__(*args, **kwargs)

    def get(self, request, pk=None):
        if pk is None:
            # Handle GET request for list of gyms
            try:
                gyms = self.gym_component.fetch_all_gyms()
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
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)
        else:
            # Handle GET request for a single gym by pk
            try:
                gym = self.gym_component.fetch_gym_by_id(pk)
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
            except Exception as e:
                return JsonResponse({"error": str(e)}, status=500)

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = GymForm(data)
            if form.is_valid():
                gym = self.gym_component.add_gym(form.cleaned_data)
                gym_data = {
                    "id": gym.id,
                    "name": gym.name,
                    "type": gym.type,
                    "description": gym.description,
                    "address_city": gym.address_city,
                    "address_street": gym.address_street,
                }
                return JsonResponse(gym_data, status=201)
            else:
                return JsonResponse({"errors": form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            return JsonResponse(
                {"error": "Creation failed", "details": str(e)}, status=500
            )

    def put(self, request, pk):
        try:
            data = json.loads(request.body)
            form = GymForm(data)
            if form.is_valid():
                gym = self.gym_component.modify_gym(pk, form.cleaned_data)
                gym_data = {
                    "id": gym.id,
                    "name": gym.name,
                    "type": gym.type,
                    "description": gym.description,
                    "address_city": gym.address_city,
                    "address_street": gym.address_street,
                }
                return JsonResponse(gym_data)
            else:
                return JsonResponse({"errors": form.errors}, status=400)
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
            self.gym_component.remove_gym(pk)
            return JsonResponse({"message": "Gym deleted"}, status=204)
        except Gym.DoesNotExist:
            return JsonResponse({"error": "Gym not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
