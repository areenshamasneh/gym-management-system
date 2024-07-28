import pytest  # type: ignore
from unittest.mock import patch, MagicMock, call
from gym_app.components.hall_component import HallComponent
from gym_app.models import Hall, HallType, Gym


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_fetch_all_halls(mock_logger, mock_repo):
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

    mock_repo.get_all_halls.return_value = [mock_hall1, mock_hall2]
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    halls = component.fetch_all_halls(1)

    assert len(halls) == 2
    assert halls[0].name == "Hall 1"
    assert halls[1].name == "Hall 2"
    logger.log.assert_called_with("Fetching all halls")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_fetch_hall_by_id(mock_logger, mock_repo):
    mock_hall = MagicMock(spec=Hall)
    mock_hall.name = "Hall 1"
    mock_hall.users_capacity = 20
    mock_hall.hall_type = MagicMock(spec=HallType)
    mock_hall.hall_type.id = 1
    mock_hall.gym = MagicMock(spec=Gym)
    mock_hall.gym.id = 1

    mock_repo.get_hall_by_id.return_value = mock_hall
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    hall = component.fetch_hall_by_id(1, 1)

    assert hall.name == "Hall 1"
    assert hall.users_capacity == 20
    logger.log.assert_called_with("Fetching hall with ID 1")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_add_hall(mock_logger, mock_repo):
    mock_hall = MagicMock(spec=Hall)
    mock_hall.name = "Hall 1"
    mock_hall.users_capacity = 20
    mock_hall.hall_type = MagicMock(spec=HallType)
    mock_hall.hall_type.id = 1
    mock_hall.gym = MagicMock(spec=Gym)
    mock_hall.gym.id = 1

    mock_repo.create_hall.return_value = mock_hall

    data = {"name": "Hall 1", "users_capacity": 20, "hall_type_id": 1}
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    hall = component.add_hall(1, data)

    assert hall.name == "Hall 1"
    assert hall.users_capacity == 20
    logger.log.assert_called_with(f"Adding new hall with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_modify_hall(mock_logger, mock_repo):
    mock_hall = MagicMock(spec=Hall)
    mock_hall.name = "Hall Updated"
    mock_hall.users_capacity = 25
    mock_hall.hall_type = MagicMock(spec=HallType)
    mock_hall.hall_type.id = 1
    mock_hall.gym = MagicMock(spec=Gym)
    mock_hall.gym.id = 1

    mock_repo.update_hall.return_value = mock_hall

    data = {"name": "Hall Updated", "users_capacity": 25, "hall_type_id": 1}
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    hall = component.modify_hall(1, 1, data)

    assert hall.name == "Hall Updated"
    assert hall.users_capacity == 25
    logger.log.assert_called_with(f"Modifying hall with ID 1 with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_remove_hall(mock_logger, mock_repo):
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    component.remove_hall(1, 1)

    assert mock_repo.delete_hall.called
    assert mock_repo.delete_hall.call_count == 1
    logger.log.assert_called_with("Removing hall with ID 1")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_add_hall_with_missing_fields(mock_logger, mock_repo):
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    mock_repo.create_hall.side_effect = KeyError("Missing required field")

    data = {
        "name": "Hall 1",
        # Missing users_capacity, hall_type_id
    }

    with pytest.raises(KeyError, match="Missing required field"):
        component.add_hall(1, data)
    logger.log.assert_called_with(f"Adding new hall with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_modify_hall_non_existent(mock_logger, mock_repo):
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    mock_repo.update_hall.side_effect = Hall.DoesNotExist

    data = {"name": "Non Existent Hall", "users_capacity": 20, "hall_type_id": 1}

    with pytest.raises(Hall.DoesNotExist):
        component.modify_hall(1, 999, data)
    logger.log.assert_called_with(f"Modifying hall with ID 999 with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_remove_hall_non_existent(mock_logger, mock_repo):
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    mock_repo.delete_hall.side_effect = Hall.DoesNotExist

    with pytest.raises(Hall.DoesNotExist):
        component.remove_hall(1, 999)
    logger.log.assert_called_with("Removing hall with ID 999")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_fetch_hall_by_id_non_existent(mock_logger, mock_repo):
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    mock_repo.get_hall_by_id.side_effect = Hall.DoesNotExist

    with pytest.raises(Hall.DoesNotExist):
        component.fetch_hall_by_id(1, 999)
    logger.log.assert_called_with("Fetching hall with ID 999")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_add_hall_invalid_data(mock_logger, mock_repo):
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    mock_repo.create_hall.side_effect = ValueError("Invalid data")

    data = {"name": "Hall 1", "users_capacity": -10, "hall_type_id": 1}

    with pytest.raises(ValueError, match="Invalid data"):
        component.add_hall(1, data)
    logger.log.assert_called_with(f"Adding new hall with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_modify_hall_invalid_data(mock_logger, mock_repo):
    logger = MagicMock()
    component = HallComponent(mock_repo, logger)
    mock_repo.update_hall.side_effect = ValueError("Invalid data")

    data = {"name": "Hall Updated", "users_capacity": -20, "hall_type_id": 1}

    with pytest.raises(ValueError, match="Invalid data"):
        component.modify_hall(1, 1, data)
    logger.log.assert_called_with(f"Modifying hall with ID 1 with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.CustomLogger")
def test_add_hall_with_form_validation(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo

    component = HallComponent(mock_repo, mock_logger)

    valid_data = {"name": "Hall Valid", "users_capacity": 10, "hall_type_id": 1}

    invalid_data = {"name": "", "users_capacity": -5, "hall_type_id": 999}

    mock_repo.create_hall.return_value = MagicMock(id=1)

    hall = component.add_hall(1, valid_data)
    assert hall is not None
    assert hall.id == 1

    expected_call = call(f"Adding new hall with data: {valid_data}")
    assert mock_logger.log.call_args_list[0] == expected_call

    mock_repo.create_hall.side_effect = ValueError("Invalid data")

    with pytest.raises(ValueError, match="Invalid data"):
        component.add_hall(1, invalid_data)

    expected_call_invalid = call(f"Adding new hall with data: {invalid_data}")
    assert mock_logger.log.call_args_list[1] == expected_call_invalid
