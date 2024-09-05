from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from common.db.database import Session
from gym_app.exceptions import ResourceNotFoundException
from gym_app.models.models_sqlalchemy import Hall, Machine, HallMachine, Gym


class MachineRepository:

    @staticmethod
    def get_all_machines_in_hall(gym_id, hall_id):
        gym = Session.get(Gym, gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        query = (
            select(Machine)
            .join(HallMachine)
            .join(Hall)
            .filter(HallMachine.hall_id == hall_id, Hall.gym_id == gym_id)
        )
        result = Session.execute(query)
        machines = result.scalars().all()
        if not machines:
            raise ResourceNotFoundException(f"No machines found in hall {hall_id} for gym_id {gym_id}.")
        return machines

    @staticmethod
    def get_machine_by_id_in_hall(gym_id, hall_id, machine_id):
        gym = Session.get(Gym, gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        query = (
            select(HallMachine)
            .options(joinedload(HallMachine.machine), joinedload(HallMachine.hall))
            .join(Hall)
            .join(Machine)
            .filter(Hall.id == hall_id, Hall.gym_id == gym_id, Machine.id == machine_id)
        )
        result = Session.execute(query)
        hall_machine = result.scalar_one_or_none()
        if not hall_machine:
            raise ResourceNotFoundException(
                f"Machine with ID {machine_id} not found in hall {hall_id} for gym_id {gym_id}.")
        return hall_machine

    @staticmethod
    def create_machine(gym_id, data):
        gym = Session.get(Gym, gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        machine = Machine(
            serial_number=data["serial_number"],
            type=data.get("type"),
            model=data.get("model"),
            brand=data.get("brand"),
            status=data.get("status"),
            maintenance_date=data.get("maintenance_date"),
        )
        Session.add(machine)
        return machine

    @staticmethod
    def create_hall_machine(gym_id, hall_id, machine_id):
        gym = Session.get(Gym, gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        hall = Session.execute(select(Hall).filter_by(id=hall_id)).scalar_one_or_none()
        if not hall:
            raise ResourceNotFoundException("Hall not found")

        machine = Session.execute(select(Machine).filter_by(id=machine_id)).scalar_one_or_none()
        if not machine:
            raise ResourceNotFoundException("Machine not found")

        if machine.type is None:
            raise ValueError("Machine type is missing")

        type_count_query = (
            Session.execute(
                select(HallMachine)
                .join(Machine)
                .filter(HallMachine.hall_id == hall_id, Machine.type == machine.type)
            )
        )
        type_count = len(type_count_query.scalars().all()) + 1

        hall_machine_name = f"{hall.name} - {machine.type.capitalize()}"
        hall_machine_uid = f"{machine.type}_{type_count}"

        hall_machine = HallMachine(
            hall_id=hall_id,
            machine_id=machine_id,
            name=hall_machine_name,
            uid=hall_machine_uid
        )

        Session.add(hall_machine)
        return hall_machine

    @staticmethod
    def update_machine(gym_id, hall_id, machine_id, data):
        gym = Session.get(Gym, gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")

        hall_machine_query = (
            select(HallMachine)
            .options(joinedload(HallMachine.machine))
            .join(Hall)
            .filter(Hall.gym_id == gym_id, Hall.id == hall_id, HallMachine.machine_id == machine_id)
        )
        hall_machine = Session.execute(hall_machine_query).scalar_one_or_none()

        if not hall_machine:
            raise ResourceNotFoundException(
                f"Machine with ID {machine_id} not found in hall {hall_id} for gym_id {gym_id}."
            )

        machine = hall_machine.machine

        machine.type = data.get("type", machine.type)
        machine.serial_number = data.get("serial_number", machine.serial_number)
        machine.model = data.get("model", machine.model)
        machine.brand = data.get("brand", machine.brand)
        machine.status = data.get("status", machine.status)
        machine.maintenance_date = data.get("maintenance_date", machine.maintenance_date)

        Session.add(machine)

        return hall_machine

    @staticmethod
    def update_hall_machine(hall_machine, machine):
        hall = Session.execute(select(Hall).filter_by(id=hall_machine.hall_id)).scalar_one_or_none()
        if not hall:
            raise ResourceNotFoundException("Hall not found")

        type_count_query = (
            select(HallMachine)
            .join(Machine)
            .filter(HallMachine.hall_id == hall_machine.hall_id, Machine.type == machine.type)
        )
        type_count = len(Session.execute(type_count_query).scalars().all()) + 1

        hall_machine_name = f"{hall.name} - {machine.type.capitalize()}"
        hall_machine_uid = f"{machine.type}_{type_count}"

        update_query = (
            update(HallMachine)
            .where(HallMachine.id == hall_machine.id)
            .values(name=hall_machine_name, uid=hall_machine_uid)
        )
        Session.execute(update_query)
        return hall_machine

    @staticmethod
    def delete_hall_machine(gym_id, hall_id, machine_id):
        hall_machine = MachineRepository.get_machine_by_id_in_hall(gym_id, hall_id, machine_id)
        Session.delete(hall_machine)
        return True

    @staticmethod
    def get_all_machines_in_gym(gym_id):
        gym = Session.get(Gym, gym_id)
        if not gym:
            raise ResourceNotFoundException("Gym not found")
        query = (
            select(HallMachine)
            .join(Hall)
            .options(joinedload(HallMachine.machine))
            .filter(Hall.gym_id == gym_id)
        )
        result = Session.execute(query)
        gym_machines = result.scalars().all()
        if not gym_machines:
            raise ResourceNotFoundException(f"No machines found in gym_id {gym_id}.")
        return gym_machines

    @staticmethod
    def get_machine_by_id_in_gym(gym_id, machine_id):
        query = (
            select(HallMachine)
            .join(Hall, Hall.id == HallMachine.hall_id)
            .join(Machine, Machine.id == HallMachine.machine_id)
            .filter(Hall.gym_id == gym_id, Machine.id == machine_id)
            .options(joinedload(HallMachine.machine))
        )
        result = Session.execute(query)
        hall_machine = result.scalar_one_or_none()
        if not hall_machine:
            raise ResourceNotFoundException(f"Machine with ID {machine_id} not found in gym_id {gym_id}.")
        return hall_machine
