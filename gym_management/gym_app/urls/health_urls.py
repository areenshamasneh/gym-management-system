from django.urls import path, include
from rest_framework.routers import DefaultRouter  # type: ignore
from gym_app.views import HealthCheckViewSet

router = DefaultRouter()
router.register(r"health", HealthCheckViewSet, basename="health_check")

urlpatterns = [
    path("", include(router.urls)),
]
