import unittest
from unittest.mock import MagicMock, patch

from gym_app.components import HallComponent
from gym_app.exceptions import ResourceNotFoundException


class TestHallComponent(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.commit_patch = patch('common.db.database.Session.commit')
        self.mock_commit = self.commit_patch.start()

        self.component = HallComponent(hall_repository=self.mock_repo)

    def tearDown(self):
        self.commit_patch.stop()

    def test_fetch_all_halls_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.get_all_halls.return_value = ["hall1", "hall2"]

        result = self.component.fetch_all_halls(gym_id=1)

        self.assertEqual(result, ["hall1", "hall2"])
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_all_halls.assert_called_once_with("mock_gym")

    def test_fetch_all_halls_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_all_halls(gym_id=1)

        self.assertEqual(str(context.exception), "Gym not found")

    def test_fetch_all_halls_no_halls_found(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.get_all_halls.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_all_halls(gym_id=1)

        self.assertEqual(str(context.exception), "No halls found for this gym")

    def test_fetch_hall_by_id_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.get_hall_by_id.return_value = "mock_hall"

        result = self.component.fetch_hall_by_id(gym_id=1, hall_id=1)

        self.assertEqual(result, "mock_hall")
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_hall_by_id.assert_called_once_with("mock_gym", 1)

    def test_fetch_hall_by_id_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_hall_by_id(gym_id=1, hall_id=1)

        self.assertEqual(str(context.exception), "Gym not found")

    def test_fetch_hall_by_id_hall_not_found(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.get_hall_by_id.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_hall_by_id(gym_id=1, hall_id=1)

        self.assertEqual(str(context.exception), "Hall not found")

    def test_add_hall_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.create_hall.return_value = "new_hall"

        result = self.component.add_hall(gym_id=1, data={"hall_type": 1, "name": "Hall 1"})

        self.assertEqual(result, "new_hall")
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.create_hall.assert_called_once_with("mock_gym", {"hall_type": 1, "name": "Hall 1"})
        self.mock_commit.assert_called_once()

    def test_add_hall_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.add_hall(gym_id=1, data={"hall_type": 1, "name": "Hall 1"})

        self.assertEqual(str(context.exception), "Gym not found")

    def test_add_hall_hall_type_missing(self):
        with self.assertRaises(ValueError) as context:
            self.component.add_hall(gym_id=1, data={"name": "Hall 1"})

        self.assertEqual(str(context.exception), "HallType ID is required")

    def test_modify_hall_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.update_hall.return_value = "updated_hall"

        result = self.component.modify_hall(gym_id=1, hall_id=1, data={"name": "Updated Hall"})

        self.assertEqual(result, "updated_hall")
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.update_hall.assert_called_once_with("mock_gym", 1, {"name": "Updated Hall"})
        self.mock_commit.assert_called_once()

    def test_modify_hall_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.modify_hall(gym_id=1, hall_id=1, data={"name": "Updated Hall"})

        self.assertEqual(str(context.exception), "Gym not found")

    def test_modify_hall_hall_not_found(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.update_hall.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.modify_hall(gym_id=1, hall_id=1, data={"name": "Updated Hall"})

        self.assertEqual(str(context.exception), "Hall not found")

    def test_remove_hall_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.delete_hall.return_value = True

        result = self.component.remove_hall(gym_id=1, hall_id=1)

        self.assertTrue(result)
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.delete_hall.assert_called_once_with("mock_gym", 1)
        self.mock_commit.assert_called_once()

    def test_remove_hall_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.remove_hall(gym_id=1, hall_id=1)

        self.assertEqual(str(context.exception), "Gym not found")

    def test_remove_hall_hall_not_found(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.delete_hall.return_value = False

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.remove_hall(gym_id=1, hall_id=1)

        self.assertEqual(str(context.exception), "Hall not found")


if __name__ == '__main__':
    unittest.main()
