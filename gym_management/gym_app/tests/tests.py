import pytest
from unittest.mock import patch, MagicMock
from django.core.exceptions import ObjectDoesNotExist
from gym_app.components.gym_component import GymComponent

@pytest.mark.django_db
class TestGymComponent:
    @patch('gym_app.repositories.gym_repository.GymRepository')
    def test_fetch_all_gyms(self, MockGymRepository):
        # Arrange
        mock_gym_1 = MagicMock()
        mock_gym_1.id = 1
        mock_gym_1.name = "Gym One"
        mock_gym_2 = MagicMock()
        mock_gym_2.id = 2
        mock_gym_2.name = "Gym Two"
        MockGymRepository.get_all_gyms.return_value = [mock_gym_1, mock_gym_2]

        # Act
        result = GymComponent.fetch_all_gyms()

        # Assert
        assert len(result) == 2
        assert result[0].name == "Gym One"
        assert result[1].name == "Gym Two"


    @patch('gym_app.repositories.gym_repository.GymRepository')
    def test_fetch_gym_by_id(self, MockGymRepository):
        # Arrange
        mock_gym = MagicMock()
        mock_gym.id = 1
        mock_gym.name = "Gym One"
        MockGymRepository.get_gym_by_id.return_value = mock_gym

        # Act
        result = GymComponent.fetch_gym_by_id(1)

        # Assert
        assert result.id == 1
        assert result.name == "Gym One"

    @patch('gym_app.repositories.gym_repository.GymRepository')
    def test_add_gym(self, MockGymRepository):
        # Arrange
        gym_data = {"name": "New Gym", "type": "Type C", "address_city": "City A"}  # Include all required fields
        mock_gym = MagicMock()
        mock_gym.id = 3
        MockGymRepository.create_gym.return_value = mock_gym

        # Act
        result = GymComponent.add_gym(gym_data)

        # Assert
        assert result.id == 3
        MockGymRepository.create_gym.assert_called_once_with(gym_data)

    @patch('gym_app.repositories.gym_repository.GymRepository')
    def test_modify_gym(self, MockGymRepository):
        # Arrange
        gym_data = {"name": "Updated Gym", "type": "Type D", "address_city": "New City"}
        mock_gym = MagicMock()
        mock_gym.id = 1
        MockGymRepository.update_gym.return_value = mock_gym

        # Act
        result = GymComponent.modify_gym(1, gym_data)

        # Assert
        assert result.id == 1
        MockGymRepository.update_gym.assert_called_once_with(1, gym_data)

    @patch('gym_app.repositories.gym_repository.GymRepository')
    def test_remove_gym(self, MockGymRepository):
        # Arrange
        MockGymRepository.delete_gym.return_value = None

        # Act
        GymComponent.remove_gym(1)

        # Assert
        MockGymRepository.delete_gym.assert_called_once_with(1)

    @patch('gym_app.repositories.gym_repository.GymRepository')
    def test_fetch_gym_by_id_not_found(self, MockGymRepository):
        # Arrange
        MockGymRepository.get_gym_by_id.side_effect = ObjectDoesNotExist

        # Act & Assert
        with pytest.raises(ObjectDoesNotExist):
            GymComponent.fetch_gym_by_id(999)

    @patch('gym_app.repositories.gym_repository.GymRepository')
    def test_modify_gym_not_found(self, MockGymRepository):
        # Arrange
        gym_data = {"name": "Updated Gym", "type": "Type D"}
        MockGymRepository.update_gym.side_effect = ObjectDoesNotExist

        # Act & Assert
        with pytest.raises(ObjectDoesNotExist):
            GymComponent.modify_gym(999, gym_data)

    @patch('gym_app.repositories.gym_repository.GymRepository')
    def test_remove_gym_not_found(self, MockGymRepository):
        # Arrange
        MockGymRepository.delete_gym.side_effect = ObjectDoesNotExist

        # Act & Assert
        with pytest.raises(ObjectDoesNotExist):
            GymComponent.remove_gym(999)
