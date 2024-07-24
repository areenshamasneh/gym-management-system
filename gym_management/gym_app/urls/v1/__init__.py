from django.urls import path, include

urlpatterns = [
    path("", include("gym_app.urls.v1.gym_urls")),
]
