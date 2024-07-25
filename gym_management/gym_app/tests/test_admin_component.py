import pytest # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components.admin_component import AdminComponent
from gym_app.models import Admin, Gym


@pytest.mark.django_db
@patch("gym_app.components.admin_component.AdminRepository")
def test_fetch_all_admins(mock_repo):

    mock_admin1 = MagicMock(spec=Admin)
    mock_admin1.name = "Admin 1"
    mock_admin1.phone_number = "1234567890"
    mock_admin1.email = "admin1@example.com"
    mock_admin1.address_city = "City 1"
    mock_admin1.address_street = "Street 1"

    mock_admin2 = MagicMock(spec=Admin)
    mock_admin2.name = "Admin 2"
    mock_admin2.phone_number = "0987654321"
    mock_admin2.email = "admin2@example.com"
    mock_admin2.address_city = "City 2"
    mock_admin2.address_street = "Street 2"

    mock_repo.get_all_admins.return_value = [mock_admin1, mock_admin2]

    admins = AdminComponent.fetch_all_admins()

    assert len(admins) == 2
    assert admins[0].name == "Admin 1"
    assert admins[1].name == "Admin 2"


@pytest.mark.django_db
@patch("gym_app.components.admin_component.AdminRepository")
def test_fetch_admin_by_id(mock_repo):

    mock_admin = MagicMock(spec=Admin)
    mock_admin.name = "Admin 1"
    mock_admin.phone_number = "1234567890"
    mock_admin.email = "admin1@example.com"
    mock_admin.address_city = "City 1"
    mock_admin.address_street = "Street 1"

    mock_repo.get_admin_by_id.return_value = mock_admin

    admin = AdminComponent.fetch_admin_by_id(1)

    assert admin.name == "Admin 1"
    assert admin.email == "admin1@example.com"


@pytest.mark.django_db
@patch("gym_app.components.admin_component.AdminRepository")
def test_add_admin(mock_repo):

    mock_admin = MagicMock(spec=Admin)
    mock_admin.name = "Admin 1"
    mock_admin.phone_number = "1234567890"
    mock_admin.email = "admin1@example.com"
    mock_admin.address_city = "City 1"
    mock_admin.address_street = "Street 1"

    mock_repo.create_admin.return_value = mock_admin

    data = {
        "name": "Admin 1",
        "phone_number": "1234567890",
        "email": "admin1@example.com",
        "gym_id": 1,
        "address_city": "City 1",
        "address_street": "Street 1",
    }

    admin = AdminComponent.add_admin(data)

    assert admin.name == "Admin 1"
    assert admin.email == "admin1@example.com"


@pytest.mark.django_db
@patch("gym_app.components.admin_component.AdminRepository")
def test_modify_admin(mock_repo):

    mock_admin = MagicMock(spec=Admin)
    mock_admin.name = "Admin Updated"
    mock_admin.phone_number = "1234567890"
    mock_admin.email = "admin1@example.com"
    mock_admin.address_city = "City 1"
    mock_admin.address_street = "Street 1"

    mock_repo.update_admin.return_value = mock_admin

    data = {
        "name": "Admin Updated",
        "phone_number": "1234567890",
        "email": "admin1@example.com",
        "gym_id": 1,
        "address_city": "City 1",
        "address_street": "Street 1",
    }

    admin = AdminComponent.modify_admin(1, data)

    assert admin.name == "Admin Updated"
    assert admin.email == "admin1@example.com"


@pytest.mark.django_db
@patch("gym_app.components.admin_component.AdminRepository")
def test_remove_admin(mock_repo):

    AdminComponent.remove_admin(1)

    assert mock_repo.delete_admin.called
    assert mock_repo.delete_admin.call_count == 1
