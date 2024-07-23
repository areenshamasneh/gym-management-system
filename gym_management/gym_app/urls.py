from django.urls import path
from .views.gym_views import GymListView, GymDetailView, GymCreateView, GymUpdateView, GymDeleteView
from .views.machine_views import MachineListView, MachineDetailView, MachineCreateView, MachineUpdateView, MachineDeleteView
from .views.hall_views import HallListView, HallDetailView, HallCreateView, HallUpdateView, HallDeleteView
from .views.halltype_views import HallTypeListView, HallTypeDetailView, HallTypeCreateView, HallTypeUpdateView, HallTypeDeleteView
from .views.admin_views import AdminListView, AdminDetailView, AdminCreateView, AdminUpdateView, AdminDeleteView
from .views.employee_views import EmployeeListView, EmployeeDetailView, EmployeeCreateView, EmployeeUpdateView, EmployeeDeleteView
from .views.member_views import MemberListView, MemberDetailView, MemberCreateView, MemberUpdateView, MemberDeleteView
from .views.hallmachine_views import HallMachineListView, HallMachineDetailView, HallMachineCreateView, HallMachineUpdateView, HallMachineDeleteView
from .views import health_check

urlpatterns = [
    path('health/', health_check, name='health_check'),

    # Gym URLs
    path('gym/', GymListView.as_view(), name='gym-list'),
    path('gym/<int:pk>/', GymDetailView.as_view(), name='gym-detail'),
    path('gym/create/', GymCreateView.as_view(), name='gym-create'),
    path('gym/<int:pk>/update/', GymUpdateView.as_view(), name='gym-update'),
    path('gym/<int:pk>/delete/', GymDeleteView.as_view(), name='gym-delete'),

    # Machine URLs
    path('machine/', MachineListView.as_view(), name='machine-list'),
    path('machine/<int:pk>/', MachineDetailView.as_view(), name='machine-detail'),
    path('machine/create/', MachineCreateView.as_view(), name='machine-create'),
    path('machine/<int:pk>/update/', MachineUpdateView.as_view(), name='machine-update'),
    path('machine/<int:pk>/delete/', MachineDeleteView.as_view(), name='machine-delete'),

    # Hall URLs
    path('hall/', HallListView.as_view(), name='hall-list'),
    path('hall/<int:pk>/', HallDetailView.as_view(), name='hall-detail'),
    path('hall/create/', HallCreateView.as_view(), name='hall-create'),
    path('hall/<int:pk>/update/', HallUpdateView.as_view(), name='hall-update'),
    path('hall/<int:pk>/delete/', HallDeleteView.as_view(), name='hall-delete'),

    # HallType URLs
    path('halltype/', HallTypeListView.as_view(), name='halltype-list'),
    path('halltype/<int:pk>/', HallTypeDetailView.as_view(), name='halltype-detail'),
    path('halltype/create/', HallTypeCreateView.as_view(), name='halltype-create'),
    path('halltype/<int:pk>/update/', HallTypeUpdateView.as_view(), name='halltype-update'),
    path('halltype/<int:pk>/delete/', HallTypeDeleteView.as_view(), name='halltype-delete'),

    # Admin URLs
    path('admin/', AdminListView.as_view(), name='admin-list'),
    path('admin/<int:pk>/', AdminDetailView.as_view(), name='admin-detail'),
    path('admin/create/', AdminCreateView.as_view(), name='admin-create'),
    path('admin/<int:pk>/update/', AdminUpdateView.as_view(), name='admin-update'),
    path('admin/<int:pk>/delete/', AdminDeleteView.as_view(), name='admin-delete'),

    # Employee URLs
    path('employee/', EmployeeListView.as_view(), name='employee-list'),
    path('employee/<int:pk>/', EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/create/', EmployeeCreateView.as_view(), name='employee-create'),
    path('employee/<int:pk>/update/', EmployeeUpdateView.as_view(), name='employee-update'),
    path('employee/<int:pk>/delete/', EmployeeDeleteView.as_view(), name='employee-delete'),

    # Member URLs
    path('member/', MemberListView.as_view(), name='member-list'),
    path('member/<int:pk>/', MemberDetailView.as_view(), name='member-detail'),
    path('member/create/', MemberCreateView.as_view(), name='member-create'),
    path('member/<int:pk>/update/', MemberUpdateView.as_view(), name='member-update'),
    path('member/<int:pk>/delete/', MemberDeleteView.as_view(), name='member-delete'),

    # HallMachine URLs
    path('hallmachine/', HallMachineListView.as_view(), name='hallmachine-list'),
    path('hallmachine/<int:pk>/', HallMachineDetailView.as_view(), name='hallmachine-detail'),
    path('hallmachine/create/', HallMachineCreateView.as_view(), name='hallmachine-create'),
    path('hallmachine/<int:pk>/update/', HallMachineUpdateView.as_view(), name='hallmachine-update'),
    path('hallmachine/<int:pk>/delete/', HallMachineDeleteView.as_view(), name='hallmachine-delete'),
]
