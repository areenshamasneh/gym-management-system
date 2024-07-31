from django.urls import path, include
from rest_framework.routers import DefaultRouter  # type: ignore
from gym_app.views import GymView, AdminView

router = DefaultRouter()
router.register(r"gyms", GymView, basename="gym")
router.register(r"gyms/(?P<gym_id>\d+)/admins", AdminView, basename="admin")

urlpatterns = [
    path("", include(router.urls)),
]
