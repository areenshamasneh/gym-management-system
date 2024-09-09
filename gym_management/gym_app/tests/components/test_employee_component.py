import unittest
from unittest.mock import MagicMock, patch

from gym_app.components import EmployeeComponent
from gym_app.exceptions import ResourceNotFoundException


class TestEmployeeComponent(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.commit_patch = patch('common.db.database.Session.commit')
        self.mock_commit = self.commit_patch.start()

        self.component = EmployeeComponent(employee_repository=self.mock_repo)

    def tearDown(self):
        self.commit_patch.stop()

    def test_fetch_all_employees_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.get_all_employees.return_value = ["employee1", "employee2"]

        result = self.component.fetch_all_employees(gym_id=1)

        self.assertEqual(result, ["employee1", "employee2"])
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_all_employees.assert_called_once_with("mock_gym")

    def test_fetch_all_employees_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_all_employees(gym_id=1)

        self.assertEqual(str(context.exception), "Gym not found")

    def test_fetch_all_employees_no_employees(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.get_all_employees.return_value = []

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_all_employees(gym_id=1)

        self.assertEqual(str(context.exception), "No Employees found for this gym")

    def test_fetch_employee_by_id_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.get_employee_by_id.return_value = "mock_employee"

        result = self.component.fetch_employee_by_id(gym_id=1, employee_id=101)

        self.assertEqual(result, "mock_employee")
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.get_employee_by_id.assert_called_once_with("mock_gym", 101)

    def test_fetch_employee_by_id_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_employee_by_id(gym_id=1, employee_id=101)

        self.assertEqual(str(context.exception), "Gym not found")

    def test_fetch_employee_by_id_employee_not_found(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.get_employee_by_id.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_employee_by_id(gym_id=1, employee_id=101)

        self.assertEqual(str(context.exception), "Employee not found")

    def test_add_employee_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.create_employee.return_value = "new_employee"

        result = self.component.add_employee(gym_id=1, data={"name": "John"})

        self.assertEqual(result, "new_employee")
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.create_employee.assert_called_once_with("mock_gym", {"name": "John"})
        self.mock_commit.assert_called_once()

    def test_add_employee_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.add_employee(gym_id=1, data={"name": "John"})

        self.assertEqual(str(context.exception), "Gym not found")

    def test_modify_employee_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.update_employee.return_value = "updated_employee"

        result = self.component.modify_employee(gym_id=1, employee_id=101, data={"name": "John Updated"})

        self.assertEqual(result, "updated_employee")
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.update_employee.assert_called_once_with("mock_gym", 101, {"name": "John Updated"})
        self.mock_commit.assert_called_once()

    def test_modify_employee_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.modify_employee(gym_id=1, employee_id=101, data={"name": "John Updated"})

        self.assertEqual(str(context.exception), "Gym not found")

    def test_modify_employee_not_found(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.update_employee.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.modify_employee(gym_id=1, employee_id=101, data={"name": "John Updated"})

        self.assertEqual(str(context.exception), "Employee not found")

    def test_remove_employee_success(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.delete_employee.return_value = True

        result = self.component.remove_employee(gym_id=1, employee_id=101)

        self.assertTrue(result)
        self.mock_repo.get_gym.assert_called_once_with(1)
        self.mock_repo.delete_employee.assert_called_once_with("mock_gym", 101)
        self.mock_commit.assert_called_once()

    def test_remove_employee_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.remove_employee(gym_id=1, employee_id=101)

        self.assertEqual(str(context.exception), "Gym not found")

    def test_remove_employee_not_found(self):
        self.mock_repo.get_gym.return_value = "mock_gym"
        self.mock_repo.delete_employee.return_value = False

        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.remove_employee(gym_id=1, employee_id=101)

        self.assertEqual(str(context.exception), "Employee not found")


if __name__ == '__main__':
    unittest.main()
