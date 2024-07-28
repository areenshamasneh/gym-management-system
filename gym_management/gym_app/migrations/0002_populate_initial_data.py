from django.db import migrations

def populate_initial_data(apps, schema_editor):
    Gym = apps.get_model('gym_app', 'Gym')
    Machine = apps.get_model('gym_app', 'Machine')
    HallType = apps.get_model('gym_app', 'HallType')
    Hall = apps.get_model('gym_app', 'Hall')
    Admin = apps.get_model('gym_app', 'Admin')
    Employee = apps.get_model('gym_app', 'Employee')
    Member = apps.get_model('gym_app', 'Member')
    HallMachine = apps.get_model('gym_app', 'HallMachine')

    # Insert default records for Gym
    Gym.objects.get_or_create(
        name='Default Gym 1',
        defaults={
            'type': 'Fitness',
            'description': 'A basic fitness gym.',
            'address_city': 'City 1',
            'address_street': 'Street 1'
        }
    )
    Gym.objects.get_or_create(
        name='Default Gym 2',
        defaults={
            'type': 'Wellness',
            'description': 'A gym focused on wellness.',
            'address_city': 'City 2',
            'address_street': 'Street 2'
        }
    )

    # Insert default records for Machine
    Machine.objects.get_or_create(
        serial_number='SN001',
        defaults={
            'type': 'running',
            'model': 'Model A',
            'brand': 'Brand X',
            'status': 'operational'
        }
    )
    Machine.objects.get_or_create(
        serial_number='SN002',
        defaults={
            'type': 'cycling',
            'model': 'Model B',
            'brand': 'Brand Y',
            'status': 'broken'
        }
    )

    # Insert default records for HallType
    HallType.objects.get_or_create(type='training', defaults={'type_description': 'Training hall'})
    HallType.objects.get_or_create(type='swimming', defaults={'type_description': 'Swimming hall'})

    # Insert default records for Hall
    Gym1 = Gym.objects.first()
    HallType1 = HallType.objects.first()
    Hall.objects.get_or_create(
        name='Main Hall',
        defaults={
            'users_capacity': 50,
            'hall_type_id': HallType1,
            'gym_id': Gym1
        }
    )
    Hall.objects.get_or_create(
        name='Secondary Hall',
        defaults={
            'users_capacity': 30,
            'hall_type_id': HallType1,
            'gym_id': Gym1
        }
    )

    # Insert default records for Admin
    Admin.objects.get_or_create(
        email='admin1@example.com',
        defaults={
            'name': 'Admin 1',
            'phone_number': '1234567890',
            'gym_id': Gym1,
            'address_city': 'City 1',
            'address_street': 'Street 1'
        }
    )
    Admin.objects.get_or_create(
        email='admin2@example.com',
        defaults={
            'name': 'Admin 2',
            'phone_number': '0987654321',
            'gym_id': Gym1,
            'address_city': 'City 2',
            'address_street': 'Street 2'
        }
    )

    # Insert default records for Employee
    Employee.objects.get_or_create(
        email='employee1@example.com',
        defaults={
            'name': 'Employee 1',
            'gym_id': Gym1,
            'address_city': 'City 1',
            'address_street': 'Street 1',
            'phone_number': '1111111111',
            'positions': 'trainer'
        }
    )
    Employee.objects.get_or_create(
        email='employee2@example.com',
        defaults={
            'name': 'Employee 2',
            'gym_id': Gym1,
            'address_city': 'City 2',
            'address_street': 'Street 2',
            'phone_number': '2222222222',
            'positions': 'cleaner'
        }
    )

    # Insert default records for Member
    Member.objects.get_or_create(
        name='Member 1',
        defaults={
            'gym_id': Gym1,
            'birth_date': '2000-01-01',
            'phone_number': '3333333333'
        }
    )
    Member.objects.get_or_create(
        name='Member 2',
        defaults={
            'gym_id': Gym1,
            'birth_date': '1990-05-15',
            'phone_number': '4444444444'
        }
    )

    # Insert default records for HallMachine
    Hall1 = Hall.objects.first()
    Machine1 = Machine.objects.first()
    HallMachine.objects.get_or_create(
        hall_id=Hall1,
        machine_id=Machine1,
        defaults={
            'name': f"{Hall1.name} - {Machine1.type}",
            'uid': f"{Machine1.type}_1"
        }
    )
    HallMachine.objects.get_or_create(
        hall_id=Hall1,
        machine_id=Machine1,
        defaults={
            'name': f"{Hall1.name} - {Machine1.type}",
            'uid': f"{Machine1.type}_2"
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('gym_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_initial_data),
    ]
