from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from ..models import Admin, Gym


class AdminListView(View):
    def get(self, request):
        admins = Admin.objects.all()
        data = [model_to_dict(admin) for admin in admins]
        return JsonResponse(data, safe=False)


class AdminDetailView(View):
    def get(self, request, pk):
        admin = get_object_or_404(Admin, pk=pk)
        data = model_to_dict(admin)
        return JsonResponse(data)


@method_decorator(csrf_exempt, name="dispatch")
class AdminCreateView(CreateView):
    model = Admin
    fields = "__all__"
    success_url = reverse_lazy("admin-list")

    def post(self, request, *args, **kwargs):
        import json

        data = json.loads(request.body)
        form = self.get_form_class()(data)
        if form.is_valid():
            self.object = form.save()
            response_data = model_to_dict(self.object)
            return JsonResponse(response_data, status=201)
        return JsonResponse(form.errors, status=400)


@method_decorator(csrf_exempt, name="dispatch")
class AdminUpdateView(UpdateView):
    model = Admin
    fields = "__all__"
    success_url = reverse_lazy("admin-list")

    def put(self, request, pk, *args, **kwargs):
        import json

        data = json.loads(request.body)
        admin = get_object_or_404(Admin, pk=pk)

        for attr, value in data.items():
            if attr == "gym":
                gym_instance = get_object_or_404(Gym, pk=value)
                setattr(admin, attr, gym_instance)
            else:
                setattr(admin, attr, value)

        admin.save()
        response_data = model_to_dict(admin)
        return JsonResponse(response_data, status=200)


@method_decorator(csrf_exempt, name="dispatch")
class AdminDeleteView(DeleteView):
    model = Admin
    success_url = reverse_lazy("admin-list")

    def delete(self, request, pk, *args, **kwargs):
        admin = get_object_or_404(Admin, pk=pk)
        admin.delete()
        return JsonResponse({"status": "deleted"}, status=204)
