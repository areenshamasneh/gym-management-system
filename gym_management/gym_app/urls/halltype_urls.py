from django.urls import path
from gym_app.views.halltype_views import (
    HallTypeListView,
    HallTypeDetailView,
    HallTypeCreateView,
    HallTypeUpdateView,
    HallTypeDeleteView,
)

urlpatterns = [
    path("", HallTypeListView.as_view(), name="halltype-list"),
    path("<int:pk>/", HallTypeDetailView.as_view(), name="halltype-detail"),
    path("create/", HallTypeCreateView.as_view(), name="halltype-create"),
    path("<int:pk>/update/", HallTypeUpdateView.as_view(), name="halltype-update"),
    path("<int:pk>/delete/", HallTypeDeleteView.as_view(), name="halltype-delete"),
]
