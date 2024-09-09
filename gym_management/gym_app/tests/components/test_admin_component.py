from unittest import TestCase
from unittest.mock import MagicMock, patch

from gym_app.components import AdminComponent
from gym_app.exceptions import ResourceNotFoundException


class TestAdminComponent(TestCase):

    def setUp(self):
        self.mock_repo = MagicMock()
        self.mock_logger = MagicMock()
        self.component = AdminComponent(admin_repository=self.mock_repo, logger=self.mock_logger)

    def test_fetch_all_admins_success(self):
        self.mock_repo.get_gym.return_value = {'id': 1, 'name': 'Test Gym'}
        self.mock_repo.get_all_admins.return_value = (['admin1', 'admin2'], 2)

        admins, total = self.component.fetch_all_admins(gym_id=1, filter_criteria=None, offset=0, limit=10)

        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_all_admins.assert_called_once_with({'id': 1, 'name': 'Test Gym'}, None, 0, 10)
        self.assertEqual(admins, ['admin1', 'admin2'])
        self.assertEqual(total, 2)

    def test_fetch_all_admins_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            self.component.fetch_all_admins(gym_id=1)

        self.mock_repo.get_gym.assert_called_once_with(1)

    def test_fetch_all_admins_no_admins_found(self):
        self.mock_repo.get_gym.return_value = {'id': 1, 'name': 'Test Gym'}
        self.mock_repo.get_all_admins.return_value = ([], 0)

        with self.assertRaises(ResourceNotFoundException):
            self.component.fetch_all_admins(gym_id=1)

    def test_fetch_admin_by_id_success(self):
        self.mock_repo.get_gym.return_value = {'id': 1, 'name': 'Test Gym'}
        self.mock_repo.get_admin_by_id.return_value = {'id': 1, 'name': 'Test Admin'}

        admin = self.component.fetch_admin_by_id(gym_id=1, admin_id=1)

        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_admin_by_id.assert_called_once_with({'id': 1, 'name': 'Test Gym'}, 1)
        self.assertEqual(admin, {'id': 1, 'name': 'Test Admin'})

    def test_fetch_admin_by_id_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            self.component.fetch_admin_by_id(gym_id=1, admin_id=1)

    def test_fetch_admin_by_id_admin_not_found(self):
        self.mock_repo.get_gym.return_value = {'id': 1, 'name': 'Test Gym'}
        self.mock_repo.get_admin_by_id.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            self.component.fetch_admin_by_id(gym_id=1, admin_id=1)

    def test_add_admin_success(self):
        self.mock_repo.get_gym.return_value = {'id': 1, 'name': 'Test Gym'}
        self.mock_repo.create_admin.return_value = {'id': 1, 'name': 'New Admin'}

        with patch('gym_app.components.admin_component.Session.commit') as mock_commit:
            admin = self.component.add_admin(gym_id=1, data={'name': 'New Admin'})
            mock_commit.assert_called_once()

        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.create_admin.assert_called_once_with({'id': 1, 'name': 'Test Gym'}, {'name': 'New Admin'})
        self.assertEqual(admin, {'id': 1, 'name': 'New Admin'})

    def test_add_admin_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            self.component.add_admin(gym_id=1, data={'name': 'New Admin'})

    def test_modify_admin_success(self):
        self.mock_repo.get_gym.return_value = {'id': 1, 'name': 'Test Gym'}
        self.mock_repo.update_admin.return_value = {'id': 1, 'name': 'Updated Admin'}

        with patch('gym_app.components.admin_component.Session.commit') as mock_commit:
            admin = self.component.modify_admin(gym_id=1, admin_id=1, data={'name': 'Updated Admin'})
            mock_commit.assert_called_once()

        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.update_admin.assert_called_once_with({'id': 1, 'name': 'Test Gym'}, 1, {'name': 'Updated Admin'})
        self.assertEqual(admin, {'id': 1, 'name': 'Updated Admin'})

    def test_modify_admin_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            self.component.modify_admin(gym_id=1, admin_id=1, data={'name': 'Updated Admin'})

    def test_modify_admin_not_found(self):
        self.mock_repo.get_gym.return_value = {'id': 1, 'name': 'Test Gym'}
        self.mock_repo.update_admin.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            self.component.modify_admin(gym_id=1, admin_id=1, data={'name': 'Updated Admin'})

    def test_remove_admin_success(self):
        self.mock_repo.get_gym.return_value = {'id': 1, 'name': 'Test Gym'}
        self.mock_repo.delete_admin.return_value = True

        with patch('gym_app.components.admin_component.Session.commit') as mock_commit:
            success = self.component.remove_admin(gym_id=1, admin_id=1)
            mock_commit.assert_called_once()

        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.delete_admin.assert_called_once_with({'id': 1, 'name': 'Test Gym'}, 1)
        self.assertTrue(success)

    def test_remove_admin_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException):
            self.component.remove_admin(gym_id=1, admin_id=1)

    def test_remove_admin_not_found(self):
        self.mock_repo.get_gym.return_value = {'id': 1, 'name': 'Test Gym'}
        self.mock_repo.delete_admin.return_value = False

        with self.assertRaises(ResourceNotFoundException):
            self.component.remove_admin(gym_id=1, admin_id=1)
