import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components import GymComponent
from gym_app.models.system_models import Gym


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
    mock_gym = MagicMock()
    mock_gym.id = 1
    mock_gym.name = "New Gym"
    mock_gym.type = "Type A"
    mock_gym.description = "Desc"
    mock_gym.address_city = "City"
    mock_gym.address_street = "Street"

    mock_data = {
        "name": "New Gym",
        "type": "Type A",
        "description": "Desc",
        "address_city": "City",
        "address_street": "Street",
    }

    mock_repo.create_gym.return_value = mock_gym

    component = GymComponent(mock_repo, mock_logger)
    result = component.add_gym(mock_data)

    assert result.name == "New Gym"
    assert result.address_city == "City"


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_modify_gym(mock_logger, mock_repo):
    gym = MagicMock()
    gym.id = 1
    gym.name = "Updated Gym"
    gym.type = "Type B"
    gym.description = "Updated Desc"
    gym.address_city = "Updated City"
    gym.address_street = "Updated Street"

    mock_repo.update_gym.return_value = gym
    mock_data = {
        "name": "Updated Gym",
        "type": "Type B",
        "description": "Updated Desc",
        "address_city": "Updated City",
        "address_street": "Updated Street",
    }

    component = GymComponent(mock_repo, mock_logger)
    result = component.modify_gym(1, mock_data)

    assert result.name == "Updated Gym"
    assert result.address_city == "Updated City"


@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_remove_gym(mock_logger, mock_repo):
    mock_repo.delete_gym.return_value = None

    component = GymComponent(mock_repo, mock_logger)
    component.remove_gym(1)

    mock_repo.delete_gym.assert_called_once_with(1)


@pytest.mark.django_db
@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_add_gym_with_missing_fields(mock_logger, mock_repo):
    mock_repo.create_gym.side_effect = KeyError("Missing required field")

    data = {
        "name": "New Gym",
        # Missing type, description, address_city, address_street
    }

    component = GymComponent(mock_repo, mock_logger)
    with pytest.raises(KeyError, match="Missing required field"):
        component.add_gym(data)


@pytest.mark.django_db
@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_modify_gym_non_existent(mock_logger, mock_repo):
    mock_repo.update_gym.side_effect = Gym.DoesNotExist

    data = {
        "name": "Non Existent Gym",
        "type": "Type C",
        "description": "Non Existent Desc",
        "address_city": "Non Existent City",
        "address_street": "Non Existent Street",
    }

    component = GymComponent(mock_repo, mock_logger)
    with pytest.raises(Gym.DoesNotExist):
        component.modify_gym(999, data)


@pytest.mark.django_db
@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_remove_gym_non_existent(mock_logger, mock_repo):
    mock_repo.delete_gym.side_effect = Gym.DoesNotExist

    component = GymComponent(mock_repo, mock_logger)
    with pytest.raises(Gym.DoesNotExist):
        component.remove_gym(999)


@pytest.mark.django_db
@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_fetch_gym_by_id_non_existent(mock_logger, mock_repo):
    mock_repo.get_gym_by_id.side_effect = Gym.DoesNotExist

    component = GymComponent(mock_repo, mock_logger)
    with pytest.raises(Gym.DoesNotExist):
        component.fetch_gym_by_id(999)


@pytest.mark.django_db
@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_add_gym_invalid_data(mock_logger, mock_repo):
    mock_repo.create_gym.side_effect = ValueError("Invalid data")

    data = {
        "name": "New Gym",
        "type": "Invalid Type",
        "description": "Desc",
        "address_city": "City",
        "address_street": "Street",
    }

    component = GymComponent(mock_repo, mock_logger)
    with pytest.raises(ValueError, match="Invalid data"):
        component.add_gym(data)


@pytest.mark.django_db
@patch("gym_app.components.gym_component.GymRepository")
@patch("gym_app.components.gym_component.SimpleLogger")
def test_modify_gym_invalid_data(mock_logger, mock_repo):
    mock_repo.update_gym.side_effect = ValueError("Invalid data")

    data = {
        "name": "Updated Gym",
        "type": "Invalid Type",
        "description": "Updated Desc",
        "address_city": "Updated City",
        "address_street": "Updated Street",
    }

    component = GymComponent(mock_repo, mock_logger)
    with pytest.raises(ValueError, match="Invalid data"):
        component.modify_gym(1, data)
