import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from ..models import Hall, HallType, Gym


class HallListView(View):
    def get(self, request):
        halls = Hall.objects.all()
        data = [model_to_dict(hall) for hall in halls]
        return JsonResponse(data, safe=False)


class HallDetailView(View):
    def get(self, request, pk):
        hall = get_object_or_404(Hall, pk=pk)
        data = model_to_dict(hall)
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class HallCreateView(CreateView):
    model = Hall
    fields = "__all__"
    success_url = reverse_lazy("hall-list")

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)

            form = self.get_form_class()(data)
            if form.is_valid():
                hall = form.save()
                response_data = model_to_dict(hall)
                return JsonResponse(response_data, status=201)
            else:
                return JsonResponse(form.errors, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class HallUpdateView(UpdateView):
    model = Hall
    fields = "__all__"
    success_url = reverse_lazy("hall-list")

    def put(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            hall = get_object_or_404(Hall, pk=kwargs.get("pk"))

            for attr, value in data.items():
                if attr == "type":
                    hall_type = get_object_or_404(HallType, pk=value)
                    setattr(hall, attr, hall_type)
                elif attr == "gym":
                    gym_instance = get_object_or_404(Gym, pk=value)
                    setattr(hall, attr, gym_instance)
                else:
                    setattr(hall, attr, value)

            hall.save()
            response_data = model_to_dict(hall)
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class HallDeleteView(DeleteView):
    model = Hall
    success_url = reverse_lazy("hall-list")

    def delete(self, request, pk, *args, **kwargs):
        hall = get_object_or_404(Hall, pk=pk)
        hall.delete()
        return JsonResponse({"message": "Hall deleted"}, status=204)
