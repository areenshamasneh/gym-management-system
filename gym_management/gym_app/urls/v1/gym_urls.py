from django.urls import path
from gym_app.views import (
    AdminController,
    EmployeeController,
    GymController,
    HallController,
    MemberController,
    MachineController,
    HallTypeController,
    HallMachineController,
)

urlpatterns = [
    path("admins/", AdminController.as_view(), name="admin-list"),
    path("admins/<int:pk>/", AdminController.as_view(), name="admin-detail"),
    path("employees/", EmployeeController.as_view(), name="employees-list"),
    path("employees/<int:pk>/", EmployeeController.as_view(), name="employees-detail"),
    path("gyms/", GymController.as_view(), name="gym-list"),
    path("gyms/<int:pk>/", GymController.as_view(), name="gym-detail"),
    path("halls/", HallController.as_view(), name="hall-list"),
    path("halls/<int:pk>/", HallController.as_view(), name="hall-detail"),
    path("members/", MemberController.as_view(), name="member-list"),
    path("members/<int:pk>/", MemberController.as_view(), name="member-detail"),
    path("machines/", MachineController.as_view(), name="machine-list"),
    path("machines/<int:pk>/", MachineController.as_view(), name="machine-detail"),
    path("hall_types/", HallTypeController.as_view(), name="hall_type-list"),
    path(
        "hall_types/<int:hall_type_id>/",
        HallTypeController.as_view(),
        name="hall_type-detail",
    ),
    path(
        "halls/<int:hall_id>/machines/",
        HallMachineController.as_view(),
        name="hall-machine-list",
    ),
    path(
        "halls/<int:hall_id>/machines/<int:machine_id>/",
        HallMachineController.as_view(),
        name="hall-machine-detail",
    ),
    path(
        "machines/<int:machine_id>/halls/",
        HallMachineController.as_view(),
        name="machine-hall-list",
    ),
    path(
        "machines/<int:machine_id>/halls/<int:hall_id>/",
        HallMachineController.as_view(),
        name="machine-hall-detail",
    ),
]
