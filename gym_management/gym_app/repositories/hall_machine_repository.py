from sqlalchemy import select
from sqlalchemy.orm import selectinload

from common.db.database import Session
from gym_app.models.models_sqlalchemy import Hall, HallMachine


class HallMachineRepository:
    @staticmethod
    def get_hall_machines_by_gym(gym_id):
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
        result = Session.execute(query)
        return result.scalars().all()

    @staticmethod
    def get_hall_machines_by_hall(hall_id):
        query = select(HallMachine).filter(HallMachine.hall_id == hall_id)
        result = Session.execute(query)
        return result.scalars().all()
