import unittest
from unittest.mock import MagicMock

from gym_app.components import HallMachineComponent
from gym_app.exceptions import ResourceNotFoundException


class TestHallMachineComponent(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.component = HallMachineComponent(repo=self.mock_repo)

    def test_fetch_hall_machines_by_gym_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.get_hall_machines_by_gym.return_value = ["machine1", "machine2"]

        result = self.component.fetch_hall_machines_by_gym(gym_id=1)

        self.assertEqual(result, ["machine1", "machine2"])
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_hall_machines_by_gym.assert_called_once_with("mock_gym")

    def test_fetch_hall_machines_by_gym_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_hall_machines_by_gym(gym_id=1)

        self.assertEqual(str(context.exception), "Gym not found")
        self.mock_repo.get_gym.assert_called_once_with(1)

    def test_fetch_hall_machines_by_gym_no_machines_found(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.get_hall_machines_by_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_hall_machines_by_gym(gym_id=1)

        self.assertEqual(str(context.exception), "No Hall Machines found for this gym")
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_hall_machines_by_gym.assert_called_once_with("mock_gym")


if __name__ == '__main__':
    unittest.main()
