from django.urls import path
from gym_app.views.gym_views import (
    GymListView,
    GymDetailView,
    GymCreateView,
    GymUpdateView,
    GymDeleteView,
)

urlpatterns = [
    path("", GymListView.as_view(), name="gym-list"),
    path("<int:pk>/", GymDetailView.as_view(), name="gym-detail"),
    path("create/", GymCreateView.as_view(), name="gym-create"),
    path("<int:pk>/update/", GymUpdateView.as_view(), name="gym-update"),
    path("<int:pk>/delete/", GymDeleteView.as_view(), name="gym-delete"),
]
