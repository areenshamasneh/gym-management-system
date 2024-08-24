from unittest.mock import patch, MagicMock

import pytest  # type: ignore

from gym_app.components import GymComponent
from gym_app.exceptions import (
    DatabaseException,
    InvalidInputException,
    ResourceNotFoundException,
)


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_fetch_all_gyms(mock_logger, mock_repo):
    gym1 = MagicMock()
    gym1.id = 1
    gym1.name = "Gym 1"
    gym1.type = "Type A"
    gym1.description = "Desc 1"
    gym1.address_city = "City 1"
    gym1.address_street = "Street 1"

    gym2 = MagicMock()
    gym2.id = 2
    gym2.name = "Gym 2"
    gym2.type = "Type B"
    gym2.description = "Desc 2"
    gym2.address_city = "City 2"
    gym2.address_street = "Street 2"

    mock_repo.get_all_gyms.return_value = [gym1, gym2]

    component = GymComponent(mock_repo, mock_logger)
    gyms = component.fetch_all_gyms()

    assert len(gyms) == 2
    assert gyms[0].name == "Gym 1"
    assert gyms[1].name == "Gym 2"


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_fetch_gym_by_id(mock_logger, mock_repo):
    gym = MagicMock()
    gym.id = 1
    gym.name = "Gym 1"
    gym.type = "Type A"
    gym.description = "Desc 1"
    gym.address_city = "City 1"
    gym.address_street = "Street 1"

    mock_repo.get_gym_by_id.return_value = gym

    component = GymComponent(mock_repo, mock_logger)
    result = component.fetch_gym_by_id(1)

    assert result.name == "Gym 1"
    assert result.address_city == "City 1"


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_add_gym(mock_logger, mock_repo):
    mock_repo.create_gym = MagicMock()
    mock_logger.log_info = MagicMock()

    component = GymComponent(mock_repo, mock_logger)

    mock_data = {
        "name": "New Gym",
        "type": "Type A",
        "description": "Desc",
        "address_city": "City",
        "address_street": "Street",
    }

    component.add_gym(mock_data)

    mock_repo.create_gym.assert_called_once_with(mock_data)
    mock_logger.log_info.assert_called_with("Adding new gym")


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_modify_gym(mock_logger, mock_repo):
    gym = MagicMock()
    gym.id = 1

    mock_repo.update_gym = MagicMock()
    mock_logger.log_info = MagicMock()

    component = GymComponent(mock_repo, mock_logger)

    mock_data = {
        "name": "Updated Gym",
        "type": "Type B",
        "description": "Updated Desc",
        "address_city": "Updated City",
        "address_street": "Updated Street",
    }

    component.modify_gym(1, mock_data)

    mock_repo.update_gym.assert_called_once_with(1, mock_data)
    mock_logger.log_info.assert_called_with("Modifying gym ID 1")


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_remove_gym(mock_logger, mock_repo):
    mock_repo.delete_gym.return_value = None

    component = GymComponent(mock_repo, mock_logger)
    component.remove_gym(1)

    mock_repo.delete_gym.assert_called_once_with(1)


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_add_gym_with_missing_fields(mock_logger, mock_repo):
    mock_repo.create_gym.side_effect = KeyError("name")

    data = {
        "name": "New Gym",
    }

    component = GymComponent(mock_repo, mock_logger)
    with pytest.raises(InvalidInputException, match="Missing required field: 'name'"):
        component.add_gym(data)


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_modify_gym_non_existent(mock_logger, mock_repo):
    mock_repo.update_gym.side_effect = ResourceNotFoundException(
        "Gym with ID 999 does not exist"
    )

    data = {
        "name": "Non Existent Gym",
        "type": "Type C",
        "description": "Non Existent Desc",
        "address_city": "Non Existent City",
        "address_street": "Non Existent Street",
    }

    component = GymComponent(mock_repo, mock_logger)
    with pytest.raises(
            ResourceNotFoundException, match="Gym with ID 999 does not exist"
    ):
        component.modify_gym(999, data)


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_remove_gym_non_existent(mock_logger, mock_repo):
    mock_repo.delete_gym.side_effect = ResourceNotFoundException(
        "Gym with ID 999 does not exist"
    )

    component = GymComponent(mock_repo, mock_logger)
    with pytest.raises(
            ResourceNotFoundException, match="Gym with ID 999 does not exist"
    ):
        component.remove_gym(999)


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_fetch_gym_by_id_non_existent(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger

    mock_repo_class.get_gym_by_id.side_effect = ResourceNotFoundException(
        "Gym with ID 999 does not exist"
    )

    component = GymComponent(mock_repo_class, mock_logger)

    with pytest.raises(
            ResourceNotFoundException, match="Resource not found for gym_id: 999"
    ):
        component.fetch_gym_by_id(999)

    mock_logger.log_error.assert_called_with("Gym with ID 999 does not exist")


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_modify_gym_invalid_data(mock_logger, mock_repo):
    mock_repo.update_gym.side_effect = ValueError("Invalid data")

    gym_id = 1
    data = {
        "name": "Updated Gym",
        "type": "Type",
        "description": "Updated Desc",
        "address_city": "Updated City",
        "address_street": "Updated Street",
    }

    component = GymComponent(mock_repo, mock_logger)
    with pytest.raises(
            DatabaseException, match=f"An error occurred while modifying gym ID {gym_id}."
    ):
        component.modify_gym(gym_id, data)
