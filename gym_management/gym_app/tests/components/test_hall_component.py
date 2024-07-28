import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components.hall_component import HallComponent
from gym_app.models import Hall, HallType, Gym


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
def test_fetch_all_halls(mock_repo):
    mock_hall1 = MagicMock(spec=Hall)
    mock_hall1.name = "Hall 1"
    mock_hall1.users_capacity = 20
    mock_hall1.hall_type = MagicMock(spec=HallType)
    mock_hall1.hall_type.id = 1
    mock_hall1.gym = MagicMock(spec=Gym)
    mock_hall1.gym.id = 1

    mock_hall2 = MagicMock(spec=Hall)
    mock_hall2.name = "Hall 2"
    mock_hall2.users_capacity = 30
    mock_hall2.hall_type = MagicMock(spec=HallType)
    mock_hall2.hall_type.id = 2
    mock_hall2.gym = MagicMock(spec=Gym)
    mock_hall2.gym.id = 2

    mock_repo.get_all_halls.return_value = [mock_hall1, mock_hall2]

    halls = HallComponent.fetch_all_halls()

    assert len(halls) == 2
    assert halls[0].name == "Hall 1"
    assert halls[1].name == "Hall 2"


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
def test_fetch_hall_by_id(mock_repo):
    mock_hall = MagicMock(spec=Hall)
    mock_hall.name = "Hall 1"
    mock_hall.users_capacity = 20
    mock_hall.hall_type = MagicMock(spec=HallType)
    mock_hall.hall_type.id = 1
    mock_hall.gym = MagicMock(spec=Gym)
    mock_hall.gym.id = 1

    mock_repo.get_hall_by_id.return_value = mock_hall

    hall = HallComponent.fetch_hall_by_id(1)

    assert hall.name == "Hall 1"
    assert hall.users_capacity == 20


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
def test_add_hall(mock_repo):
    mock_hall = MagicMock(spec=Hall)
    mock_hall.name = "Hall 1"
    mock_hall.users_capacity = 20
    mock_hall.hall_type = MagicMock(spec=HallType)
    mock_hall.hall_type.id = 1
    mock_hall.gym = MagicMock(spec=Gym)
    mock_hall.gym.id = 1

    mock_repo.create_hall.return_value = mock_hall

    data = {"name": "Hall 1", "users_capacity": 20, "hall_type_id": 1, "gym_id": 1}
    hall = HallComponent.add_hall(data)
    assert hall.name == "Hall 1"
    assert hall.users_capacity == 20


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
def test_modify_hall(mock_repo):
    mock_hall = MagicMock(spec=Hall)
    mock_hall.name = "Hall Updated"
    mock_hall.users_capacity = 25
    mock_hall.hall_type = MagicMock(spec=HallType)
    mock_hall.hall_type.id = 1
    mock_hall.gym = MagicMock(spec=Gym)
    mock_hall.gym.id = 1

    mock_repo.update_hall.return_value = mock_hall

    data = {
        "name": "Hall Updated",
        "users_capacity": 25,
        "hall_type_id": 1,
        "gym_id": 1,
    }
    hall = HallComponent.modify_hall(1, data)

    assert hall.name == "Hall Updated"
    assert hall.users_capacity == 25


@pytest.mark.django_db
@patch("gym_app.components.hall_component.HallRepository")
def test_remove_hall(mock_repo):
    HallComponent.remove_hall(1)

    assert mock_repo.delete_hall.called
    assert mock_repo.delete_hall.call_count == 1
