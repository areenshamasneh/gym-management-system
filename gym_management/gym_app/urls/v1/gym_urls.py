from django.urls import include, path
from rest_framework.routers import DefaultRouter  # type: ignore
from gym_app.views import (
    GymViewSet,
    AdminViewSet,
    EmployeeViewSet,
    HallViewSet,
    HallMachineViewSet,
    MachineViewSet,
    MemberViewSet,
)

router = DefaultRouter()
router.register(r"gyms", GymViewSet, basename="gym")
router.register(r"gyms/(?P<gym_id>\d+)/admins", AdminViewSet, basename="admin")
router.register(r"gyms/(?P<gym_id>\d+)/employees", EmployeeViewSet, basename="employee")
router.register(
    r"gyms/(?P<gym_id>\d+)/halls/(?P<hall_id>\d+)/machines",
    MachineViewSet,
    basename="machines-hall",
)
router.register(
    r"gyms/(?P<gym_id>\d+)/halls/machines", HallMachineViewSet, basename="hall-machine"
)
router.register(r"gyms/(?P<gym_id>\d+)/halls", HallViewSet, basename="hall")
router.register(r"gyms/(?P<gym_id>\d+)/members", MemberViewSet, basename="member")

urlpatterns = [
    path("", include(router.urls)),
]
