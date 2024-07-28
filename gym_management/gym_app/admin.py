from django.contrib import admin
from gym_app.models import (
    Gym,
    Machine,
    Hall,
    HallMachine,
    Admin,
    Employee,
    Member,
    HallType,
)

admin.site.register(Gym)
admin.site.register(Machine)
admin.site.register(Hall)
admin.site.register(HallMachine)
admin.site.register(Admin)
admin.site.register(Employee)
admin.site.register(Member)
admin.site.register(HallType)
