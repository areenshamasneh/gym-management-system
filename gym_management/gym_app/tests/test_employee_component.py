import pytest # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components.employee_component import EmployeeComponent
from gym_app.models import Employee, Gym


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
def test_fetch_all_employees(mock_repo):

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

    employees = EmployeeComponent.fetch_all_employees()

    assert len(employees) == 2
    assert employees[0].name == "John Doe"
    assert employees[1].name == "Jane Smith"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
def test_fetch_employee_by_id(mock_repo):

    mock_employee = MagicMock(spec=Employee)
    mock_employee.name = "John Doe"
    mock_employee.email = "john@example.com"
    mock_employee.positions = "Trainer, Cleaner"
    mock_employee.gym = MagicMock(spec=Gym)
    mock_employee.gym.id = 1

    mock_repo.get_employee_by_id.return_value = mock_employee

    employee = EmployeeComponent.fetch_employee_by_id(1)

    assert employee.name == "John Doe"
    assert employee.email == "john@example.com"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
def test_add_employee(mock_repo):

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

    employee = EmployeeComponent.add_employee(data)

    assert employee.name == "John Doe"
    assert employee.email == "john@example.com"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
def test_modify_employee(mock_repo):

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

    employee = EmployeeComponent.modify_employee(1, data)

    assert employee.name == "John Updated"
    assert employee.email == "john.updated@example.com"


@pytest.mark.django_db
@patch("gym_app.components.employee_component.EmployeeRepository")
def test_remove_employee(mock_repo):

    EmployeeComponent.remove_employee(1)

    assert mock_repo.delete_employee.called
    assert mock_repo.delete_employee.call_count == 1
