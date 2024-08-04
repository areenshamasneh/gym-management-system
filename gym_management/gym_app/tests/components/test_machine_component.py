import unittest
from unittest.mock import MagicMock

from gym_app.components.machine_component import MachineComponent
from gym_app.exceptions import (
    DatabaseException,
    ResourceNotFoundException,
    ValidationException,
)
from gym_app.logging import SimpleLogger
from gym_app.repositories.machine_repository import MachineRepository


class TestMachineComponent(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock(spec=MachineRepository)
        self.mock_logger = MagicMock(spec=SimpleLogger)
        self.component = MachineComponent(repo=self.mock_repo, logger=self.mock_logger)

    def test_fetch_all_machines_in_gym_success(self):
        gym_id = 1
        expected_machines = [
            {"id": 1, "name": "Treadmill"},
            {"id": 2, "name": "Elliptical"},
        ]
        self.mock_repo.get_all_hall_machines_in_gym.return_value = expected_machines

        result = self.component.fetch_all_machines_in_gym(gym_id)

        self.assertEqual(result, expected_machines)
        self.mock_logger.log_info.assert_called_with(
            f"Fetching all hall machines for gym_id: {gym_id}"
        )

    def test_fetch_all_machines_in_gym_failure(self):
        gym_id = 1
        self.mock_repo.get_all_hall_machines_in_gym.side_effect = Exception(
            "Database error"
        )

        with self.assertRaises(DatabaseException) as context:
            self.component.fetch_all_machines_in_gym(gym_id)

        self.assertEqual(
            str(context.exception),
            "An error occurred while fetching machines in the gym.",
        )
        self.mock_logger.log_error.assert_called_with(
            "Error fetching machines in gym: Database error"
        )

    def test_fetch_all_machines_in_hall_success(self):
        gym_id, hall_id = 1, 1
        expected_machines = [{"id": 1, "name": "Treadmill"}]
        self.mock_repo.get_all_machines_in_hall.return_value = expected_machines

        result = self.component.fetch_all_machines_in_hall(gym_id, hall_id)

        self.assertEqual(result, expected_machines)
        self.mock_logger.log_info.assert_called_with(
            f"Fetching all machines for gym_id: {gym_id}, hall_id: {hall_id}"
        )

    def test_fetch_all_machines_in_hall_failure(self):
        gym_id, hall_id = 1, 1
        self.mock_repo.get_all_machines_in_hall.side_effect = Exception(
            "Database error"
        )

        with self.assertRaises(DatabaseException) as context:
            self.component.fetch_all_machines_in_hall(gym_id, hall_id)

        self.assertEqual(
            str(context.exception),
            "An error occurred while fetching machines in the hall.",
        )
        self.mock_logger.log_error.assert_called_with(
            "Error fetching machines in hall: Database error"
        )

    def test_fetch_machine_by_id_in_hall_success(self):
        gym_id, hall_id, machine_id = 1, 1, 1
        expected_machine = MagicMock()
        expected_machine.machine_id = machine_id
        self.mock_repo.get_machine_by_id_in_hall.return_value = expected_machine

        result = self.component.fetch_machine_by_id_in_hall(gym_id, hall_id, machine_id)

        self.assertEqual(result, machine_id)
        self.mock_logger.log_info.assert_called_with(
            f"Fetching machine by ID: {machine_id} in hall: {hall_id}"
        )

    def test_fetch_machine_by_id_in_hall_not_found(self):
        gym_id, hall_id, machine_id = 1, 1, 1
        self.mock_repo.get_machine_by_id_in_hall.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_machine_by_id_in_hall(gym_id, hall_id, machine_id)

        self.assertEqual(
            str(context.exception), f"Machine with ID {machine_id} not found."
        )
        self.mock_logger.log_error.assert_called_with(
            f"Machine with ID {machine_id} not found in hall: {hall_id}"
        )

    def test_fetch_machine_by_id_in_hall_failure(self):
        gym_id, hall_id, machine_id = 1, 1, 1
        self.mock_repo.get_machine_by_id_in_hall.side_effect = Exception(
            "Database error"
        )

        with self.assertRaises(DatabaseException) as context:
            self.component.fetch_machine_by_id_in_hall(gym_id, hall_id, machine_id)

        self.assertEqual(
            str(context.exception),
            "An error occurred while fetching the machine by ID.",
        )
        self.mock_logger.log_error.assert_called_with(
            f"Error fetching machine by ID: Database error"
        )

    def test_add_hall_machine_success(self):
        gym_id, hall_id = 1, 1
        data = {"name": "Treadmill"}
        expected_machine = MagicMock()
        self.mock_repo.create_hall_machine.return_value = expected_machine

        result = self.component.add_hall_machine(gym_id, hall_id, data)

        self.assertEqual(result, expected_machine)
        self.mock_logger.log_info.assert_any_call(
            f"Adding hall machine with data: {data}"
        )
        self.mock_logger.log_info.assert_any_call(
            f"Added hall machine: {expected_machine}"
        )

    def test_add_hall_machine_validation_error(self):
        gym_id, hall_id = 1, 1
        data = {"name": "Treadmill"}
        self.mock_repo.create_hall_machine.side_effect = ValueError("Invalid data")

        with self.assertRaises(ValidationException) as context:
            self.component.add_hall_machine(gym_id, hall_id, data)

        self.assertEqual(str(context.exception), "Validation error: Invalid data")
        self.mock_logger.log_error.assert_called_with(
            "Error adding hall machine: Invalid data"
        )

    def test_add_hall_machine_failure(self):
        gym_id, hall_id = 1, 1
        data = {"name": "Treadmill"}
        self.mock_repo.create_hall_machine.side_effect = Exception("Database error")

        with self.assertRaises(DatabaseException) as context:
            self.component.add_hall_machine(gym_id, hall_id, data)

        self.assertEqual(
            str(context.exception), "An error occurred while adding the hall machine."
        )
        self.mock_logger.log_error.assert_called_with(
            "Error adding hall machine: Database error"
        )

    def test_modify_hall_machine_success(self):
        gym_id, hall_id, machine_id = 1, 1, 1
        data = {"name": "Updated Treadmill"}
        expected_machine = MagicMock()
        self.mock_repo.update_hall_machine.return_value = expected_machine

        result = self.component.modify_hall_machine(gym_id, hall_id, machine_id, data)

        self.assertEqual(result, expected_machine)
        self.mock_logger.log_info.assert_any_call(
            f"Modifying hall machine with ID: {machine_id} and data: {data}"
        )
        self.mock_logger.log_info.assert_any_call(
            f"Modified hall machine: {expected_machine}"
        )

    def test_modify_hall_machine_not_found(self):
        gym_id, hall_id, machine_id = 1, 1, 1
        data = {"name": "Updated Treadmill"}
        self.mock_repo.update_hall_machine.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.modify_hall_machine(gym_id, hall_id, machine_id, data)

        self.assertEqual(
            str(context.exception), f"Machine with ID {machine_id} not found."
        )
        self.mock_logger.log_error.assert_called_with(
            f"Machine with ID {machine_id} not found."
        )

    def test_modify_hall_machine_validation_error(self):
        gym_id, hall_id, machine_id = 1, 1, 1
        data = {"name": "Updated Treadmill"}
        self.mock_repo.update_hall_machine.side_effect = ValueError("Invalid data")

        with self.assertRaises(ValidationException) as context:
            self.component.modify_hall_machine(gym_id, hall_id, machine_id, data)

        self.assertEqual(str(context.exception), "Validation error: Invalid data")
        self.mock_logger.log_error.assert_called_with(
            "Error modifying hall machine: Invalid data"
        )

    def test_modify_hall_machine_failure(self):
        gym_id, hall_id, machine_id = 1, 1, 1
        data = {"name": "Updated Treadmill"}
        self.mock_repo.update_hall_machine.side_effect = Exception("Database error")

        with self.assertRaises(DatabaseException) as context:
            self.component.modify_hall_machine(gym_id, hall_id, machine_id, data)

        self.assertEqual(
            str(context.exception),
            "An error occurred while modifying the hall machine.",
        )
        self.mock_logger.log_error.assert_called_with(
            "Error modifying hall machine: Database error"
        )

    def test_remove_hall_machine_success(self):
        gym_id, hall_id, machine_id = 1, 1, 1
        self.mock_repo.delete_hall_machine.return_value = None

        self.component.remove_hall_machine(gym_id, hall_id, machine_id)

        self.mock_logger.log_info.assert_called_with(
            f"Removed hall machine with ID: {machine_id}"
        )

    def test_remove_hall_machine_validation_error(self):
        gym_id, hall_id, machine_id = 1, 1, 1
        self.mock_repo.delete_hall_machine.side_effect = ValueError("Invalid data")

        with self.assertRaises(ValidationException) as context:
            self.component.remove_hall_machine(gym_id, hall_id, machine_id)

        self.assertEqual(str(context.exception), "Validation error: Invalid data")
        self.mock_logger.log_error.assert_called_with(
            "Error removing hall machine: Invalid data"
        )

    def test_remove_hall_machine_failure(self):
        gym_id, hall_id, machine_id = 1, 1, 1
        self.mock_repo.delete_hall_machine.side_effect = Exception("Database error")

        with self.assertRaises(DatabaseException) as context:
            self.component.remove_hall_machine(gym_id, hall_id, machine_id)

        self.assertEqual(
            str(context.exception), "An error occurred while removing the hall machine."
        )
        self.mock_logger.log_error.assert_called_with(
            "Error removing hall machine: Database error"
        )


if __name__ == "__main__":
    unittest.main()
