def serialize_gym(gym):
    return {
        "id": gym.id,
        "name": gym.name,
        "type": gym.type,
        "description": gym.description,
        "address_city": gym.address_city,
        "address_street": gym.address_street
    }


def serialize_hall_type(hall_type):
    return {
        "id": hall_type.id,
        "name": hall_type.name,
        "code": hall_type.code,
        "type_description": hall_type.type_description
    }


def serialize_machine(machine):
    return {
        "id": machine.id,
        "serial_number": machine.serial_number,
        "type": machine.type,
        "model": machine.model,
        "brand": machine.brand,
        "status": machine.status,
        "maintenance_date": machine.maintenance_date.isoformat() if machine.maintenance_date else None
    }


def serialize_hall(hall):
    return {
        "id": hall.id,
        "name": hall.name,
        "users_capacity": hall.users_capacity,
        "hall_type": serialize_hall_type(hall.hall_type) if hall.hall_type else None,
        "gym": serialize_gym(hall.gym) if hall.gym else None
    }


def serialize_hall_machine(hall_machine):
    return {
        "id": hall_machine.id,
        "hall": serialize_hall(hall_machine.hall) if hall_machine.hall else None,
        "machine": serialize_machine(hall_machine.machine) if hall_machine.machine else None,
        "name": hall_machine.name,
        "uid": hall_machine.uid
    }


def serialize_admin(admin):
    return {
        "id": admin.id,
        "name": admin.name,
        "phone_number": admin.phone_number,
        "email": admin.email,
        "gym": serialize_gym(admin.gym) if admin.gym else None,
        "address_city": admin.address_city,
        "address_street": admin.address_street
    }


def serialize_employee(employee):
    return {
        "id": employee.id,
        "name": employee.name,
        "gym": serialize_gym(employee.gym) if employee.gym else None,
        "manager": serialize_employee(employee.manager) if employee.manager else None,
        "address_city": employee.address_city,
        "address_street": employee.address_street,
        "phone_number": employee.phone_number,
        "email": employee.email,
        "positions": employee.positions
    }


def serialize_member(member):
    return {
        "id": member.id,
        "name": member.name,
        "gym": serialize_gym(member.gym) if member.gym else None,
        "phone_number": member.phone_number,
        "birth_date": member.birth_date.isoformat() if member.birth_date else None
    }
