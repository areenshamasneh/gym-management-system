from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from gym_app.exceptions import ResourceNotFoundException
from gym_app.models.models_sqlalchemy import Hall, Machine, HallMachine
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
                hall = session.get(Hall, hall_id)
                machine = session.get(Machine, machine_id)

                type_count = (
                                 session.query(HallMachine)
                                 .join(Machine)
                                 .filter(HallMachine.hall_id == hall_id, Machine.type == machine.type)
                                 .count()
                             ) + 1

                hall_machine_name = f"{hall.name} - {machine.type.capitalize()}"
                hall_machine_uid = f"{machine.type}_{type_count}"

                hall_machine = HallMachine(
                    hall_id=hall_id,
                    machine_id=machine_id,
                    name=hall_machine_name,
                    uid=hall_machine_uid
                )

                session.add(hall_machine)
                session.commit()
                session.refresh(hall_machine)

                return hall_machine

            except SQLAlchemyError as e:
                session.rollback()
                raise

    @staticmethod
    def update_machine_and_hall_machine(gym_id, hall_id, machine_id, data):
        with SessionLocal() as session:
            try:
                hall_machine_query = (
                    select(HallMachine)
                    .options(joinedload(HallMachine.machine))
                    .join(Hall)
                    .filter(Hall.gym_id == gym_id, Hall.id == hall_id, HallMachine.machine_id == machine_id)
                )
                hall_machine = session.execute(hall_machine_query).scalar_one_or_none()

                if not hall_machine:
                    raise ResourceNotFoundException(
                        f"Machine with ID {machine_id} not found in hall {hall_id} for gym_id {gym_id}."
                    )

                machine = hall_machine.machine
                original_type = machine.type
                machine.type = data.get("type", machine.type)
                machine.serial_number = data.get("serial_number", machine.serial_number)
                machine.model = data.get("model", machine.model)
                machine.brand = data.get("brand", machine.brand)
                machine.status = data.get("status", machine.status)
                machine.maintenance_date = data.get("maintenance_date", machine.maintenance_date)

                session.commit()
                session.refresh(machine)

                if original_type != machine.type:
                    hall = session.get(Hall, hall_id)

                    type_count = (
                                     session.query(HallMachine)
                                     .join(Machine)
                                     .filter(HallMachine.hall_id == hall_id, Machine.type == machine.type)
                                     .count()
                                 ) + 1

                    hall_machine.name = f"{hall.name} - {machine.type.capitalize()}"
                    hall_machine.uid = f"{machine.type}_{type_count}"
                    session.commit()

                session.refresh(hall_machine)
                session.refresh(hall_machine, attribute_names=['name', 'uid'])

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
                    .options(joinedload(HallMachine.machine))
                    .filter(Hall.gym_id == gym_id)
                )
                result = session.execute(query)
                gym_machines = result.scalars().all()
                if not gym_machines:
                    raise ResourceNotFoundException(f"No machines found in gym_id {gym_id}.")
                return gym_machines
            except SQLAlchemyError as e:
                print(f"SQLAlchemy error in get_all_machines_in_gym: {str(e)}")
                session.rollback()
                raise

    @staticmethod
    def get_machine_by_id_in_gym(gym_id, machine_id):
        with SessionLocal() as session:
            try:
                query = (
                    select(HallMachine)
                    .join(Hall, Hall.id == HallMachine.hall_id)
                    .join(Machine, Machine.id == HallMachine.machine_id)
                    .filter(Hall.gym_id == gym_id, Machine.id == machine_id)
                    .options(joinedload(HallMachine.machine))
                )
                result = session.execute(query)
                hall_machine = result.scalar_one_or_none()
                if not hall_machine:
                    raise ResourceNotFoundException(f"Machine with ID {machine_id} not found in gym_id {gym_id}.")
                return hall_machine
            except SQLAlchemyError as e:
                print(f"SQLAlchemy error in get_machine_by_id_in_gym: {str(e)}")
                session.rollback()
                raise
