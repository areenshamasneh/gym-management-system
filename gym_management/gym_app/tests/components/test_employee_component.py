import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components import EmployeeComponent
from gym_app.models import Employee, Gym
from gym_app.logging import SimpleLogger


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_fetch_all_employees(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
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
    mock_employee2.gym.id = 2

    mock_repo.get_all_employees.return_value = [mock_employee1, mock_employee2]

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    employees = component.fetch_all_employees(1)

    assert len(employees) == 2
    assert employees[0].name == "John Doe"
    assert employees[1].name == "Jane Smith"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_fetch_employee_by_id(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
    mock_logger.return_value = mock_logger_instance

    mock_employee = MagicMock(spec=Employee)
    mock_employee.name = "John Doe"
    mock_employee.email = "john@example.com"
    mock_employee.positions = "Trainer, Cleaner"
    mock_employee.gym = MagicMock(spec=Gym)
    mock_employee.gym.id = 1

    mock_repo.get_employee_by_id.return_value = mock_employee

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    employee = component.fetch_employee_by_id(1, 1)

    assert employee.name == "John Doe"
    assert employee.email == "john@example.com"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_add_employee(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
    mock_logger.return_value = mock_logger_instance

    mock_employee = MagicMock(spec=Employee)
    mock_employee.name = "John Doe"
    mock_employee.email = "john@example.com"
    mock_employee.positions = "Trainer, Cleaner"
    mock_employee.gym = MagicMock(spec=Gym)
    mock_employee.gym.id = 1

    mock_repo.create_employee.return_value = mock_employee

    data = {
        "name": "John Doe",
        "email": "john@example.com",
        "positions": "Trainer, Cleaner",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "123 Street",
    }

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    employee = component.add_employee(1, data)

    assert employee.name == "John Doe"
    assert employee.email == "john@example.com"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_modify_employee(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
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

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    employee = component.modify_employee(1, 1, data)

    assert employee.name == "John Updated"
    assert employee.email == "john.updated@example.com"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_remove_employee(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
    mock_logger.return_value = mock_logger_instance

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    component.remove_employee(1, 1)

    assert mock_repo.delete_employee.called
    assert mock_repo.delete_employee.call_count == 1


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_add_employee_with_missing_fields(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
    mock_logger.return_value = mock_logger_instance

    mock_repo.create_employee.side_effect = KeyError("Missing required field")

    data = {
        "name": "John Doe",
        "email": "john@example.com",
        # Missing positions, gym_id, address_city, address_street
    }

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    with pytest.raises(KeyError, match="Missing required field"):
        component.add_employee(1, data)


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_modify_employee_non_existent(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
    mock_logger.return_value = mock_logger_instance

    mock_repo.update_employee.side_effect = Employee.DoesNotExist

    data = {
        "name": "Non Existent Employee",
        "email": "nonexistent@example.com",
        "positions": "None",
        "gym_id": 1,
        "address_city": "Nowhere",
        "address_street": "No Street",
    }

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    with pytest.raises(Employee.DoesNotExist):
        component.modify_employee(1, 999, data)


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_remove_employee_non_existent(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
    mock_logger.return_value = mock_logger_instance

    mock_repo.delete_employee.side_effect = Employee.DoesNotExist

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    with pytest.raises(Employee.DoesNotExist):
        component.remove_employee(1, 999)


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_fetch_employee_by_id_non_existent(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
    mock_logger.return_value = mock_logger_instance

    mock_repo.get_employee_by_id.side_effect = Employee.DoesNotExist

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    with pytest.raises(Employee.DoesNotExist):
        component.fetch_employee_by_id(1, 999)


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_add_employee_invalid_data(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
    mock_logger.return_value = mock_logger_instance

    mock_repo.create_employee.side_effect = ValueError("Invalid data")

    data = {
        "name": "John Doe",
        "email": "invalid_email_format",
        "positions": "Trainer, Cleaner",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "123 Street",
    }

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    with pytest.raises(ValueError, match="Invalid data"):
        component.add_employee(1, data)


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
@patch("gym_app.logging.SimpleLogger")
def test_modify_employee_invalid_data(mock_logger, mock_repo):
    mock_logger_instance = MagicMock(spec=SimpleLogger)
    mock_logger.return_value = mock_logger_instance

    mock_repo.update_employee.side_effect = ValueError("Invalid data")

    data = {
        "name": "John Updated",
        "email": "invalid_email_format",
        "positions": "Trainer",
        "gym_id": 1,
        "address_city": "New York",
        "address_street": "456 Avenue",
    }

    component = EmployeeComponent(mock_repo, mock_logger_instance)
    with pytest.raises(ValueError, match="Invalid data"):
        component.modify_employee(1, 1, data)
