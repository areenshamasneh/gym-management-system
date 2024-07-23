from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.forms.models import model_to_dict
from ..models import Machine


class MachineListView(View):
    def get(self, request):
        machines = Machine.objects.all()
        data = [model_to_dict(machine) for machine in machines]
        return JsonResponse(data, safe=False)


class MachineDetailView(View):
    def get(self, request, pk):
        machine = get_object_or_404(Machine, pk=pk)
        data = model_to_dict(machine)
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class MachineCreateView(View):
    def post(self, request, *args, **kwargs):
        import json

        data = json.loads(request.body)
        machine = Machine.objects.create(**data)
        response_data = model_to_dict(machine)
        return JsonResponse(response_data, status=201)


@method_decorator(csrf_exempt, name="dispatch")
class MachineUpdateView(View):
    def put(self, request, pk, *args, **kwargs):
        import json

        data = json.loads(request.body)
        machine = get_object_or_404(Machine, pk=pk)
        for attr, value in data.items():
            setattr(machine, attr, value)
        machine.save()
        response_data = model_to_dict(machine)
        return JsonResponse(response_data, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class MachineDeleteView(View):
    def delete(self, request, pk, *args, **kwargs):
        machine = get_object_or_404(Machine, pk=pk)
        machine.delete()
        return JsonResponse({"message": "Machine deleted"}, status=204)
