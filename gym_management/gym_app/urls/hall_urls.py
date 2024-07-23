from django.urls import path
from gym_app.views.hall_views import (
    HallListView,
    HallDetailView,
    HallCreateView,
    HallUpdateView,
    HallDeleteView,
)

urlpatterns = [
    path("", HallListView.as_view(), name="hall-list"),
    path("<int:pk>/", HallDetailView.as_view(), name="hall-detail"),
    path("create/", HallCreateView.as_view(), name="hall-create"),
    path("<int:pk>/update/", HallUpdateView.as_view(), name="hall-update"),
    path("<int:pk>/delete/", HallDeleteView.as_view(), name="hall-delete"),
]
