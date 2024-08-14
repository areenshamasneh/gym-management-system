from unittest.mock import patch, MagicMock

import pytest  # type: ignore
from rest_framework.exceptions import NotFound, APIException  # type: ignore

from gym_app.components import EmployeeComponent
from gym_app.exceptions import ResourceNotFoundException
from gym_app.models import Employee, Gym


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_fetch_all_employees(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    mock_employee1 = MagicMock(spec=Employee)
    mock_employee1.name = "John Doe"
    mock_employee1.email = "john@example.com"
    mock_employee1.positions = "Trainer, Cleaner"
    mock_employee1.gym = MagicMock(spec=Gym)
    mock_employee1.gym.id = 1

    mock_employee2 = MagicMock(spec=Employee)
    mock_employee2.name = "Jane Smith"
    mock_employee2.email = "jane@example.com"
    mock_employee2.positions = "System Worker"
    mock_employee2.gym = MagicMock(spec=Gym)
    mock_employee2.gym.id = 1

    mock_repo.get_all_employees.return_value = [mock_employee1, mock_employee2]

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    employees = component.fetch_all_employees(1)

    assert len(employees) == 2
    assert employees[0].name == "John Doe"
    assert employees[1].name == "Jane Smith"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_fetch_employee_by_id(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    mock_employee = MagicMock(spec=Employee)
    mock_employee.name = "John Doe"
    mock_employee.email = "john@example.com"
    mock_employee.positions = "Trainer, Cleaner"
    mock_employee.gym = MagicMock(spec=Gym)
    mock_employee.gym.id = 1

    mock_repo.get_employee_by_id.return_value = mock_employee

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    employee = component.fetch_employee_by_id(1, 1)

    assert employee.name == "John Doe"
    assert employee.email == "john@example.com"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_add_employee(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "positions": "cleaner, trainer",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "123 Street",
    }

    mock_employee = MagicMock(spec=Employee)
    mock_employee.name = data["name"]
    mock_employee.email = data["email"]
    mock_employee.positions = data["positions"]
    mock_employee.gym = MagicMock(spec=Gym)
    mock_employee.gym.id = data["gym_id"]

    mock_repo.create_employee.return_value = mock_employee

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    added_employee = component.add_employee(1, data)

    assert added_employee.name == "John Doe"
    assert added_employee.email == "john.doe@example.com"
    assert "cleaner" in added_employee.positions
    assert "trainer" in added_employee.positions


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_modify_employee(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    mock_employee = MagicMock(spec=Employee)
    mock_employee.name = "John Updated"
    mock_employee.email = "john.updated@example.com"
    mock_employee.positions = "Trainer"
    mock_employee.gym = MagicMock(spec=Gym)
    mock_employee.gym.id = 1

    mock_repo.update_employee.return_value = mock_employee

    data = {
        "name": "John Updated",
        "email": "john.updated@example.com",
        "positions": "Trainer",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "456 Avenue",
    }

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    employee = component.modify_employee(1, 1, data)

    assert employee.name == "John Updated"
    assert employee.email == "john.updated@example.com"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_remove_employee(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    component.remove_employee(1, 1)

    assert mock_repo.delete_employee.called
    assert mock_repo.delete_employee.call_count == 1


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_add_employee_with_missing_fields(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    data = {
        "name": "John Doe",
        "email": "john@example.com",
        # Missing positions, gym_id, address_city, address_street
    }

    mock_repo.create_employee.side_effect = APIException("Invalid data")

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    with pytest.raises(APIException, match="Error adding employee"):
        component.add_employee(1, data)


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_modify_employee_non_existent(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    mock_repo.update_employee.side_effect = APIException("Employee not found")

    data = {
        "name": "Non Existent Employee",
        "email": "nonexistent@example.com",
        "positions": "None",
        "gym_id": 1,
        "address_city": "Nowhere",
        "address_street": "No Street",
    }

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    with pytest.raises(APIException, match="Error modifying employee"):
        component.modify_employee(1, 999, data)


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_remove_employee_non_existent(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    mock_repo.delete_employee.side_effect = APIException("Employee not found")

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    with pytest.raises(APIException, match="Error removing employee"):
        component.remove_employee(1, 999)


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_fetch_employee_by_id_non_existent(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    mock_repo.get_employee_by_id.side_effect = Employee.DoesNotExist

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    with pytest.raises(
            ResourceNotFoundException, match="Employee with ID 999 does not exist"
    ):
        component.fetch_employee_by_id(1, 999)


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_add_employee_invalid_data(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    data = {
        "name": "John Doe",
        "email": "invalid_email_format",
        "positions": "Trainer, Cleaner",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "123 Street",
    }

    mock_repo.create_employee.side_effect = APIException("Invalid data")

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    with pytest.raises(APIException, match="Error adding employee"):
        component.add_employee(1, data)


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_modify_employee_invalid_data(mock_logger, mock_repo):
    mock_logger_instance = MagicMock()
    mock_logger.return_value = mock_logger_instance

    data = {
        "name": "John Doe",
        "email": "invalid_email_format",
        "positions": "Trainer, Cleaner",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "123 Street",
    }

    mock_repo.update_employee.side_effect = APIException("Invalid data")

    component = EmployeeComponent(
        employee_repository=mock_repo, logger=mock_logger_instance
    )
    with pytest.raises(APIException, match="Error modifying employee"):
        component.modify_employee(1, 1, data)
