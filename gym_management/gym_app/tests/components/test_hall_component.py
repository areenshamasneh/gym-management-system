import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components.hall_component import HallComponent
from gym_app.models import Hall, HallType, Gym


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_fetch_all_halls(mock_logger_class, mock_repo_class):
    mock_hall1 = MagicMock(spec=Hall)
    mock_hall1.name = "Hall 1"
    mock_hall1.users_capacity = 20
    mock_hall1.hall_type = MagicMock(spec=HallType)
    mock_hall1.hall_type.id = 1
    mock_hall1.gym = MagicMock(spec=Gym)
    mock_hall1.gym.id = 1

    mock_hall2 = MagicMock(spec=Hall)
    mock_hall2.name = "Hall 2"
    mock_hall2.users_capacity = 30
    mock_hall2.hall_type = MagicMock(spec=HallType)
    mock_hall2.hall_type.id = 2
    mock_hall2.gym = MagicMock(spec=Gym)
    mock_hall2.gym.id = 2

    mock_repo_class.return_value.get_all_halls.return_value = [mock_hall1, mock_hall2]
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent()

    halls = component.fetch_all_halls(1)

    assert len(halls) == 2
    assert halls[0].name == "Hall 1"
    assert halls[1].name == "Hall 2"
    mock_logger.log.assert_called_with("Fetching all halls")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_fetch_hall_by_id(mock_logger_class, mock_repo_class):
    mock_hall = MagicMock(spec=Hall)
    mock_hall.name = "Hall 1"
    mock_hall.users_capacity = 20
    mock_hall.hall_type = MagicMock(spec=HallType)
    mock_hall.hall_type.id = 1
    mock_hall.gym = MagicMock(spec=Gym)
    mock_hall.gym.id = 1

    mock_repo_class.return_value.get_hall_by_id.return_value = mock_hall
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent()

    hall = component.fetch_hall_by_id(1, 1)

    assert hall.name == "Hall 1"
    assert hall.users_capacity == 20
    mock_logger.log_info.assert_called_with("Fetching hall with ID 1")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_add_hall(mock_logger_class, mock_repo_class):
    mock_hall = MagicMock(spec=Hall)
    mock_hall.name = "Hall 1"
    mock_hall.users_capacity = 20
    mock_hall.hall_type = MagicMock(spec=HallType)
    mock_hall.hall_type.id = 1
    mock_hall.gym = MagicMock(spec=Gym)
    mock_hall.gym.id = 1

    mock_repo_class.return_value.create_hall.return_value = mock_hall
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    data = {"name": "Hall 1", "users_capacity": 20, "hall_type_id": 1}
    hall = component.add_hall(1, data)

    assert hall.name == "Hall 1"
    assert hall.users_capacity == 20
    mock_logger.log_info.assert_any_call(f"Adding new hall with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_modify_hall(mock_logger_class, mock_repo_class):
    mock_hall = MagicMock(spec=Hall)
    mock_hall.name = "Hall Updated"
    mock_hall.users_capacity = 25
    mock_hall.hall_type = MagicMock(spec=HallType)
    mock_hall.hall_type.id = 1
    mock_hall.gym = MagicMock(spec=Gym)
    mock_hall.gym.id = 1

    mock_repo_class.return_value.update_hall.return_value = mock_hall
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    data = {"name": "Hall Updated", "users_capacity": 25, "hall_type_id": 1}
    hall = component.modify_hall(1, 1, data)

    assert hall.name == "Hall Updated"
    assert hall.users_capacity == 25
    mock_logger.log_info.assert_any_call(f"Modifying hall with ID 1 with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_remove_hall(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent()

    component.remove_hall(1, 1)

    assert mock_repo_class.return_value.delete_hall.called
    assert mock_repo_class.return_value.delete_hall.call_count == 1
    mock_logger.log_info.assert_called_with("Removing hall with ID 1")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_add_hall_with_missing_fields(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent()
    mock_repo_class.return_value.create_hall.side_effect = KeyError(
        "Missing required field"
    )

    data = {
        "name": "Hall 1",
        # Missing users_capacity, hall_type_id
    }

    with pytest.raises(KeyError, match="Missing required field"):
        component.add_hall(1, data)
    mock_logger.log_info.assert_called_with(f"Adding new hall with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_modify_hall_non_existent(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent()
    mock_repo_class.return_value.update_hall.side_effect = Hall.DoesNotExist

    data = {"name": "Non Existent Hall", "users_capacity": 20, "hall_type_id": 1}

    with pytest.raises(Hall.DoesNotExist):
        component.modify_hall(1, 999, data)
    mock_logger.log_info.assert_called_with(
        f"Modifying hall with ID 999 with data: {data}"
    )


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_remove_hall_non_existent(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent()
    mock_repo_class.return_value.delete_hall.side_effect = Hall.DoesNotExist

    with pytest.raises(Hall.DoesNotExist):
        component.remove_hall(1, 999)
    mock_logger.log_info.assert_called_with("Removing hall with ID 999")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_fetch_hall_by_id_non_existent(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent()
    mock_repo_class.return_value.get_hall_by_id.side_effect = Hall.DoesNotExist

    with pytest.raises(Hall.DoesNotExist):
        component.fetch_hall_by_id(1, 999)
    mock_logger.log_info.assert_called_with("Fetching hall with ID 999")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_add_hall_invalid_data(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent()
    mock_repo_class.return_value.create_hall.side_effect = ValueError("Invalid data")

    data = {"name": "Hall 1", "users_capacity": -10, "hall_type_id": 1}

    with pytest.raises(ValueError, match="Invalid data"):
        component.add_hall(1, data)
    mock_logger.log_info.assert_called_with(f"Adding new hall with data: {data}")
