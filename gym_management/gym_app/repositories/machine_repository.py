from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from gym_app.models.models_sqlalchemy import Hall, Machine, HallMachine
from gym_app.exceptions import ResourceNotFoundException
from gym_management.settings import SessionLocal

class MachineRepository:

    @staticmethod
    def get_all_machines_in_hall(gym_id, hall_id):
        with SessionLocal() as session:
            try:
                query = (
                    select(Machine)
                    .join(HallMachine)
                    .join(Hall)
                    .filter(HallMachine.hall_id == hall_id, Hall.gym_id == gym_id)
                )
                result = session.execute(query)
                machines = result.scalars().all()
                if not machines:
                    raise ResourceNotFoundException(f"No machines found in hall {hall_id} for gym_id {gym_id}.")
                return machines
            except SQLAlchemyError as e:
                session.rollback()
                raise

    @staticmethod
    def get_machine_by_id_in_hall(gym_id, hall_id, machine_id):
        with SessionLocal() as session:
            try:
                query = (
                    select(HallMachine)
                    .options(joinedload(HallMachine.machine), joinedload(HallMachine.hall))
                    .join(Hall)
                    .join(Machine)
                    .filter(Hall.id == hall_id, Hall.gym_id == gym_id, Machine.id == machine_id)
                )
                result = session.execute(query)
                hall_machine = result.scalar_one_or_none()
                if not hall_machine:
                    raise ResourceNotFoundException(
                        f"Machine with ID {machine_id} not found in hall {hall_id} for gym_id {gym_id}.")
                return hall_machine
            except SQLAlchemyError as e:
                session.rollback()
                raise

    @staticmethod
    def create_machine(data):
        with SessionLocal() as session:
            try:
                machine = Machine(
                    serial_number=data["serial_number"],
                    type=data.get("type"),
                    model=data.get("model"),
                    brand=data.get("brand"),
                    status=data.get("status"),
                    maintenance_date=data.get("maintenance_date"),
                )
                session.add(machine)
                session.commit()
                session.refresh(machine)
                return machine
            except SQLAlchemyError as e:
                session.rollback()
                raise

    @staticmethod
    def create_hall_machine(gym_id, hall_id, machine_id):
        with SessionLocal() as session:
            try:
                hall_machine = HallMachine(
                    hall_id=hall_id,
                    machine_id=machine_id
                )
                session.add(hall_machine)
                session.commit()
                session.refresh(hall_machine)
                session.refresh(hall_machine, attribute_names=['hall', 'machine'])

                return hall_machine

            except SQLAlchemyError as e:
                session.rollback()
                raise

    @staticmethod
    def update_hall_machine(gym_id, hall_id, machine_id, data):
        with SessionLocal() as session:
            try:
                hall_machine = MachineRepository.get_machine_by_id_in_hall(gym_id, hall_id, machine_id)
                if "hall_id" in data:
                    hall_instance = session.get(Hall, data.get("hall_id"))
                    if not hall_instance or hall_instance.gym_id != gym_id:
                        raise ResourceNotFoundException(f"Hall with ID {data.get('hall_id')} not found in gym_id {gym_id}.")
                    hall_machine.hall = hall_instance
                if "machine_id" in data:
                    machine_instance = session.get(Machine, data.get("machine_id"))
                    if not machine_instance:
                        raise ResourceNotFoundException(f"Machine with ID {data.get('machine_id')} not found.")
                    hall_machine.machine = machine_instance
                if "name" in data:
                    hall_machine.name = data.get("name")
                if "uid" in data:
                    hall_machine.uid = data.get("uid")
                session.commit()
                session.refresh(hall_machine)
                return hall_machine
            except SQLAlchemyError as e:
                session.rollback()
                raise

    @staticmethod
    def delete_hall_machine(gym_id, hall_id, machine_id):
        with SessionLocal() as session:
            try:
                hall_machine = MachineRepository.get_machine_by_id_in_hall(gym_id, hall_id, machine_id)
                session.delete(hall_machine)
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise

    @staticmethod
    def get_all_machines_in_gym(gym_id):
        with SessionLocal() as session:
            try:
                query = (
                    select(HallMachine)
                    .join(Hall)
                    .join(Machine)
                    .filter(Hall.gym_id == gym_id)
                )
                result = session.execute(query)
                gym_machines = result.scalars().all()
                if not gym_machines:
                    raise ResourceNotFoundException(f"No machines found in gym_id {gym_id}.")
                return gym_machines
            except SQLAlchemyError as e:
                session.rollback()
                raise

    @staticmethod
    def get_machine_by_id_in_gym(gym_id, machine_id):
        with SessionLocal() as session:
            try:
                query = (
                    select(HallMachine)
                    .join(Hall)
                    .join(Machine)
                    .filter(Hall.gym_id == gym_id, Machine.id == machine_id)
                )
                result = session.execute(query)
                hall_machine = result.scalar_one_or_none()
                if not hall_machine:
                    raise ResourceNotFoundException(f"Machine with ID {machine_id} not found in gym_id {gym_id}.")
                return hall_machine
            except SQLAlchemyError as e:
                session.rollback()
                raise
