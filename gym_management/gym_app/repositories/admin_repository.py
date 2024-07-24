from gym_app.models import Admin, Gym
from django.shortcuts import get_object_or_404

class AdminRepository:
    @staticmethod
    def get_all_admins():
        return Admin.objects.all()

    @staticmethod
    def get_admin_by_id(admin_id):
        return get_object_or_404(Admin, pk=admin_id)

    @staticmethod
    def create_admin(data):
        gym = get_object_or_404(Gym, pk=data["gym"])
        return Admin.objects.create(
            name=data["name"],
            phone_number=data.get("phone_number", ""),
            email=data["email"],
            gym=gym,
            address_city=data["address_city"],
            address_street=data["address_street"],
        )

    @staticmethod
    def update_admin(admin_id, data):
        admin = get_object_or_404(Admin, pk=admin_id)
        gym = get_object_or_404(Gym, pk=data.get("gym", admin.gym.pk))
        admin.name = data.get("name", admin.name)
        admin.phone_number = data.get("phone_number", admin.phone_number)
        admin.email = data.get("email", admin.email)
        admin.gym = gym
        admin.address_city = data.get("address_city", admin.address_city)
        admin.address_street = data.get("address_street", admin.address_street)
        admin.save()
        return admin

    @staticmethod
    def delete_admin(admin_id):
        admin = get_object_or_404(Admin, pk=admin_id)
        admin.delete()
