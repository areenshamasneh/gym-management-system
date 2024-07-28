from gym_app.urls.health_urls import health_check
from django.urls import path, include

urlpatterns = [
    path("health/", include("gym_app.urls.health_urls")),
    path("v1/", include("gym_app.urls.v1")),
    path("v2/", include("gym_app.urls.v2")),

]
