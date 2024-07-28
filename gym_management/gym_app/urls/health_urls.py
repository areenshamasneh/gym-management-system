from django.urls import path
from gym_app.controllers import health_check

urlpatterns = [
    path("", health_check, name="health_check"),
]
