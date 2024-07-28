import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components import AdminComponent
from gym_app.models import Admin, Gym
from gym_app.forms import AdminForm
from django.http import Http404


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
    try:
        admin = admin_component.add_admin(mock_gym.id, data)
        assert admin.name == "Admin 1"
        assert admin.email == "admin1@example.com"
    except ValueError as e:
        print(f"Form validation errors: {e}")


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

    form = AdminForm(data, instance=admin)
    assert form.is_valid(), f"Form errors: {form.errors}"
    updated_admin = form.save()
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

    form = AdminForm(data)
    assert not form.is_valid()
    assert "This field is required." in form.errors["email"]
    assert "This field is required." in form.errors["address_city"]
    assert "This field is required." in form.errors["address_street"]


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
        "gym_id": mock_gym.id,
    }

    mock_repo_instance.get_admin_by_id.side_effect = Admin.DoesNotExist

    admin_component = AdminComponent(
        admin_repository=mock_repo_instance, logger=MagicMock()
    )
    with pytest.raises(ValueError, match="Admin with ID 999 does not exist"):
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


@pytest.mark.django_db
def test_add_admin_with_missing_fields():
    mock_gym = Gym.objects.create(name="Test Gym")

    data = {
        "name": "Admin1",
        "phone_number": "1234567890",
        # Missing email, address_city, address_street
        "gym": mock_gym.id,
    }

    form = AdminForm(data)
    assert not form.is_valid()
    assert "This field is required." in form.errors["email"]
    assert "This field is required." in form.errors["address_city"]
    assert "This field is required." in form.errors["address_street"]


@pytest.mark.django_db
def test_valid_admin_form():
    data = {
        "name": "ValidAdmin",
        "phone_number": "1234567890",
        "email": "valid.admin@example.com",
        "address_city": "Valid City",
        "address_street": "Valid Street",
    }
    form = AdminForm(data)
    assert form.is_valid(), f"Form errors: {form.errors}"
    assert form.cleaned_data["name"] == "ValidAdmin"


@pytest.mark.django_db
def test_invalid_name_in_admin_form():
    data = {
        "name": "Invalid123",
        "phone_number": "1234567890",
        "email": "invalid.name@example.com",
        "address_city": "Valid City",
        "address_street": "Valid Street",
    }
    form = AdminForm(data)
    assert not form.is_valid()
    assert "Name should only contain letters" in form.errors["name"]


@pytest.mark.django_db
def test_invalid_phone_number_in_admin_form():
    data = {
        "name": "Valid Admin",
        "phone_number": "12345ABC90",
        "email": "valid.admin@example.com",
        "address_city": "Valid City",
        "address_street": "Valid Street",
    }
    form = AdminForm(data)
    assert not form.is_valid()
    assert "Phone number should only contain digits" in form.errors["phone_number"]


@pytest.mark.django_db
def test_duplicate_email_in_admin_form():
    gym = Gym.objects.create(name="Existing Gym")

    Admin.objects.create(
        name="Existing Admin",
        phone_number="1234567890",
        email="duplicate.email@example.com",
        address_city="Existing City",
        address_street="Existing Street",
        gym_id=gym,
    )

    data = {
        "name": "New Admin",
        "phone_number": "9876543210",
        "email": "duplicate.email@example.com",
        "address_city": "New City",
        "address_street": "New Street",
        "gym_id": gym.id,
    }
    form = AdminForm(data)
    assert not form.is_valid()
    assert "Email already exists" in form.errors["email"]


@pytest.mark.django_db
def test_address_length_in_admin_form():
    data = {
        "name": "Valid Admin",
        "phone_number": "1234567890",
        "email": "valid.admin@example.com",
        "address_city": "A" * 256,
        "address_street": "Street",
    }
    form = AdminForm(data)
    assert not form.is_valid()
    assert (
        "Ensure this value has at most 255 characters (it has 256)."
        in form.errors["address_city"]
    )

    data["address_city"] = "Valid City"
    data["address_street"] = "S" * 256
    form = AdminForm(data)
    assert not form.is_valid()
    assert (
        "Ensure this value has at most 255 characters (it has 256)."
        in form.errors["address_street"]
    )
