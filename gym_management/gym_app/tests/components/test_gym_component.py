import unittest
from unittest.mock import MagicMock, patch

from gym_app.components import GymComponent
from gym_app.exceptions import ResourceNotFoundException


class TestGymComponent(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.commit_patch = patch('common.db.database.Session.commit')
        self.mock_commit = self.commit_patch.start()

        self.component = GymComponent(gym_repository=self.mock_repo)

    def tearDown(self):
        self.commit_patch.stop()

    def test_fetch_all_gyms_success(self):
        self.mock_repo.get_all_gyms.return_value = ["gym1", "gym2"]

        result = self.component.fetch_all_gyms(page_number=1, page_size=10)

        self.assertEqual(result, ["gym1", "gym2"])
        self.mock_repo.get_all_gyms.assert_called_once_with(1, 10)

    def test_fetch_gym_by_id_success(self):
        self.mock_repo.get_gym_by_id.return_value = "mock_gym"

        result = self.component.fetch_gym_by_id(gym_id=1)

        self.assertEqual(result, "mock_gym")
        self.mock_repo.get_gym_by_id.assert_called_once_with(1)

    def test_fetch_gym_by_id_not_found(self):
        self.mock_repo.get_gym_by_id.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_gym_by_id(gym_id=1)

        self.assertEqual(str(context.exception), "Gym not found")

    def test_add_gym_success(self):
        self.mock_repo.create_gym.return_value = "new_gym"

        result = self.component.add_gym(data={"name": "Gym 1"})

        self.assertEqual(result, "new_gym")
        self.mock_repo.create_gym.assert_called_once_with({"name": "Gym 1"})
        self.mock_commit.assert_called_once()

    def test_modify_gym_success(self):
        self.mock_repo.update_gym.return_value = "updated_gym"

        result = self.component.modify_gym(gym_id=1, data={"name": "Updated Gym"})

        self.assertEqual(result, "updated_gym")
        self.mock_repo.update_gym.assert_called_once_with(1, {"name": "Updated Gym"})
        self.mock_commit.assert_called_once()

    def test_modify_gym_not_found(self):
        self.mock_repo.update_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.modify_gym(gym_id=1, data={"name": "Updated Gym"})

        self.assertEqual(str(context.exception), "Gym not found")

    def test_remove_gym_success(self):
        self.mock_repo.delete_gym.return_value = True

        result = self.component.remove_gym(gym_id=1)

        self.assertTrue(result)
        self.mock_repo.delete_gym.assert_called_once_with(1)
        self.mock_commit.assert_called_once()

    def test_remove_gym_not_found(self):
        self.mock_repo.delete_gym.return_value = False

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.remove_gym(gym_id=1)

        self.assertEqual(str(context.exception), "Gym not found")


if __name__ == '__main__':
    unittest.main()
