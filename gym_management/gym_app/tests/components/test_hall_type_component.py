from unittest.mock import MagicMock, patch

import pytest

from gym_app.components.hall_type_component import HallTypeComponent
from gym_app.exceptions import ResourceNotFoundException, DatabaseException


@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_fetch_all_hall_types(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallTypeComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.get_all_hall_types.return_value = []

    with pytest.raises(ResourceNotFoundException, match="Resource not found"):
        component.fetch_all_hall_types()

    mock_logger.log_error.assert_called_with("No hall types available.")


@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_fetch_hall_type_by_id(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallTypeComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.get_hall_type_by_id.return_value = None

    with pytest.raises(ResourceNotFoundException, match="Resource not found"):
        component.fetch_hall_type_by_id(999)

    mock_logger.log_error.assert_called_with("Hall type with ID 999 does not exist.")


@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_add_hall_type(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallTypeComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.create_hall_type.return_value = {'id': 1, 'code': 'CODE', 'name': 'Name'}

    data = {'code': 'CODE', 'name': 'Name'}
    result = component.add_hall_type(data)

    assert result == {'id': 1, 'code': 'CODE', 'name': 'Name'}
    mock_logger.log_info.assert_called_with(f"Adding new hall type with data: {data}")


@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_modify_hall_type(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallTypeComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.update_hall_type.return_value = {'id': 1, 'code': 'CODE', 'name': 'Updated Name'}

    data = {'name': 'Updated Name'}
    result = component.modify_hall_type(1, data)

    assert result == {'id': 1, 'code': 'CODE', 'name': 'Updated Name'}
    mock_logger.log_info.assert_called_with(f"Modifying hall type with ID 1 with data: {data}")


@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_remove_hall_type(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallTypeComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.delete_hall_type.return_value = True

    component.remove_hall_type(1)

    mock_repo_class.return_value.delete_hall_type.assert_called_with(1)
    mock_logger.log_info.assert_called_with("Removing hall type with ID 1")


@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_add_hall_type_database_exception(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallTypeComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.create_hall_type.side_effect = DatabaseException("Database error")

    with pytest.raises(DatabaseException, match="Database error"):
        component.add_hall_type({'code': 'CODE', 'name': 'Name'})

    mock_logger.log_error.assert_called_with("Error adding hall type: Database error")


@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_modify_hall_type_resource_not_found(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallTypeComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.update_hall_type.side_effect = ResourceNotFoundException("Resource not found")

    with pytest.raises(ResourceNotFoundException, match="Resource not found"):
        component.modify_hall_type(1, {'name': 'Updated Name'})

    mock_logger.log_error.assert_called_with("Resource not found")


@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_remove_hall_type_resource_not_found(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = HallTypeComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.delete_hall_type.side_effect = ResourceNotFoundException("Resource not found")

    with pytest.raises(ResourceNotFoundException, match="Resource not found"):
        component.remove_hall_type(1)

    mock_logger.log_error.assert_called_with("Resource not found")
