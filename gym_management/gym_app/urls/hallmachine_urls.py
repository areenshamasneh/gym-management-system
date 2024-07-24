from django.urls import path
from gym_app.views.hallmachine_views import (
    HallMachineListView,
    HallMachineDetailView,
    HallMachineCreateView,
    HallMachineUpdateView,
    HallMachineDeleteView,
)

urlpatterns = [
    path("", HallMachineListView.as_view(), name="hallmachine-list"),
    path("<int:pk>/", HallMachineDetailView.as_view(), name="hallmachine-detail"),
    path("create/", HallMachineCreateView.as_view(), name="hallmachine-create"),
    path(
        "<int:pk>/update/", HallMachineUpdateView.as_view(), name="hallmachine-update"
    ),
    path(
        "<int:pk>/delete/", HallMachineDeleteView.as_view(), name="hallmachine-delete"
    ),
]
