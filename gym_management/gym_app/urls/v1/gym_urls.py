from django.urls import include, path
from rest_framework_nested import routers

from gym_app.views import (
    GymViewSet,
    AdminViewSet,
    EmployeeViewSet,
    HallViewSet,
    MachineViewSet,
    HallMachineViewSet,
    MemberViewSet,
)

router = routers.SimpleRouter()
router.register(r'gyms', GymViewSet, basename='gym')

gyms_router = routers.NestedSimpleRouter(router, r'gyms', lookup='gym')
gyms_router.register(r'admins', AdminViewSet, basename='gym-admins')
gyms_router.register(r'employees', EmployeeViewSet, basename='gym-employees')
gyms_router.register(r'halls', HallViewSet, basename='gym-halls')
gyms_router.register(r'members', MemberViewSet, basename='gym-members')

halls_router = routers.NestedSimpleRouter(gyms_router, r'halls', lookup='hall')
halls_router.register(r'machines', MachineViewSet, basename='hall-machines')

hall_machines_router = routers.NestedSimpleRouter(gyms_router, r'halls', lookup='hall')
hall_machines_router.register(r'machines', HallMachineViewSet, basename='hall-machine')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(gyms_router.urls)),
    path('', include(halls_router.urls)),
    path('', include(hall_machines_router.urls)),
]
