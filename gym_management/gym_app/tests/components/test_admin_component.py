import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from django.http import Http404
from gym_app.components import AdminComponent
from gym_app.models import Admin, Gym
from gym_app.serializers import AdminSerializer
from gym_app.exceptions import ResourceNotFoundException


@pytest.mark.django_db
@patch("gym_app.components.admin_component.AdminRepository")
def test_fetch_all_admins(mock_repo):
    mock_gym_id = 1

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

    admin_component = AdminComponent(admin_repository=mock_repo, logger=MagicMock())
    admins = admin_component.fetch_all_admins(mock_gym_id)

    assert len(admins) == 2
    assert admins[0].name == "Admin 1"
    assert admins[1].name == "Admin 2"


@pytest.mark.django_db
@patch("gym_app.components.admin_component.AdminRepository")
def test_fetch_admin_by_id(mock_repo):
    mock_gym_id = 1
    mock_admin_id = 1

    mock_admin = MagicMock(spec=Admin)
    mock_admin.name = "Admin 1"
    mock_admin.phone_number = "1234567890"
    mock_admin.email = "admin1@example.com"
    mock_admin.address_city = "City 1"
    mock_admin.address_street = "Street 1"

    mock_repo.get_admin_by_id.return_value = mock_admin

    admin_component = AdminComponent(admin_repository=mock_repo, logger=MagicMock())
    admin = admin_component.fetch_admin_by_id(mock_gym_id, mock_admin_id)

    assert admin.name == "Admin 1"
    assert admin.email == "admin1@example.com"


@pytest.mark.django_db
@patch("gym_app.components.admin_component.AdminRepository")
def test_add_admin(mock_repo):
    mock_repo_instance = mock_repo.return_value

    mock_gym = Gym.objects.create(name="Test Gym")

    mock_admin = MagicMock(spec=Admin)
    mock_admin.name = "Admin 1"
    mock_admin.phone_number = "1234567890"
    mock_admin.email = "admin1@example.com"
    mock_admin.address_city = "City 1"
    mock_admin.address_street = "Street 1"

    mock_repo_instance.create_admin.return_value = mock_admin

    data = {
        "name": "Admin 1",
        "phone_number": "1234567890",
        "email": "admin1@example.com",
        "address_city": "City 1",
        "address_street": "Street 1",
        "gym_id": mock_gym.id,
    }

    admin_component = AdminComponent(
        admin_repository=mock_repo_instance, logger=MagicMock()
    )
    admin = admin_component.add_admin(mock_gym.id, data)
    assert admin.name == "Admin 1"
    assert admin.email == "admin1@example.com"


@pytest.mark.django_db
def test_modify_admin():
    mock_gym = Gym.objects.create(name="Test Gym")

    admin = Admin.objects.create(
        name="OldAdminName",
        phone_number="1234567890",
        email="oldadmin@example.com",
        address_city="OldCity",
        address_street="OldStreet",
        gym_id=mock_gym,
    )

    data = {
        "name": "UpdatedAdminName",
        "phone_number": "1234567890",
        "email": "updatedadmin@example.com",
        "address_city": "UpdatedCity",
        "address_street": "UpdatedStreet",
        "gym_id": mock_gym.id,
    }

    serializer = AdminSerializer(instance=admin, data=data)
    assert serializer.is_valid(), f"Serializer errors: {serializer.errors}"
    updated_admin = serializer.save()
    assert updated_admin.name == "UpdatedAdminName"
    assert updated_admin.email == "updatedadmin@example.com"


@pytest.mark.django_db
def test_add_admin_with_missing_fields():
    mock_gym = Gym.objects.create(name="Test Gym")

    data = {
        "name": "Admin1",
        "phone_number": "1234567890",
        "gym_id": mock_gym.id,
    }

    serializer = AdminSerializer(data=data)
    assert not serializer.is_valid()
    assert "This field is required." in serializer.errors["email"]
    assert "This field is required." in serializer.errors["address_city"]
    assert "This field is required." in serializer.errors["address_street"]


@pytest.mark.django_db
@patch("gym_app.components.admin_component.AdminRepository")
def test_modify_admin_non_existent(mock_repo):
    mock_repo_instance = mock_repo.return_value
    mock_gym = Gym.objects.create(name="Test Gym")
    non_existent_admin_id = 999
    data = {
        "name": "NonExistentAdmin",
        "phone_number": "0000000000",
        "email": "nonexistent@example.com",
        "address_city": "Nowhere",
        "address_street": "No Street",
    }

    mock_repo_instance.get_admin_by_id.side_effect = Http404(
        f"Admin with ID {non_existent_admin_id} not found for gym_id {mock_gym.id}"
    )

    admin_component = AdminComponent(
        admin_repository=mock_repo_instance, logger=MagicMock()
    )

    with pytest.raises(
        ResourceNotFoundException,
        match=f"Admin with ID {non_existent_admin_id} not found",
    ):
        admin_component.modify_admin(mock_gym.id, non_existent_admin_id, data)


@pytest.mark.django_db
@patch("gym_app.components.admin_component.AdminRepository")
def test_remove_admin(mock_repo):
    mock_gym_id = 1
    mock_admin_id = 1

    admin_component = AdminComponent(admin_repository=mock_repo, logger=MagicMock())
    admin_component.remove_admin(mock_gym_id, mock_admin_id)

    assert mock_repo.delete_admin.called
    assert mock_repo.delete_admin.call_count == 1
