from gym_app.exceptions import ResourceNotFoundException
from gym_app.models import Admin, Gym


class AdminRepository:

    @staticmethod
    def get_all_admins(gym_id):
        return Admin.objects.filter(gym_id=gym_id)

    @staticmethod
    def get_admin_by_id(gym_id, admin_id):
        admin = Admin.objects.filter(pk=admin_id, gym_id=gym_id).first()
        if admin is None:
            raise ResourceNotFoundException(f"Admin with ID {admin_id} not found for gym_id {gym_id}")
        return admin

    @staticmethod
    def create_admin(gym_id, data):
        gym = Gym.objects.get(pk=gym_id)
        if not Gym.objects.filter(pk=gym_id).exists():
            raise ResourceNotFoundException(f"Gym with ID {gym_id} not found")
        return Admin.objects.create(
            name=data["name"],
            phone_number=data.get("phone_number", ""),
            email=data["email"],
            gym_id=gym,
            address_city=data["address_city"],
            address_street=data["address_street"],
        )

    @staticmethod
    def update_admin(gym_id, admin_id, data):
        if not Admin.objects.filter(pk=admin_id, gym_id=gym_id).exists():
            raise ResourceNotFoundException(f"Admin with ID {admin_id} not found for gym_id {gym_id}")
        Admin.objects.filter(pk=admin_id, gym_id=gym_id).update(
            name=data.get("name"),
            phone_number=data.get("phone_number", ""),
            email=data.get("email"),
            address_city=data.get("address_city"),
            address_street=data.get("address_street"),
        )
        return AdminRepository.get_admin_by_id(gym_id, admin_id)

    @staticmethod
    def delete_admin(gym_id, admin_id):
        if not Admin.objects.filter(pk=admin_id, gym_id=gym_id).exists():
            raise ResourceNotFoundException(f"Admin with ID {admin_id} not found for gym_id {gym_id}")
        Admin.objects.filter(pk=admin_id, gym_id=gym_id).delete()
