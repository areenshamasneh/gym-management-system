import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components.hall_machine_component import HallMachineComponents
from gym_app.models import HallMachine


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_fetch_all_hall_machines(mock_repo):

    mock_hall_machine1 = MagicMock(spec=HallMachine)
    mock_hall_machine1.hall_id = 1
    mock_hall_machine1.machine_id = 1

    mock_hall_machine2 = MagicMock(spec=HallMachine)
    mock_hall_machine2.hall_id = 1
    mock_hall_machine2.machine_id = 2

    mock_repo.return_value.get_all_hall_machines.return_value = [
        mock_hall_machine1,
        mock_hall_machine2,
    ]

    hall_machines = HallMachineComponents().fetch_all_hall_machines(hall_id=1)

    assert len(hall_machines) == 2
    assert hall_machines[0].hall_id == 1
    assert hall_machines[1].hall_id == 1


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_fetch_hall_machine_by_id(mock_repo):

    mock_hall_machine = MagicMock(spec=HallMachine)
    mock_hall_machine.hall_id = 1
    mock_hall_machine.machine_id = 1

    mock_repo.return_value.get_hall_machine_by_id.return_value = mock_hall_machine

    hall_machine = HallMachineComponents().fetch_hall_machine_by_id(1, 1)

    assert hall_machine.hall_id == 1
    assert hall_machine.machine_id == 1


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_add_hall_machine(mock_repo):

    mock_hall_machine = MagicMock(spec=HallMachine)
    mock_hall_machine.hall_id = 1
    mock_hall_machine.machine_id = 1
    mock_hall_machine.name = "Sample HallMachine"
    mock_hall_machine.uid = "machine_1"

    mock_repo.return_value.create_hall_machine.return_value = mock_hall_machine

    data = {
        "hall_id": 1,
        "machine_id": 1,
        "name": "Sample HallMachine",
        "uid": "machine_1",
    }

    hall_machine = HallMachineComponents().add_hall_machine(data)

    assert hall_machine.hall_id == 1
    assert hall_machine.machine_id == 1
    assert hall_machine.name == "Sample HallMachine"
    assert hall_machine.uid == "machine_1"


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_modify_hall_machine(mock_repo):

    mock_hall_machine = MagicMock(spec=HallMachine)
    mock_hall_machine.name = "Updated HallMachine"
    mock_hall_machine.uid = "machine_1_updated"

    mock_repo.return_value.update_hall_machine.return_value = mock_hall_machine

    data = {"name": "Updated HallMachine", "uid": "machine_1_updated"}

    hall_machine = HallMachineComponents().modify_hall_machine(1, 1, data)

    assert hall_machine.name == "Updated HallMachine"
    assert hall_machine.uid == "machine_1_updated"


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_remove_hall_machine(mock_repo):

    HallMachineComponents().remove_hall_machine(1, 1)

    mock_repo.return_value.delete_hall_machine.assert_called_once_with(1, 1)


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_add_hall_machine_with_missing_fields(mock_repo):
    mock_repo.return_value.create_hall_machine.side_effect = KeyError(
        "Missing required field"
    )

    data = {
        "hall_id": 1,
    }

    with pytest.raises(KeyError, match="Missing required field"):
        HallMachineComponents().add_hall_machine(data)


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_modify_hall_machine_non_existent(mock_repo):
    mock_repo.return_value.update_hall_machine.side_effect = HallMachine.DoesNotExist

    data = {
        "name": "Non Existent HallMachine",
        "uid": "non_existent_uid",
    }

    with pytest.raises(HallMachine.DoesNotExist):
        HallMachineComponents().modify_hall_machine(999, 999, data)


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_remove_hall_machine_non_existent(mock_repo):
    mock_repo.return_value.delete_hall_machine.side_effect = HallMachine.DoesNotExist

    with pytest.raises(HallMachine.DoesNotExist):
        HallMachineComponents().remove_hall_machine(999, 999)


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_fetch_hall_machine_by_id_non_existent(mock_repo):
    mock_repo.return_value.get_hall_machine_by_id.side_effect = HallMachine.DoesNotExist

    with pytest.raises(HallMachine.DoesNotExist):
        HallMachineComponents().fetch_hall_machine_by_id(999, 999)


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_add_hall_machine_invalid_data(mock_repo):
    mock_repo.return_value.create_hall_machine.side_effect = ValueError("Invalid data")

    data = {
        "hall_id": 1,
        "machine_id": -1,
        "name": "Invalid HallMachine",
        "uid": "invalid_uid",
    }

    with pytest.raises(ValueError, match="Invalid data"):
        HallMachineComponents().add_hall_machine(data)


@pytest.mark.django_db
@patch("gym_app.components.hall_machine_component.HallMachineRepository")
def test_modify_hall_machine_invalid_data(mock_repo):
    mock_repo.return_value.update_hall_machine.side_effect = ValueError("Invalid data")

    data = {
        "name": "Updated HallMachine",
        "uid": "",
    }

    with pytest.raises(ValueError, match="Invalid data"):
        HallMachineComponents().modify_hall_machine(1, 1, data)
