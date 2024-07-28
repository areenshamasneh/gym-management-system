from django.urls import path, include

urlpatterns = [
    path("", include("gym_app.urls.v2.gym_urls")),
]
