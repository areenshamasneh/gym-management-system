import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components.machine_component import MachineComponent
from gym_app.models import Machine


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_fetch_all_machines(mock_repo):

    mock_machine1 = MagicMock(spec=Machine)
    mock_machine1.serial_number = "SN001"
    mock_machine1.type = "Running"
    mock_machine1.model = "Model 1"
    mock_machine1.brand = "Brand 1"
    mock_machine1.status = "operational"
    mock_machine1.maintenance_date = "2024-01-01"

    mock_machine2 = MagicMock(spec=Machine)
    mock_machine2.serial_number = "SN002"
    mock_machine2.type = "Cycling"
    mock_machine2.model = "Model 2"
    mock_machine2.brand = "Brand 2"
    mock_machine2.status = "broken"
    mock_machine2.maintenance_date = "2024-02-01"

    mock_repo.get_all_machines.return_value = [mock_machine1, mock_machine2]

    machines = MachineComponent.fetch_all_machines()

    assert len(machines) == 2
    assert machines[0].serial_number == "SN001"
    assert machines[1].serial_number == "SN002"


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_fetch_machine_by_id(mock_repo):

    mock_machine = MagicMock(spec=Machine)
    mock_machine.serial_number = "SN001"
    mock_machine.type = "Running"
    mock_machine.model = "Model 1"
    mock_machine.brand = "Brand 1"
    mock_machine.status = "operational"
    mock_machine.maintenance_date = "2024-01-01"

    mock_repo.get_machine_by_id.return_value = mock_machine

    machine = MachineComponent.fetch_machine_by_id("SN001")

    assert machine.serial_number == "SN001"
    assert machine.type == "Running"


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_add_machine(mock_repo):

    mock_machine = MagicMock(spec=Machine)
    mock_machine.serial_number = "SN001"
    mock_machine.type = "Running"
    mock_machine.model = "Model 1"
    mock_machine.brand = "Brand 1"
    mock_machine.status = "operational"
    mock_machine.maintenance_date = "2024-01-01"

    mock_repo.create_machine.return_value = mock_machine

    data = {
        "serial_number": "SN001",
        "type": "Running",
        "model": "Model 1",
        "brand": "Brand 1",
        "status": "operational",
        "maintenance_date": "2024-01-01",
    }

    machine = MachineComponent.add_machine(data)

    assert machine.serial_number == "SN001"
    assert machine.type == "Running"


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_modify_machine(mock_repo):

    mock_machine = MagicMock(spec=Machine)
    mock_machine.serial_number = "SN001"
    mock_machine.type = "Running"
    mock_machine.model = "Model Updated"
    mock_machine.brand = "Brand 1"
    mock_machine.status = "operational"
    mock_machine.maintenance_date = "2024-01-01"

    mock_repo.update_machine.return_value = mock_machine

    data = {
        "model": "Model Updated",
    }

    machine = MachineComponent.modify_machine("SN001", data)

    assert machine.model == "Model Updated"


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_remove_machine(mock_repo):

    MachineComponent.remove_machine("SN001")

    assert mock_repo.delete_machine.called
    assert mock_repo.delete_machine.call_count == 1


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_add_machine_with_missing_fields(mock_repo):
    mock_repo.create_machine.side_effect = KeyError("Missing required field")

    data = {"serial_number": "SN001"}

    with pytest.raises(KeyError, match="Missing required field"):
        MachineComponent.add_machine(data)


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_modify_machine_non_existent(mock_repo):
    mock_repo.update_machine.side_effect = Machine.DoesNotExist

    data = {"model": "Non Existent Machine"}

    with pytest.raises(Machine.DoesNotExist):
        MachineComponent.modify_machine("SN999", data)


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_remove_machine_non_existent(mock_repo):
    mock_repo.delete_machine.side_effect = Machine.DoesNotExist

    with pytest.raises(Machine.DoesNotExist):
        MachineComponent.remove_machine("SN999")


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_fetch_machine_by_id_non_existent(mock_repo):
    mock_repo.get_machine_by_id.side_effect = Machine.DoesNotExist

    with pytest.raises(Machine.DoesNotExist):
        MachineComponent.fetch_machine_by_id("SN999")


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_add_machine_invalid_data(mock_repo):
    mock_repo.create_machine.side_effect = ValueError("Invalid data")

    data = {
        "serial_number": "SN001",
        "type": "",
        "model": "Invalid Machine",
        "brand": "Brand 1",
        "status": "operational",
        "maintenance_date": "2024-01-01",
    }

    with pytest.raises(ValueError, match="Invalid data"):
        MachineComponent.add_machine(data)


@pytest.mark.django_db
@patch("gym_app.components.machine_component.MachineRepository")
def test_modify_machine_invalid_data(mock_repo):
    mock_repo.update_machine.side_effect = ValueError("Invalid data")

    data = {
        "model": "",
    }

    with pytest.raises(ValueError, match="Invalid data"):
        MachineComponent.modify_machine("SN001", data)
