from sqlalchemy import select, update
from sqlalchemy.orm import joinedload

from common.db.database import Session
from gym_app.models.models_sqlalchemy import Hall, Machine, HallMachine, Gym


class MachineRepository:
    @staticmethod
    def get_gym(gym_id):
        return Session.get(Gym, gym_id)

    @staticmethod
    def get_all_machines_in_hall(gym, hall_id):
        query = (
            select(Machine)
            .join(HallMachine)
            .join(Hall)
            .where(HallMachine.hall_id == hall_id, Hall.gym_id == gym.id)
        )
        result = Session.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_machine_by_id_in_hall(gym, hall_id, machine_id):
        query = (
            select(HallMachine)
            .options(joinedload(HallMachine.machine), joinedload(HallMachine.hall))
            .join(Hall)
            .join(Machine)
            .where(Hall.id == hall_id, Hall.gym_id == gym.id, Machine.id == machine_id)
        )
        result = Session.execute(query)
        return result.scalar_one_or_none()

    @staticmethod
    def create_machine(data):
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
    def create_hall_machine(hall_id, machine_id):
        hall_query = select(Hall).where(Hall.id == hall_id)
        machine_query = select(Machine).where(Machine.id == machine_id)

        hall = Session.execute(hall_query).scalar_one_or_none()
        machine = Session.execute(machine_query).scalar_one_or_none()

        type_count_query = (
            select(HallMachine)
            .join(Machine)
            .where(HallMachine.hall_id == hall_id, Machine.type == machine.type)
        )
        type_count = len(Session.execute(type_count_query).scalars().all()) + 1

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
    def update_machine(gym, hall_id, machine_id, data):
        query = (
            select(HallMachine)
            .options(joinedload(HallMachine.machine))
            .join(Hall)
            .where(Hall.gym_id == gym.id, Hall.id == hall_id, HallMachine.machine_id == machine_id)
        )
        hall_machine = Session.execute(query).scalar_one_or_none()

        if hall_machine:
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
        hall_query = select(Hall).where(Hall.id == hall_machine.hall_id)
        hall = Session.execute(hall_query).scalar_one_or_none()

        type_count_query = (
            select(HallMachine)
            .join(Machine)
            .where(HallMachine.hall_id == hall_machine.hall_id, Machine.type == machine.type)
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
    def delete_hall_machine(gym, hall_id, machine_id):
        hall_machine = MachineRepository.get_machine_by_id_in_hall(gym, hall_id, machine_id)
        if hall_machine:
            Session.delete(hall_machine)
            return True
        return False

    @staticmethod
    def get_all_machines_in_gym(gym):
        query = (
            select(HallMachine)
            .join(Hall)
            .options(joinedload(HallMachine.machine))
            .where(Hall.gym_id == gym.id)
        )
        result = Session.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_machine_by_id_in_gym(gym, machine_id):
        query = (
            select(HallMachine)
            .join(Hall, Hall.id == HallMachine.hall_id)
            .join(Machine, Machine.id == HallMachine.machine_id)
            .where(Hall.gym_id == gym.id, Machine.id == machine_id)
            .options(joinedload(HallMachine.machine))
        )
        result = Session.execute(query)
        return result.scalar_one_or_none()
