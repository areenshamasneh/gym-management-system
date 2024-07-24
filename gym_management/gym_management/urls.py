from django.contrib import admin
from django.urls import path, include
from gym_app.views import health_check

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", health_check, name="health_check"),
    # Include app URLs
    path("api/gym/", include("gym_app.urls.gym_urls")),
    path("api/machine/", include("gym_app.urls.machine_urls")),
    path("api/hall/", include("gym_app.urls.hall_urls")),
    path("api/halltype/", include("gym_app.urls.halltype_urls")),
    path("api/admin/", include("gym_app.urls.admin_urls")),
    path("api/employee/", include("gym_app.urls.employee_urls")),
    path("api/member/", include("gym_app.urls.member_urls")),
    path("api/hallmachine/", include("gym_app.urls.hallmachine_urls")),
]
