from unittest.mock import MagicMock

import pytest

from gym_app.components import MachineComponent
from gym_app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
)


class TestMachineComponent:

    @pytest.fixture
    def component(self):
        return MachineComponent()

    def test_fetch_all_machines_in_hall_success(self, component):
        component.repo.get_all_machines_in_hall = MagicMock(return_value=['machine1', 'machine2'])
        machines = component.fetch_all_machines_in_hall(gym_id=1, hall_id=1)
        assert machines == ['machine1', 'machine2']

    def test_fetch_all_machines_in_hall_no_machines(self, component):
        component.repo.get_all_machines_in_hall = MagicMock(return_value=[])
        with pytest.raises(ResourceNotFoundException):
            component.fetch_all_machines_in_hall(gym_id=1, hall_id=1)

    def test_fetch_machine_by_id_in_hall_success(self, component):
        component.repo.get_machine_by_id_in_hall = MagicMock(return_value=MagicMock(machine='machine'))
        machine = component.fetch_machine_by_id_in_hall(gym_id=1, hall_id=1, machine_id=1)
        assert machine == 'machine'

    def test_fetch_machine_by_id_in_hall_not_found(self, component):
        component.repo.get_machine_by_id_in_hall = MagicMock(return_value=None)
        with pytest.raises(ResourceNotFoundException):
            component.fetch_machine_by_id_in_hall(gym_id=1, hall_id=1, machine_id=1)

    def test_add_machine_and_hall_machine_success(self, component):
        component.repo.create_machine = MagicMock(return_value=MagicMock(id=1))
        component.repo.create_hall_machine = MagicMock()
        machine = component.add_machine_and_hall_machine(gym_id=1, hall_id=1, machine_data={'name': 'Machine1'})
        assert machine.id == 1

    def test_add_machine_and_hall_machine_validation_error(self, component):
        component.repo.create_machine = MagicMock(side_effect=ValueError("Invalid data"))
        with pytest.raises(ValidationException):
            component.add_machine_and_hall_machine(gym_id=1, hall_id=1, machine_data={'name': 'Machine1'})

    def test_modify_machine_and_hall_machine_success(self, component):
        component.repo.update_machine_and_hall_machine = MagicMock(return_value='updated_machine')
        hall_machine = component.modify_machine_and_hall_machine(gym_id=1, hall_id=1, machine_id=1,
                                                                 data={'name': 'Machine1'})
        assert hall_machine == 'updated_machine'

    def test_modify_machine_and_hall_machine_not_found(self, component):
        component.repo.update_machine_and_hall_machine = MagicMock(side_effect=ResourceNotFoundException())
        with pytest.raises(ResourceNotFoundException):
            component.modify_machine_and_hall_machine(gym_id=1, hall_id=1, machine_id=1, data={'name': 'Machine1'})

    def test_modify_machine_and_hall_machine_validation_error(self, component):
        component.repo.update_machine_and_hall_machine = MagicMock(side_effect=ValueError("Invalid data"))
        with pytest.raises(ValidationException):
            component.modify_machine_and_hall_machine(gym_id=1, hall_id=1, machine_id=1, data={'name': 'Machine1'})

    def test_remove_hall_machine_success(self, component):
        component.repo.delete_hall_machine = MagicMock()
        component.remove_hall_machine(gym_id=1, hall_id=1, machine_id=1)
        component.repo.delete_hall_machine.assert_called_once_with(1, 1, 1)

    def test_remove_hall_machine_validation_error(self, component):
        component.repo.delete_hall_machine = MagicMock(side_effect=ValueError("Invalid ID"))
        with pytest.raises(ValidationException):
            component.remove_hall_machine(gym_id=1, hall_id=1, machine_id=1)

    def test_fetch_all_machines_in_gym_success(self, component):
        component.repo.get_all_machines_in_gym = MagicMock(return_value=['machine1', 'machine2'])
        machines = component.fetch_all_machines_in_gym(gym_id=1)
        assert machines == ['machine1', 'machine2']

    def test_fetch_all_machines_in_gym_no_machines(self, component):
        component.repo.get_all_machines_in_gym = MagicMock(return_value=[])
        with pytest.raises(ResourceNotFoundException):
            component.fetch_all_machines_in_gym(gym_id=1)

    def test_fetch_machine_by_id_in_gym_success(self, component):
        component.repo.get_machine_by_id_in_gym = MagicMock(return_value=MagicMock(machine='machine'))
        machine = component.fetch_machine_by_id_in_gym(gym_id=1, machine_id=1)
        assert machine == 'machine'

    def test_fetch_machine_by_id_in_gym_not_found(self, component):
        component.repo.get_machine_by_id_in_gym = MagicMock(return_value=None)
        with pytest.raises(ResourceNotFoundException):
            component.fetch_machine_by_id_in_gym(gym_id=1, machine_id=1)
