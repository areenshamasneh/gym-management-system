from sqlalchemy import select
from sqlalchemy.orm import selectinload

from common.db.database import Session
from gym_app.models.models_sqlalchemy import Hall, HallMachine, Gym


class HallMachineRepository:
    @staticmethod
    def get_gym(gym_id):
        return Session.get(Gym, gym_id)

    @staticmethod
    def get_hall_machines_by_gym(gym):
        query = (
            select(HallMachine)
            .join(Hall)
            .where(Hall.gym_id == gym.id)
            .options(
                selectinload(HallMachine.hall).selectinload(Hall.gym),
                selectinload(HallMachine.hall).selectinload(Hall.hall_type),
                selectinload(HallMachine.machine)
            )
        )
        result = Session.execute(query)
        return result.scalars().all()
