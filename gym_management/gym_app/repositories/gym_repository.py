from django.core.paginator import Paginator
from sqlalchemy import select
from gym_app.models.models_sqlalchemy import Gym
from gym_app.utils import PaginationResponse
from gym_management.settings import SessionLocal


class GymRepository:
    @staticmethod
    def get_all_gyms(page_number=1, page_size=10):
        with SessionLocal() as session:
            query = select(Gym)
            result = session.execute(query)
            gyms = result.scalars().all()
            paginator = Paginator(gyms, page_size)
            paginated_gyms = paginator.get_page(page_number)
            return PaginationResponse(
                items=list(paginated_gyms),
                total_items=paginator.count,
                total_pages=paginator.num_pages,
                current_page=paginated_gyms.number,
                page_size=page_size
            )

    @staticmethod
    def get_gym_by_id(pk):
        with SessionLocal() as session:
            return session.get(Gym, pk)

    @staticmethod
    def create_gym(data):
        print(f"Request data: {data}")  #
        with SessionLocal() as session:
            gym = Gym(
                name=data.get("name"),
                type=data.get("type"),
                description=data.get("description"),
                address_city=data.get("address_city"),
                address_street=data.get("address_street"),
            )
            session.add(gym)
            session.commit()
            session.refresh(gym)
            return gym

    @staticmethod
    def update_gym(pk, data):
        with SessionLocal() as session:
            gym = session.get(Gym, pk)
            if gym:
                for key, value in data.items():
                    setattr(gym, key, value)
                session.commit()
                session.refresh(gym)
                return gym
            return None

    @staticmethod
    def delete_gym(pk):
        with SessionLocal() as session:
            gym = session.get(Gym, pk)
            if gym:
                session.delete(gym)
                session.commit()
                return True
            return False
