from gym_app.repositories import GymRepository
from gym_app.exceptions import InvalidInputException, ResourceNotFoundException, DatabaseException
from gym_app.logging import SimpleLogger


class GymComponent:
    def __init__(self, gym_repository=None, logger=None):
        self.gym_repository = gym_repository or GymRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("GymComponent initialized")

    def fetch_all_gyms(self, page_number=1, page_size=10, db_session=None):
        try:
            gyms, total = self.gym_repository.get_all_gyms(db_session, page_number, page_size)
            return gyms, total
        except Exception as e:
            self.logger.log_error(f"An error occurred while fetching all gyms: {e}")
            raise DatabaseException("An error occurred while fetching all gyms.")

    def fetch_gym_by_id(self, gym_id, db_session=None):
        try:
            gym = self.gym_repository.get_gym_by_id(db_session, gym_id)
            if gym is None:
                raise ResourceNotFoundException(f"Gym with ID {gym_id} does not exist")
            return gym
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except Exception as e:
            self.logger.log_error(f"An error occurred while fetching gym by ID {gym_id}: {e}")
            raise DatabaseException(f"An error occurred while fetching gym by ID {gym_id}.")

    def add_gym(self, data, db_session=None):
        try:
            gym = self.gym_repository.create_gym(db_session, data)
            db_session.commit()
            db_session.refresh(gym)
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

    def modify_gym(self, gym_id, data, db_session=None):
        try:
            gym = self.gym_repository.update_gym(db_session, gym_id, data)
            if gym:
                db_session.commit()
                db_session.refresh(gym)
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

    def remove_gym(self, gym_id, db_session=None):
        try:
            success = self.gym_repository.delete_gym(db_session, gym_id)
            if not success:
                raise ResourceNotFoundException(f"Gym with ID {gym_id} does not exist")
            db_session.commit()
            return success
        except ResourceNotFoundException as e:
            self.logger.log_error(str(e))
            raise
        except Exception as e:
            self.logger.log_error(f"An error occurred while removing gym ID {gym_id}: {e}")
            raise DatabaseException(f"An error occurred while removing gym ID {gym_id}.")
