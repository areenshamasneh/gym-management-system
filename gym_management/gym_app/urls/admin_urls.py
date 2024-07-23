from django.urls import path
from gym_app.views.admin_views import (
    AdminListView,
    AdminDetailView,
    AdminCreateView,
    AdminUpdateView,
    AdminDeleteView,
)

urlpatterns = [
    path("", AdminListView.as_view(), name="admin-list"),
    path("<int:pk>/", AdminDetailView.as_view(), name="admin-detail"),
    path("create/", AdminCreateView.as_view(), name="admin-create"),
    path("<int:pk>/update/", AdminUpdateView.as_view(), name="admin-update"),
    path("<int:pk>/delete/", AdminDeleteView.as_view(), name="admin-delete"),
]
