import unittest
from unittest.mock import MagicMock

from gym_app.components import MachineComponent
from gym_app.exceptions import ResourceNotFoundException


class TestMachineComponent(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.component = MachineComponent(repo=self.mock_repo)

    def test_fetch_all_machines_in_gym_success(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.get_all_machines_in_gym.return_value = ["machine1", "machine2"]
        result = self.component.fetch_all_machines_in_gym(1)
        self.assertEqual(result, ["machine1", "machine2"])
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_all_machines_in_gym.assert_called_once_with("gym")

    def test_fetch_all_machines_in_gym_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None
        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_all_machines_in_gym(1)
        self.assertEqual(str(context.exception), "Gym not found")
        self.mock_repo.get_gym.assert_called_once_with(1)

    def test_fetch_machine_by_id_in_gym_success(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.get_machine_by_id_in_gym.return_value = MagicMock(machine="machine1")
        result = self.component.fetch_machine_by_id_in_gym(1, 101)
        self.assertEqual(result, "machine1")
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_machine_by_id_in_gym.assert_called_once_with("gym", 101)

    def test_fetch_machine_by_id_in_gym_not_found(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.get_machine_by_id_in_gym.return_value = None
        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_machine_by_id_in_gym(1, 101)
        self.assertEqual(str(context.exception), "Machine with ID 101 not found in gym_id 1.")
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_machine_by_id_in_gym.assert_called_once_with("gym", 101)

    def test_fetch_all_machines_in_hall_success(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.get_all_machines_in_hall.return_value = ["machine1", "machine2"]
        result = self.component.fetch_all_machines_in_hall(1, 2)
        self.assertEqual(result, ["machine1", "machine2"])
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_all_machines_in_hall.assert_called_once_with("gym", 2)

    def test_fetch_all_machines_in_hall_not_found(self):
        self.mock_repo.get_gym.return_value = None
        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_all_machines_in_hall(1, 2)
        self.assertEqual(str(context.exception), "Gym not found")
        self.mock_repo.get_gym.assert_called_once_with(1)

    def test_add_machine_and_hall_machine_success(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.create_machine.return_value = MagicMock(id=101)
        result = self.component.add_machine_and_hall_machine(1, 2, {"name": "Machine A"})
        self.assertEqual(result.id, 101)
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.create_machine.assert_called_once_with({"name": "Machine A"})
        self.mock_repo.create_hall_machine.assert_called_once_with(2, 101)

    def test_add_machine_and_hall_machine_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None
        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.add_machine_and_hall_machine(1, 2, {"name": "Machine A"})
        self.assertEqual(str(context.exception), "Gym not found")
        self.mock_repo.get_gym.assert_called_once_with(1)

    def test_modify_machine_and_hall_machine_success(self):
        hall_machine = MagicMock()
        hall_machine.machine = MagicMock()

        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.update_machine.return_value = hall_machine
        self.mock_repo.update_hall_machine.return_value = "updated_hall_machine"

        result = self.component.modify_machine_and_hall_machine(1, 2, 101, {"name": "Machine A"})
        self.assertEqual(result, "updated_hall_machine")

        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.update_machine.assert_called_once_with("gym", 2, 101, {"name": "Machine A"})

        self.mock_repo.update_hall_machine.assert_called_once_with(hall_machine, hall_machine.machine)

    def test_modify_machine_and_hall_machine_machine_not_found(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.update_machine.return_value = None
        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.modify_machine_and_hall_machine(1, 2, 101, {"name": "Machine A"})
        self.assertEqual(str(context.exception), "Machine with ID 101 not found in hall_id 2.")
        self.mock_repo.get_gym.assert_called_once_with(1)

    def test_remove_hall_machine_success(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.delete_hall_machine.return_value = True
        result = self.component.remove_hall_machine(1, 2, 101)
        self.assertTrue(result)
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.delete_hall_machine.assert_called_once_with("gym", 2, 101)

    def test_remove_hall_machine_failure(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.delete_hall_machine.return_value = False
        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.remove_hall_machine(1, 2, 101)
        self.assertEqual(str(context.exception), "Failed to delete hall machine")
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.delete_hall_machine.assert_called_once_with("gym", 2, 101)


if __name__ == '__main__':
    unittest.main()
