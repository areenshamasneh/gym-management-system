from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import selectinload

from gym_management.settings import SessionLocal
from gym_app.models.models_sqlalchemy import Hall, HallMachine


class HallMachineRepository:
    @staticmethod
    def get_hall_machines_by_gym(gym_id):
        with SessionLocal() as session:
            query = (
                select(HallMachine)
                .join(Hall)
                .filter(Hall.gym_id == gym_id)
                .options(
                    selectinload(HallMachine.hall).selectinload(Hall.gym),
                    selectinload(HallMachine.hall).selectinload(Hall.hall_type),
                    selectinload(HallMachine.machine)
                )
            )
            result = session.execute(query)
            return result.scalars().all()

    @staticmethod
    def get_hall_machines_by_hall(hall_id):
        with SessionLocal() as session:
            query = select(HallMachine).filter(HallMachine.hall_id == hall_id)
            result = session.execute(query)
            return result.scalars().all()
