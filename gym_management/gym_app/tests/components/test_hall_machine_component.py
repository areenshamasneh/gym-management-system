import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components import HallMachineComponents
from gym_app.models import HallMachine
from gym_app.repositories.hall_machine_repository import HallMachineRepository


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_fetch_all_hall_machines(mock_logger, mock_repo):
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

    hall_machine_component = HallMachineComponents()
    hall_machines = hall_machine_component.fetch_all_hall_machines(gym_id=1, hall_id=1)

    assert len(hall_machines) == 2
    assert hall_machines[0].hall_id == 1
    assert hall_machines[1].hall_id == 1


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_fetch_hall_machine_by_id(mock_logger, mock_repo):
    mock_hall_machine = MagicMock(spec=HallMachine)
    mock_hall_machine.hall_id = 1
    mock_hall_machine.machine_id = 1

    mock_repo.return_value.get_hall_machine_by_id.return_value = mock_hall_machine

    hall_machine_component = HallMachineComponents()
    hall_machine = hall_machine_component.fetch_hall_machine_by_id(
        gym_id=1, hall_id=1, machine_id=1
    )

    assert hall_machine.hall_id == 1
    assert hall_machine.machine_id == 1


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_add_hall_machine(mock_logger, mock_repo):
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

    hall_machine_component = HallMachineComponents()
    hall_machine = hall_machine_component.add_hall_machine(
        gym_id=1, hall_id=1, data=data
    )

    assert hall_machine.hall_id == 1
    assert hall_machine.machine_id == 1
    assert hall_machine.name == "Sample HallMachine"
    assert hall_machine.uid == "machine_1"


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_modify_hall_machine(mock_logger, mock_repo):
    mock_hall_machine = MagicMock(spec=HallMachine)
    mock_hall_machine.name = "Updated HallMachine"
    mock_hall_machine.uid = "machine_1_updated"

    mock_repo.return_value.update_hall_machine.return_value = mock_hall_machine

    data = {"name": "Updated HallMachine", "uid": "machine_1_updated"}

    hall_machine_component = HallMachineComponents()
    hall_machine = hall_machine_component.modify_hall_machine(
        gym_id=1, hall_id=1, machine_id=1, data=data
    )

    assert hall_machine.name == "Updated HallMachine"
    assert hall_machine.uid == "machine_1_updated"


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_remove_hall_machine(mock_logger, mock_repo):
    hall_machine_component = HallMachineComponents()
    hall_machine_component.remove_hall_machine(gym_id=1, hall_id=1, machine_id=1)

    mock_repo.return_value.delete_hall_machine.assert_called_once_with(1, 1, 1)


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_add_hall_machine_with_missing_fields(mock_logger, mock_repo):
    mock_repo.return_value.create_hall_machine.side_effect = KeyError(
        "Missing required field"
    )

    data = {"hall_id": 1}

    hall_machine_component = HallMachineComponents()
    with pytest.raises(KeyError, match="Missing required field"):
        hall_machine_component.add_hall_machine(gym_id=1, hall_id=1, data=data)


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_modify_hall_machine_non_existent(mock_logger, mock_repo):
    mock_repo.return_value.update_hall_machine.side_effect = HallMachine.DoesNotExist

    data = {"name": "Non Existent HallMachine", "uid": "non_existent_uid"}

    hall_machine_component = HallMachineComponents()
    with pytest.raises(HallMachine.DoesNotExist):
        hall_machine_component.modify_hall_machine(
            gym_id=1, hall_id=999, machine_id=999, data=data
        )


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_remove_hall_machine_non_existent(mock_logger, mock_repo):
    mock_repo.return_value.delete_hall_machine.side_effect = HallMachine.DoesNotExist

    hall_machine_component = HallMachineComponents()
    with pytest.raises(HallMachine.DoesNotExist):
        hall_machine_component.remove_hall_machine(
            gym_id=1, hall_id=999, machine_id=999
        )


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_fetch_hall_machine_by_id_non_existent(mock_logger, mock_repo):
    mock_repo.return_value.get_hall_machine_by_id.side_effect = HallMachine.DoesNotExist

    hall_machine_component = HallMachineComponents()
    with pytest.raises(HallMachine.DoesNotExist):
        hall_machine_component.fetch_hall_machine_by_id(
            gym_id=1, hall_id=999, machine_id=999
        )


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_add_hall_machine_invalid_data(mock_logger, mock_repo):
    mock_repo.return_value.create_hall_machine.side_effect = ValueError("Invalid data")

    data = {
        "hall_id": 1,
        "machine_id": -1,
        "name": "Invalid HallMachine",
        "uid": "invalid_uid",
    }

    hall_machine_component = HallMachineComponents()
    with pytest.raises(ValueError, match="Invalid data"):
        hall_machine_component.add_hall_machine(gym_id=1, hall_id=1, data=data)


@patch("gym_app.components.hall_machine_component.HallMachineRepository")
@patch("gym_app.components.hall_machine_component.SimpleLogger")
def test_modify_hall_machine_invalid_data(mock_logger, mock_repo):
    mock_repo.return_value.update_hall_machine.side_effect = ValueError("Invalid data")

    data = {"name": "Updated HallMachine", "uid": ""}

    hall_machine_component = HallMachineComponents()
    with pytest.raises(ValueError, match="Invalid data"):
        hall_machine_component.modify_hall_machine(
            gym_id=1, hall_id=1, machine_id=1, data=data
        )
