from django.urls import path
from gym_app.views import (
    HallTypeController,
)

urlpatterns = [
    path("hall_types/", HallTypeController.as_view(), name="hall_type-list"),
    path(
        "hall_types/<int:hall_type_id>/",
        HallTypeController.as_view(),
        name="hall_type-detail",
    ),
]
