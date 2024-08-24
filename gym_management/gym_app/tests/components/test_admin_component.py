from unittest import TestCase
from unittest.mock import MagicMock, patch

from gym_app.components.admin_component import AdminComponent
from gym_app.exceptions import ResourceNotFoundException, DatabaseException


class TestAdminComponent(TestCase):
    def setUp(self):
        self.mock_repository = MagicMock()
        self.mock_logger = MagicMock()
        self.component = AdminComponent(admin_repository=self.mock_repository, logger=self.mock_logger)

    @patch('gym_app.components.admin_component.AdminRepository')
    def test_fetch_all_admins(self, mockrepo):
        gym_id = 1
        mock_admins = [{"id": 1, "name": "Admin 1"}, {"id": 2, "name": "Admin 2"}]
        self.mock_repository.get_all_admins.return_value = mock_admins

        result = self.component.fetch_all_admins(gym_id)

        self.mock_repository.get_all_admins.assert_called_once_with(gym_id)
        self.assertEqual(result, mock_admins)
        self.mock_logger.log_info.assert_called_with(f"Fetching all admins for gym_id: {gym_id}")

    @patch('gym_app.components.admin_component.AdminRepository')
    def test_fetch_admin_by_id(self, mockrepo):
        gym_id = 1
        admin_id = 1
        mock_admin = {"id": admin_id, "name": "Admin 1"}
        self.mock_repository.get_admin_by_id.return_value = mock_admin

        result = self.component.fetch_admin_by_id(gym_id, admin_id)

        self.mock_repository.get_admin_by_id.assert_called_once_with(gym_id, admin_id)
        self.assertEqual(result, mock_admin)
        self.mock_logger.log_info.assert_called_with(f"Fetching admin by ID {admin_id} for gym_id: {gym_id}")

    @patch('gym_app.components.admin_component.AdminRepository')
    def test_add_admin(self, mockrepo):
        gym_id = 1
        admin_data = {"name": "Admin 1", "email": "admin1@example.com"}
        mock_admin = {"id": 1, "name": "Admin 1", "email": "admin1@example.com"}
        self.mock_repository.create_admin.return_value = mock_admin

        result = self.component.add_admin(gym_id, admin_data)

        self.mock_repository.create_admin.assert_called_once_with(gym_id, admin_data)
        self.assertEqual(result, mock_admin)
        self.mock_logger.log_info.assert_called_with(f"Adding new admin for gym_id: {gym_id}")

    @patch('gym_app.components.admin_component.AdminRepository')
    def test_modify_admin(self, mockrepo):
        gym_id = 1
        admin_id = 1
        admin_data = {"name": "Admin 1 Updated"}
        mock_admin = {"id": admin_id, "name": "Admin 1 Updated"}
        self.mock_repository.update_admin.return_value = mock_admin

        result = self.component.modify_admin(gym_id, admin_id, admin_data)

        self.mock_repository.update_admin.assert_called_once_with(gym_id, admin_id, admin_data)
        self.assertEqual(result, mock_admin)
        self.mock_logger.log_info.assert_called_with(f"Modifying admin ID {admin_id} for gym_id: {gym_id}")

    @patch('gym_app.components.admin_component.AdminRepository')
    def test_remove_admin(self, mockrepo):
        gym_id = 1
        admin_id = 1
        self.mock_repository.delete_admin.return_value = True

        result = self.component.remove_admin(gym_id, admin_id)

        self.mock_repository.delete_admin.assert_called_once_with(gym_id, admin_id)
        self.assertTrue(result, "Expected remove_admin to return True, but got None")
        self.mock_logger.log_info.assert_called_with(f"Removing admin ID {admin_id} for gym_id: {gym_id}")

    @patch('gym_app.components.admin_component.AdminRepository')
    def test_remove_admin_not_found(self, mockrepo):
        gym_id = 1
        admin_id = 1
        self.mock_repository.delete_admin.side_effect = ResourceNotFoundException("Admin not found")

        with self.assertRaises(ResourceNotFoundException):
            self.component.remove_admin(gym_id, admin_id)
        self.mock_logger.log_error.assert_called_with(
            f"Admin with ID {admin_id} not found for gym_id {gym_id}: Admin not found")

    @patch('gym_app.components.admin_component.AdminRepository')
    def test_remove_admin_database_error(self, mockrepo):
        gym_id = 1
        admin_id = 1
        self.mock_repository.delete_admin.side_effect = Exception("Database error")

        with self.assertRaises(DatabaseException):
            self.component.remove_admin(gym_id, admin_id)
        self.mock_logger.log_error.assert_called_with(
            f"Unexpected error removing admin ID {admin_id} for gym_id: {gym_id}: Database error")
