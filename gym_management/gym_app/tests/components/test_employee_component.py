from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import NoResultFound

from gym_app.components import EmployeeComponent
from gym_app.exceptions import ResourceNotFoundException, InvalidInputException
from gym_app.repositories import EmployeeRepository


@pytest.fixture
def mock_employee_repository():
    return MagicMock(spec=EmployeeRepository)


@pytest.fixture
def mock_logger():
    return MagicMock()


@pytest.fixture
def employee_component(mock_employee_repository, mock_logger):
    return EmployeeComponent(employee_repository=mock_employee_repository, logger=mock_logger)


def test_fetch_all_employees(employee_component, mock_employee_repository, mock_logger):
    mock_employee1 = MagicMock()
    mock_employee1.name = "John Doe"
    mock_employee1.email = "john@example.com"
    mock_employee1.positions = "Trainer, Cleaner"

    mock_employee2 = MagicMock()
    mock_employee2.name = "Jane Smith"
    mock_employee2.email = "jane@example.com"
    mock_employee2.positions = "System Worker"

    mock_employee_repository.get_all_employees.return_value = [mock_employee1, mock_employee2]

    employees = employee_component.fetch_all_employees(1)

    assert len(employees) == 2
    assert employees[0].name == "John Doe"
    assert employees[1].name == "Jane Smith"


def test_fetch_employee_by_id(employee_component, mock_employee_repository, mock_logger):
    mock_employee = MagicMock()
    mock_employee.name = "John Doe"
    mock_employee.email = "john@example.com"
    mock_employee.positions = "Trainer, Cleaner"

    mock_employee_repository.get_employee_by_id.return_value = mock_employee

    employee = employee_component.fetch_employee_by_id(1, 1)

    assert employee.name == "John Doe"
    assert employee.email == "john@example.com"


def test_add_employee(employee_component, mock_employee_repository, mock_logger):
    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "positions": "cleaner, trainer",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "123 Street",
    }

    mock_employee = MagicMock()
    mock_employee.name = data["name"]
    mock_employee.email = data["email"]
    mock_employee.positions = data["positions"]

    mock_employee_repository.create_employee.return_value = mock_employee

    added_employee = employee_component.add_employee(1, data)

    assert added_employee.name == "John Doe"
    assert added_employee.email == "john.doe@example.com"
    assert "cleaner" in added_employee.positions
    assert "trainer" in added_employee.positions


def test_modify_employee(employee_component, mock_employee_repository, mock_logger):
    mock_employee = MagicMock()
    mock_employee.name = "John Updated"
    mock_employee.email = "john.updated@example.com"
    mock_employee.positions = "Trainer"

    mock_employee_repository.update_employee.return_value = mock_employee

    data = {
        "name": "John Updated",
        "email": "john.updated@example.com",
        "positions": "Trainer",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "456 Avenue",
    }

    employee = employee_component.modify_employee(1, 1, data)

    assert employee.name == "John Updated"
    assert employee.email == "john.updated@example.com"


def test_remove_employee(employee_component, mock_employee_repository, mock_logger):
    employee_component.remove_employee(1, 1)

    assert mock_employee_repository.delete_employee.called
    assert mock_employee_repository.delete_employee.call_count == 1


def test_add_employee_with_missing_fields(employee_component, mock_employee_repository, mock_logger):
    data = {
        "name": "John Doe",
        "email": "john@example.com",
    }

    mock_employee_repository.create_employee.side_effect = InvalidInputException("Invalid data")

    with pytest.raises(InvalidInputException, match="Error adding employee"):
        employee_component.add_employee(1, data)


def test_remove_employee_non_existent(mock_employee_repository, mock_logger):
    mock_employee_repository.delete_employee.side_effect = NoResultFound("Employee not found")

    employee_component = EmployeeComponent(employee_repository=mock_employee_repository, logger=mock_logger)

    with pytest.raises(ResourceNotFoundException, match="Employee with ID 999 does not exist"):
        employee_component.remove_employee(1, 999)

    mock_logger.log_info.assert_called_with("Removing employee ID 999 for gym_id: 1")
    mock_logger.log_error.assert_called_with("Employee with ID 999 does not exist for gym_id: 1")


def test_fetch_employee_by_id_non_existent(employee_component, mock_employee_repository, mock_logger):
    mock_employee_repository.get_employee_by_id.return_value = None

    expected_error_message = "Employee with ID 999 does not exist for gym_id: 1"

    with pytest.raises(ResourceNotFoundException, match=expected_error_message):
        employee_component.fetch_employee_by_id(1, 999)

    mock_logger.log_info.assert_called_with("Fetching employee with ID 999")
    mock_logger.log_error.assert_called_with(f"Resource not found: Employee with ID 999 does not exist for gym_id: 1")


def test_add_employee_invalid_data(employee_component, mock_employee_repository, mock_logger):
    data = {
        "name": "John Doe",
        "email": "invalid_email_format",
        "positions": "Trainer, Cleaner",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "123 Street",
    }

    mock_employee_repository.create_employee.side_effect = InvalidInputException("Invalid data")

    with pytest.raises(InvalidInputException, match="Error adding employee"):
        employee_component.add_employee(1, data)


def test_modify_employee_invalid_data(employee_component, mock_employee_repository, mock_logger):
    data = {
        "name": "John Doe",
        "email": "invalid_email_format",
        "positions": "Trainer, Cleaner",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "123 Street",
    }

    mock_employee_repository.update_employee.side_effect = InvalidInputException("Invalid data")

    with pytest.raises(InvalidInputException, match="Error modifying employee"):
        employee_component.modify_employee(1, 1, data)
