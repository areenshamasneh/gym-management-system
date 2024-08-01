from gym_app.models.system_models import Gym
from rest_framework import viewsets  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework import status  # type: ignore
from django.shortcuts import get_object_or_404
from gym_app.models import Admin
from gym_app.serializers import AdminSerializer
from django.db.models import Q


class AdminViewSet(viewsets.ViewSet):
    def list(self, request, gym_id=None):
        try:
            gym = Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            return Response(
                {"detail": "Gym with ID {} does not exist".format(gym_id)},
                status=status.HTTP_404_NOT_FOUND,
            )

        name = request.GET.get("name", "")
        email = request.GET.get("email", "")
        phone_number = request.GET.get("phone_number", "")
        address_city = request.GET.get("address_city", "")
        address_street = request.GET.get("address_street", "")

        filter_criteria = Q(gym_id=gym_id)
        if name:
            filter_criteria &= Q(name__icontains=name)
        if email:
            filter_criteria &= Q(email__icontains=email)
        if phone_number:
            filter_criteria &= Q(phone_number__icontains=phone_number)
        if address_city:
            filter_criteria &= Q(address_city__icontains=address_city)
        if address_street:
            filter_criteria &= Q(address_street__icontains=address_street)

        admins = Admin.objects.filter(filter_criteria)
        serializer = AdminSerializer(admins, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, gym_id=None):
        if gym_id is None:
            return Response({"detail": "Gym ID is required"}, status=400)
        try:
            gym = Gym.objects.get(id=gym_id)
        except Gym.DoesNotExist:
            return Response(
                {"detail": "Gym with ID {} does not exist".format(gym_id)},
                status=status.HTTP_404_NOT_FOUND,
            )

        admin = get_object_or_404(Admin, pk=pk, gym_id=gym_id)
        serializer = AdminSerializer(admin)
        return Response(serializer.data)

    def create(self, request, gym_id=None):
        if gym_id is None:
            return Response({"detail": "Gym ID is required"}, status=400)

        gym = get_object_or_404(Gym, pk=gym_id)
        data = request.data.copy()
        data["gym_id"] = gym.id

        serializer = AdminSerializer(data=data)
        if serializer.is_valid():
            serializer.save(gym_id=gym.id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None, gym_id=None):
        if gym_id is None:
            return Response({"detail": "Gym ID is required"}, status=400)

        admin = get_object_or_404(Admin, pk=pk, gym_id=gym_id)
        data = request.data.copy()
        data["gym_id"] = gym_id
        serializer = AdminSerializer(admin, data=data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None, gym_id=None):
        if gym_id is None:
            return Response({"detail": "Gym ID is required"}, status=400)

        admin = get_object_or_404(Admin, pk=pk, gym_id=gym_id)
        data = request.data.copy()
        data["gym_id"] = gym_id
        serializer = AdminSerializer(admin, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None, gym_id=None):
        if gym_id is None:
            return Response({"detail": "Gym ID is required"}, status=400)

        admin = get_object_or_404(Admin, pk=pk, gym_id=gym_id)
        admin.delete()
        return Response(status=204)
