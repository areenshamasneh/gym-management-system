from gym_app.repositories import GymRepository
from gym_app.exceptions import InvalidInputException, ResourceNotFoundException, DatabaseException
from gym_app.logging import SimpleLogger
from common import Session


class GymComponent:
    def __init__(self, gym_repository=None, logger=None):
        self.gym_repository = gym_repository or GymRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("GymComponent initialized")

    def fetch_all_gyms(self, page_number=1, page_size=10):
        try:
            with Session() as session:
                gyms, total = self.gym_repository.get_all_gyms(session, page_number, page_size)
                return gyms, total
        except Exception as e:
            self.logger.log_error(f"An error occurred while fetching all gyms: {e}")
            raise DatabaseException("An error occurred while fetching all gyms.")

    def fetch_gym_by_id(self, gym_id):
        try:
            with Session() as session:
                gym = self.gym_repository.get_gym_by_id(session, gym_id)
                if gym is None:
                    raise ResourceNotFoundException(f"Gym with ID {gym_id} does not exist")
                return gym
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except Exception as e:
            self.logger.log_error(f"An error occurred while fetching gym by ID {gym_id}: {e}")
            raise DatabaseException(f"An error occurred while fetching gym by ID {gym_id}.")

    def add_gym(self, data):
        try:
            with Session() as session:
                gym = self.gym_repository.create_gym(session, data)
                session.commit()
                session.refresh(gym)
                return gym
        except KeyError as e:
            missing_field = str(e).strip("'")
            raise InvalidInputException(f"Missing required field: '{missing_field}'")
        except ValueError as e:
            self.logger.log_error(f"Invalid data: {e}")
            raise DatabaseException("An error occurred while adding the gym.")
        except Exception as e:
            self.logger.log_error(f"An error occurred while adding the gym: {e}")
            raise DatabaseException("An error occurred while adding the gym.")

    def modify_gym(self, gym_id, data):
        try:
            with Session() as session:
                gym = self.gym_repository.update_gym(session, gym_id, data)
                if gym:
                    session.commit()
                    session.refresh(gym)
                    return gym
                raise ResourceNotFoundException(f"Gym with ID {gym_id} does not exist")
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except ValueError as e:
            self.logger.log_error(f"Invalid data: {e}")
            raise DatabaseException(f"An error occurred while modifying gym ID {gym_id}.")
        except Exception as e:
            self.logger.log_error(f"An error occurred while modifying gym ID {gym_id}: {e}")
            raise DatabaseException(f"An error occurred while modifying gym ID {gym_id}.")

    def remove_gym(self, gym_id):
        try:
            with Session() as session:
                success = self.gym_repository.delete_gym(session, gym_id)
                if not success:
                    raise ResourceNotFoundException(f"Gym with ID {gym_id} does not exist")
                session.commit()
                return success
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except Exception as e:
            self.logger.log_error(f"An error occurred while removing gym ID {gym_id}: {e}")
            raise DatabaseException(f"An error occurred while removing gym ID {gym_id}.")
