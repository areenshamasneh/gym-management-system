from django.urls import path
from gym_app.views import (
    AdminController,
)

urlpatterns = [
    path("admins/", AdminController.as_view(), name="admin-list"),
]
