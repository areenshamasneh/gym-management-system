from gym_app.models import Admin, Gym


class AdminRepository:
    @staticmethod
    def get_all_admins(gym_id):
        return Admin.objects.filter(gym_id=gym_id).select_related('gym')

    @staticmethod
    def get_admin_by_id(gym_id, admin_id):
        return Admin.objects.filter(pk=admin_id, gym_id=gym_id).select_related('gym').first()

    @staticmethod
    def create_admin(gym_id, data):
        gym = Gym.objects.get(pk=gym_id)
        return Admin.objects.create(
            name=data["name"],
            phone_number=data.get("phone_number", ""),
            email=data["email"],
            gym=gym,
            address_city=data["address_city"],
            address_street=data["address_street"],
        )

    @staticmethod
    def update_admin(gym_id, admin_id, data):
        admin = Admin.objects.filter(pk=admin_id, gym__id=gym_id).first()

        if 'name' in data:
            admin.name = data['name']
        if 'phone_number' in data:
            admin.phone_number = data['phone_number']
        if 'email' in data:
            admin.email = data['email']
        if 'address_city' in data:
            admin.address_city = data['address_city']
        if 'address_street' in data:
            admin.address_street = data['address_street']

        admin.save()
        return admin

    @staticmethod
    def delete_admin(gym_id, admin_id):
        Admin.objects.filter(pk=admin_id, gym_id=gym_id).delete()
