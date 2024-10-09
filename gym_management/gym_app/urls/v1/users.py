from django.urls import path, include
from rest_framework.routers import DefaultRouter  # type: ignore

from gym_app.controllers.v1.user_controller import UserController

router = DefaultRouter()
router.register(r"users", UserController, basename="users")

urlpatterns = [
    path("", include(router.urls)),
]
