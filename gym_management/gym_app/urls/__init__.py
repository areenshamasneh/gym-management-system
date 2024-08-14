from django.urls import path, include

urlpatterns = [
    path("", include("gym_app.urls.health_urls")),
    path("v1/", include("gym_app.urls.v1")),
]
