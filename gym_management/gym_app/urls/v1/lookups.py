from django.urls import path, include
from rest_framework.routers import DefaultRouter  # type: ignore

from gym_app.views import HallTypeViewSet

router = DefaultRouter()
router.register(r"hall_types", HallTypeViewSet, basename="hall_type")

urlpatterns = [
    path("", include(router.urls)),
]
