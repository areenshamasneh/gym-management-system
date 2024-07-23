from django.urls import path
from gym_app.views.member_views import (
    MemberListView,
    MemberDetailView,
    MemberCreateView,
    MemberUpdateView,
    MemberDeleteView,
)

urlpatterns = [
    path("", MemberListView.as_view(), name="member-list"),
    path("<int:pk>/", MemberDetailView.as_view(), name="member-detail"),
    path("create/", MemberCreateView.as_view(), name="member-create"),
    path("<int:pk>/update/", MemberUpdateView.as_view(), name="member-update"),
    path("<int:pk>/delete/", MemberDeleteView.as_view(), name="member-delete"),
]
