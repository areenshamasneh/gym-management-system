import pytest # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components.hall_type_component import HallTypeComponent
from gym_app.models import HallType


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
def test_fetch_all_hall_types(mock_repo):

    mock_hall_type1 = MagicMock(spec=HallType)
    mock_hall_type1.id = 1
    mock_hall_type1.type = "sauna"
    mock_hall_type1.type_description = "Relaxing sauna"

    mock_hall_type2 = MagicMock(spec=HallType)
    mock_hall_type2.id = 2
    mock_hall_type2.type = "training"
    mock_hall_type2.type_description = "Fitness training"

    mock_repo.get_all_hall_types.return_value = [mock_hall_type1, mock_hall_type2]

    hall_types = HallTypeComponent.fetch_all_hall_types()

    assert len(hall_types) == 2
    assert hall_types[0].type == "sauna"
    assert hall_types[1].type == "training"


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
def test_fetch_hall_type_by_id(mock_repo):

    mock_hall_type = MagicMock(spec=HallType)
    mock_hall_type.id = 1
    mock_hall_type.type = "sauna"
    mock_hall_type.type_description = "Relaxing sauna"

    mock_repo.get_hall_type_by_id.return_value = mock_hall_type

    hall_type = HallTypeComponent.fetch_hall_type_by_id(1)

    assert hall_type.type == "sauna"
    assert hall_type.type_description == "Relaxing sauna"


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
def test_add_hall_type(mock_repo):

    mock_hall_type = MagicMock(spec=HallType)
    mock_hall_type.id = 1
    mock_hall_type.type = "sauna"
    mock_hall_type.type_description = "Relaxing sauna"

    mock_repo.create_hall_type.return_value = mock_hall_type

    data = {"type": "sauna", "type_description": "Relaxing sauna"}

    hall_type = HallTypeComponent.add_hall_type(data)

    assert hall_type.type == "sauna"
    assert hall_type.type_description == "Relaxing sauna"


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
def test_modify_hall_type(mock_repo):

    mock_hall_type = MagicMock(spec=HallType)
    mock_hall_type.id = 1
    mock_hall_type.type = "sauna"
    mock_hall_type.type_description = "Updated description"

    mock_repo.update_hall_type.return_value = mock_hall_type

    data = {"type_description": "Updated description"}

    hall_type = HallTypeComponent.modify_hall_type(1, data)

    assert hall_type.type_description == "Updated description"


@pytest.mark.django_db
@patch("gym_app.components.hall_type_component.HallTypeRepository")
def test_remove_hall_type(mock_repo):

    HallTypeComponent.remove_hall_type(1)

    assert mock_repo.delete_hall_type.called
    assert mock_repo.delete_hall_type.call_count == 1
