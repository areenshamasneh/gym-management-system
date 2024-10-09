from django.urls import include, path
from rest_framework_nested import routers

from gym_app.controllers import (
    GymController,
    AdminController,
    EmployeeController,
    HallController,
    MachineController,
    MemberController,
    GymMachineController,
)

router = routers.SimpleRouter()
router.register(r'gyms', GymController, basename='gym')

gyms_router = routers.NestedSimpleRouter(router, r'gyms', lookup='gym')
gyms_router.register(r'admins', AdminController, basename='gym-admins')
gyms_router.register(r'employees', EmployeeController, basename='gym-employees')
gyms_router.register(r'halls', HallController, basename='gym-halls')
gyms_router.register(r'members', MemberController, basename='gym-members')
gyms_router.register(r'machines', GymMachineController, basename='gym-machines')

halls_router = routers.NestedSimpleRouter(gyms_router, r'halls', lookup='hall')
halls_router.register(r'machines', MachineController, basename='hall-machines')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(gyms_router.urls)),
    path('', include(halls_router.urls)),
]
