from django.urls import path
from gym_app.views.machine_views import (
    MachineListView,
    MachineDetailView,
    MachineCreateView,
    MachineUpdateView,
    MachineDeleteView,
)

urlpatterns = [
    path("", MachineListView.as_view(), name="machine-list"),
    path("<int:pk>/", MachineDetailView.as_view(), name="machine-detail"),
    path("create/", MachineCreateView.as_view(), name="machine-create"),
    path("<int:pk>/update/", MachineUpdateView.as_view(), name="machine-update"),
    path("<int:pk>/delete/", MachineDeleteView.as_view(), name="machine-delete"),
]
