from django.urls import path
from gym_app.controllers import AdminController, EmployeeController, GymController

urlpatterns = [
    path("admins/", AdminController.as_view(), name="admin-list"),
    path("admins/<int:pk>/", AdminController.as_view(), name="admin-detail"),
    path("employees/", EmployeeController.as_view(), name="employees-list"),
    path("employees/<int:pk>/", EmployeeController.as_view(), name="employees-detail"),
    path("gyms/", GymController.as_view(), name="gym-list"),
    path("gyms/<int:pk>/", GymController.as_view(), name="gym-detail"),
]