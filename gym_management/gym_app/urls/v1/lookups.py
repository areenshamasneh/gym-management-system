from django.urls import path, include
from rest_framework.routers import DefaultRouter  # type: ignore

from gym_app.controllers import HallTypeController

router = DefaultRouter()
router.register(r"hall_types", HallTypeController, basename="hall_type")

urlpatterns = [
    path("", include(router.urls)),
]
