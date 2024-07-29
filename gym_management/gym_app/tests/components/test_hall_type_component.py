import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components import HallTypeComponent
from gym_app.models import HallType
from gym_app.logging import SimpleLogger


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_fetch_all_hall_types(mock_logger, mock_repo):
    mock_hall_type1 = MagicMock(spec=HallType)
    mock_hall_type1.id = 1
    mock_hall_type1.type = "sauna"
    mock_hall_type1.type_description = "Relaxing sauna"

    mock_hall_type2 = MagicMock(spec=HallType)
    mock_hall_type2.id = 2
    mock_hall_type2.type = "training"
    mock_hall_type2.type_description = "Fitness training"

    mock_repo.get_all_hall_types.return_value = [mock_hall_type1, mock_hall_type2]

    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)
    hall_types = component.fetch_all_hall_types()

    assert len(hall_types) == 2
    assert hall_types[0].type == "sauna"
    assert hall_types[1].type == "training"
    mock_logger.log.assert_called_with("Fetching all hall types")


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_fetch_hall_type_by_id(mock_logger, mock_repo):
    mock_hall_type = MagicMock(spec=HallType)
    mock_hall_type.id = 1
    mock_hall_type.type = "sauna"
    mock_hall_type.type_description = "Relaxing sauna"

    mock_repo.get_hall_type_by_id.return_value = mock_hall_type

    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)
    hall_type = component.fetch_hall_type_by_id(1)

    assert hall_type.type == "sauna"
    assert hall_type.type_description == "Relaxing sauna"
    mock_logger.log.assert_called_with("Fetching hall type with ID 1")


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_add_hall_type(mock_logger, mock_repo):
    mock_hall_type = MagicMock(spec=HallType)
    mock_hall_type.id = 1
    mock_hall_type.type = "sauna"
    mock_hall_type.type_description = "Relaxing sauna"

    mock_repo.create_hall_type.return_value = mock_hall_type

    data = {"type": "sauna", "type_description": "Relaxing sauna"}

    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)
    hall_type = component.add_hall_type(data)

    assert hall_type.type == "sauna"
    assert hall_type.type_description == "Relaxing sauna"
    mock_logger.log.assert_called_with(f"Adding new hall type with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_modify_hall_type(mock_logger, mock_repo):
    mock_hall_type = MagicMock(spec=HallType)
    mock_hall_type.id = 1
    mock_hall_type.type = "sauna"
    mock_hall_type.type_description = "Updated description"

    mock_repo.update_hall_type.return_value = mock_hall_type

    data = {"type_description": "Updated description"}

    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)
    hall_type = component.modify_hall_type(1, data)

    assert hall_type.type_description == "Updated description"
    mock_logger.log.assert_called_with(
        f"Modifying hall type with ID 1 with data: {data}"
    )


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_remove_hall_type(mock_logger, mock_repo):
    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)
    component.remove_hall_type(1)

    assert mock_repo.delete_hall_type.called
    assert mock_repo.delete_hall_type.call_count == 1
    mock_logger.log.assert_called_with("Removing hall type with ID 1")


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_add_hall_type_with_missing_fields(mock_logger, mock_repo):
    mock_repo.create_hall_type.side_effect = KeyError("Missing required field")

    data = {"type": "sauna"}

    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)

    with pytest.raises(KeyError, match="Missing required field"):
        component.add_hall_type(data)
    mock_logger.log.assert_called_with(f"Adding new hall type with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_modify_hall_type_non_existent(mock_logger, mock_repo):
    mock_repo.update_hall_type.side_effect = HallType.DoesNotExist

    data = {"type_description": "Non Existent HallType"}

    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)

    with pytest.raises(HallType.DoesNotExist):
        component.modify_hall_type(999, data)
    mock_logger.log.assert_called_with(
        f"Modifying hall type with ID 999 with data: {data}"
    )


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_remove_hall_type_non_existent(mock_logger, mock_repo):
    mock_repo.delete_hall_type.side_effect = HallType.DoesNotExist

    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)

    with pytest.raises(HallType.DoesNotExist):
        component.remove_hall_type(999)
    mock_logger.log.assert_called_with("Removing hall type with ID 999")


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_fetch_hall_type_by_id_non_existent(mock_logger, mock_repo):
    mock_repo.get_hall_type_by_id.side_effect = HallType.DoesNotExist

    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)

    with pytest.raises(HallType.DoesNotExist):
        component.fetch_hall_type_by_id(999)
    mock_logger.log.assert_called_with("Fetching hall type with ID 999")


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_add_hall_type_invalid_data(mock_logger, mock_repo):
    mock_repo.create_hall_type.side_effect = ValueError("Invalid data")

    data = {
        "type": "",
        "type_description": "Invalid HallType",
    }

    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)

    with pytest.raises(ValueError, match="Invalid data"):
        component.add_hall_type(data)
    mock_logger.log.assert_called_with(f"Adding new hall type with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
@patch("gym_app.components.hall_type_component.SimpleLogger")
def test_add_hall_type_invalid_data(mock_logger, mock_repo):
    mock_repo.create_hall_type.side_effect = ValueError("Invalid data")

    data = {
        "type": "",
        "type_description": "Invalid HallType",
    }

    component = HallTypeComponent(repo=mock_repo, logger=mock_logger)

    with pytest.raises(ValueError, match="Invalid data"):
        component.add_hall_type(data)
    mock_logger.log.assert_called_with("Error adding hall type: Invalid data")
