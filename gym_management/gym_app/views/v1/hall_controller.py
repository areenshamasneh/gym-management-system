import json
from django.http import JsonResponse, Http404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from gym_app.components import HallComponent
from gym_app.forms import HallForm


@method_decorator(csrf_exempt, name="dispatch")
class HallController(View):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.component = HallComponent()

    def get(self, request, gym_id, pk=None):
        if pk:
            hall = self.component.fetch_hall_by_id(gym_id, pk)
            data = model_to_dict(hall)
            return JsonResponse(data)
        else:
            halls = self.component.fetch_all_halls(gym_id)
            data = [model_to_dict(hall) for hall in halls]
            return JsonResponse(data, safe=False)

    def post(self, request, gym_id):
        data = json.loads(request.body)
        form = HallForm(data)
        if form.is_valid():
            hall = self.component.add_hall(gym_id, form.cleaned_data)
            response_data = model_to_dict(hall)
            return JsonResponse(response_data, status=201)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    def put(self, request, gym_id, pk):
        data = json.loads(request.body)
        form = HallForm(data)
        if form.is_valid():
            hall = self.component.modify_hall(gym_id, pk, form.cleaned_data)
            response_data = model_to_dict(hall)
            return JsonResponse(response_data)
        else:
            return JsonResponse({"error": form.errors}, status=400)

    def delete(self, request, gym_id, pk):
        self.component.remove_hall(gym_id, pk)
        return JsonResponse({"message": "Hall deleted"}, status=204)
