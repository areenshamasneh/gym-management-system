import unittest
from unittest.mock import MagicMock, patch

from gym_app.components.hall_machine_component import HallMachineComponent
from gym_app.exceptions import (
    ResourceNotFoundException,
    ValidationException,
)


class TestHallMachineComponent(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_logger = MagicMock()
        self.component = HallMachineComponent(
            repo=self.mock_repo, logger=self.mock_logger
        )

    @patch(
        "gym_app.components.hall_machine_component.HallMachineRepository",
        return_value=MagicMock(),
    )
    def test_fetch_hall_machines_by_gym_success(self, MockRepo):
        self.mock_repo.get_hall_machines_by_gym.return_value = ["machine1", "machine2"]
        result = self.component.fetch_hall_machines_by_gym("gym_id")
        self.assertEqual(result, ["machine1", "machine2"])
        self.mock_logger.log_info.assert_called_with(
            "Fetching hall machines for gym ID gym_id"
        )

    @patch(
        "gym_app.components.hall_machine_component.HallMachineRepository",
        return_value=MagicMock(),
    )
    def test_fetch_hall_machines_by_gym_validation_exception(self, MockRepo):
        self.mock_repo.get_hall_machines_by_gym.side_effect = ValueError(
            "Invalid input"
        )
        with self.assertRaises(ValidationException):
            self.component.fetch_hall_machines_by_gym("gym_id")
        self.mock_logger.log_error.assert_called_with(
            "Error fetching hall machines: Invalid input"
        )

    @patch(
        "gym_app.components.hall_machine_component.HallMachineRepository",
        return_value=MagicMock(),
    )
    def test_fetch_hall_machines_by_hall_success(self, MockRepo):
        self.mock_repo.get_hall_machines_by_hall.return_value = ["machine1", "machine2"]
        result = self.component.fetch_hall_machines_by_hall("hall_id")
        self.assertEqual(result, ["machine1", "machine2"])
        self.mock_logger.log_info.assert_called_with(
            "Fetching hall machines for hall ID hall_id"
        )

    @patch(
        "gym_app.components.hall_machine_component.HallMachineRepository",
        return_value=MagicMock(),
    )
    def test_fetch_hall_machines_by_hall_resource_not_found(self, MockRepo):
        self.mock_repo.get_hall_machines_by_hall.return_value = None
        with self.assertRaises(ResourceNotFoundException):
            self.component.fetch_hall_machines_by_hall("hall_id")
        self.mock_logger.log_error.assert_called_with(
            "Error fetching hall machines: No hall machines found for hall ID hall_id."
        )


if __name__ == "__main__":
    unittest.main()
