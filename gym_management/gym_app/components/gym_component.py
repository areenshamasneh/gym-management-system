from gym_app.models.system_models import Gym
from gym_app.repositories import GymRepository
from gym_app.logging import SimpleLogger
from django.http import Http404


class GymComponent:
    def __init__(self, gym_repository=None, logger=None):
        self.gym_repository = gym_repository or GymRepository()
        self.logger = logger or SimpleLogger()
        self.logger.log_info("GymComponent initialized")

    def fetch_all_gyms(self):
        try:
            self.logger.log_info("Fetching all gyms")
            return self.gym_repository.get_all_gyms()
        except Exception as e:
            self.logger.log_error(f"Error fetching gyms: {str(e)}")
            raise

    def fetch_gym_by_id(self, pk):
        try:
            self.logger.log_info(f"Fetching gym by ID {pk}")
            gym = self.gym_repository.get_gym_by_id(pk)
            if not gym:
                raise Http404("Gym not found")
            return gym
        except Gym.DoesNotExist:
            self.logger.log_error(f"Gym with ID {pk} not found")
            raise Http404(f"Gym with ID {pk} does not exist")
        except Exception as e:
            self.logger.log_error(f"Error fetching gym by ID {pk}: {str(e)}")
            raise

    def add_gym(self, data):
        try:
            self.logger.log_info("Adding new gym")
            self.gym_repository.create_gym(data)
        except Exception as e:
            self.logger.log_error(f"Error adding gym: {str(e)}")
            raise

    def modify_gym(self, pk, data):
        try:
            self.logger.log_info(f"Modifying gym ID {pk}")
            gym = self.gym_repository.get_gym_by_id(pk)
            if not gym:
                raise Http404("Gym not found")
            self.gym_repository.update_gym(pk, data)
        except Gym.DoesNotExist:
            self.logger.log_error(f"Gym with ID {pk} not found")
            raise Http404(f"Gym with ID {pk} does not exist")
        except Exception as e:
            self.logger.log_error(f"Error modifying gym ID {pk}: {str(e)}")
            raise

    def remove_gym(self, pk):
        try:
            self.logger.log_info(f"Removing gym ID {pk}")
            gym = self.gym_repository.get_gym_by_id(pk)
            if not gym:
                raise Http404("Gym not found")
            self.gym_repository.delete_gym(pk)
        except Gym.DoesNotExist:
            self.logger.log_error(f"Gym with ID {pk} not found")
            raise Http404(f"Gym with ID {pk} does not exist")
        except Exception as e:
            self.logger.log_error(f"Error removing gym ID {pk}: {str(e)}")
            raise
