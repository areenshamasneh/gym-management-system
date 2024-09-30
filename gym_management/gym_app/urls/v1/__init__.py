from django.urls import path, include

urlpatterns = [
    path("", include("gym_app.urls.v1.gym_urls")),
    path("lookups/", include("gym_app.urls.v1.lookups")),
    path("", include("gym_app.urls.v1.users")),

]
