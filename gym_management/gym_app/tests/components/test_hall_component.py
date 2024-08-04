from unittest.mock import patch, MagicMock

import pytest  # type: ignore

from gym_app.components.hall_component import HallComponent
from gym_app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
    DatabaseException,
)


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_fetch_all_halls(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.get_all_halls.return_value = [MagicMock(name="Hall")]
    component.fetch_all_halls(1)

    mock_logger.log_info.assert_called_with("Fetching all halls for gym ID 1")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_fetch_all_halls_db_exception(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.get_all_halls.side_effect = Exception("DB Error")

    with pytest.raises(DatabaseException):
        component.fetch_all_halls(1)

    mock_logger.log_error.assert_called_with("Error fetching all halls: DB Error")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_fetch_hall_by_id(mock_logger_class, mock_repo_class):
    mock_hall = MagicMock(name="Hall")
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.get_hall_by_id.return_value = mock_hall
    component.fetch_hall_by_id(1, 1)

    mock_logger.log_info.assert_called_with("Fetching hall with ID 1 for gym ID 1")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_fetch_hall_by_id_not_found(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.get_hall_by_id.return_value = None

    with pytest.raises(ResourceNotFoundException):
        component.fetch_hall_by_id(1, 999)

    mock_logger.log_error.assert_called_with("Hall with ID 999 not found")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_add_hall(mock_logger_class, mock_repo_class):
    mock_hall = MagicMock(name="Hall")
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.create_hall.return_value = mock_hall
    data = {"name": "Hall 1", "users_capacity": 20, "hall_type_id": 1}
    component.add_hall(1, data)

    mock_logger.log_info.assert_any_call(
        f"Adding new hall with data: {data} for gym ID 1"
    )
    mock_logger.log_info.assert_any_call(f"Hall added: {mock_hall}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_add_hall_validation_exception(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.create_hall.side_effect = ValueError("Invalid data")

    data = {"name": "Hall 1"}
    with pytest.raises(ValidationException):
        component.add_hall(1, data)

    mock_logger.log_error.assert_called_with("Error adding hall: Invalid data")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_add_hall_db_exception(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.create_hall.side_effect = Exception("DB Error")

    data = {"name": "Hall 1", "users_capacity": 20, "hall_type_id": 1}
    with pytest.raises(DatabaseException):
        component.add_hall(1, data)

    mock_logger.log_error.assert_called_with("Error adding hall: DB Error")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_modify_hall(mock_logger_class, mock_repo_class):
    mock_hall = MagicMock(name="Hall")
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.update_hall.return_value = mock_hall
    data = {"name": "Hall Updated", "users_capacity": 25, "hall_type_id": 1}
    component.modify_hall(1, 1, data)
    mock_logger.log_info.assert_any_call(
        f"Modifying hall with ID 1 with data: {data} for gym ID 1"
    )
    mock_logger.log_info.assert_any_call(f"Hall modified: {mock_hall}")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_modify_hall_not_found(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.update_hall.return_value = None

    data = {"name": "Hall Updated", "users_capacity": 25, "hall_type_id": 1}
    with pytest.raises(ResourceNotFoundException):
        component.modify_hall(1, 999, data)

    mock_logger.log_error.assert_called_with("Hall with ID 999 not found")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_modify_hall_validation_exception(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.update_hall.side_effect = ValueError("Invalid data")

    data = {"name": "Hall Updated"}
    with pytest.raises(ValidationException):
        component.modify_hall(1, 1, data)

    mock_logger.log_error.assert_called_with("Error modifying hall: Invalid data")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_modify_hall_db_exception(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.update_hall.side_effect = Exception("DB Error")

    data = {"name": "Hall Updated", "users_capacity": 25, "hall_type_id": 1}
    with pytest.raises(DatabaseException):
        component.modify_hall(1, 1, data)

    mock_logger.log_error.assert_called_with("Error modifying hall: DB Error")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_remove_hall(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    component.remove_hall(1, 1)

    mock_logger.log_info.assert_called_with("Removing hall with ID 1 for gym ID 1")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_remove_hall_not_found(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.delete_hall.return_value = False

    with pytest.raises(ResourceNotFoundException):
        component.remove_hall(1, 999)

    mock_logger.log_error.assert_called_with("Hall with ID 999 not found")


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
@patch("gym_app.components.hall_component.SimpleLogger")
def test_remove_hall_db_exception(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.delete_hall.side_effect = Exception("DB Error")

    with pytest.raises(DatabaseException):
        component.remove_hall(1, 1)

    mock_logger.log_error.assert_called_with("Error removing hall: DB Error")
