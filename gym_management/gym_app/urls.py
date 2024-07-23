from django.urls import path
from .views.controller_health_check import health_check

urlpatterns = [
    path('health/', health_check, name='health_check'),
]
