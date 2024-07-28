from django.urls import path
from gym_app.views import (
    AdminController,
    EmployeeController,
    GymController,
    HallController,
    MemberController,
    HallTypeController,
    HallMachineController,
)

urlpatterns = [
    path("gyms/", GymController.as_view(), name="gym-list"),
    path("gyms/<int:pk>/", GymController.as_view(), name="gym-detail"),
    path("gyms/<int:gym_id>/admins/", AdminController.as_view(), name="admin-list"),
    path(
        "gyms/<int:gym_id>/admins/<int:pk>/",
        AdminController.as_view(),
        name="admin-detail",
    ),
    path(
        "gyms/<int:gym_id>/employees/",
        EmployeeController.as_view(),
        name="employees-list",
    ),
    path(
        "gyms/<int:gym_id>/employees/<int:pk>/",
        EmployeeController.as_view(),
        name="employees-detail",
    ),
    path("gyms/<int:gym_id>/halls/", HallController.as_view(), name="hall-list"),
    path(
        "gyms/<int:gym_id>/halls/<int:pk>/",
        HallController.as_view(),
        name="hall-detail",
    ),
    path("gyms/<int:gym_id>/members/", MemberController.as_view(), name="member-list"),
    path(
        "gyms/<int:gym_id>/members/<int:pk>/",
        MemberController.as_view(),
        name="member-detail",
    ),
    path("hall_types/", HallTypeController.as_view(), name="hall_type-list"),
    path(
        "hall_types/<int:hall_type_id>/",
        HallTypeController.as_view(),
        name="hall_type-detail",
    ),
    path(
        "gyms/<int:gym_id>/halls/<int:hall_id>/machines/",
        HallMachineController.as_view(),
        name="hall-machine-list",
    ),
    path(
        "gyms/<int:gym_id>/halls/<int:hall_id>/machines/<str:machine_id>/",
        HallMachineController.as_view(),
        name="hall-machine-detail",
    ),
]
