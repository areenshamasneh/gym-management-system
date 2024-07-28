from gym_app.models import Admin, Gym
from django.shortcuts import get_object_or_404


class AdminRepository:

    def get_all_admins(gym_id):
        return Admin.objects.filter(gym_id=gym_id)

    def get_admin_by_id(gym_id, admin_id):
        return get_object_or_404(Admin, pk=admin_id, gym_id=gym_id)

    def create_admin(gym_id, data):
        gym = get_object_or_404(Gym, pk=gym_id)
        return Admin.objects.create(
            name=data["name"],
            phone_number=data.get("phone_number", ""),
            email=data["email"],
            gym_id=gym,
            address_city=data["address_city"],
            address_street=data["address_street"],
        )

    def update_admin(gym_id, admin_id, data):
        admin = get_object_or_404(Admin, pk=admin_id, gym_id=gym_id)
        admin.name = data.get("name", admin.name)
        admin.phone_number = data.get("phone_number", admin.phone_number)
        admin.email = data.get("email", admin.email)
        admin.address_city = data.get("address_city", admin.address_city)
        admin.address_street = data.get("address_street", admin.address_street)
        admin.save()
        return admin

    def delete_admin(gym_id, admin_id):
        admin = get_object_or_404(Admin, pk=admin_id, gym_id=gym_id)
        admin.delete()
