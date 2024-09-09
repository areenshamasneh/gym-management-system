import unittest
from unittest.mock import MagicMock

from gym_app.components.hall_type_component import HallTypeComponent
from gym_app.exceptions import ResourceNotFoundException, DatabaseException


class TestHallTypeComponent(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.component = HallTypeComponent(repo=self.mock_repo)

    def test_fetch_all_hall_types_success(self):
        self.mock_repo.get_all_hall_types.return_value = ["hall_type1", "hall_type2"]
        result = self.component.fetch_all_hall_types()
        self.assertEqual(result, ["hall_type1", "hall_type2"])
        self.mock_repo.get_all_hall_types.assert_called_once()

    def test_fetch_all_hall_types_not_found(self):
        self.mock_repo.get_all_hall_types.return_value = None
        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_all_hall_types()
        self.assertEqual(str(context.exception), "No hall types found")
        self.mock_repo.get_all_hall_types.assert_called_once()

    def test_fetch_hall_type_by_id_success(self):
        self.mock_repo.get_hall_type_by_id.return_value = "hall_type"
        result = self.component.fetch_hall_type_by_id(1)
        self.assertEqual(result, "hall_type")
        self.mock_repo.get_hall_type_by_id.assert_called_once_with(1)

    def test_fetch_hall_type_by_id_not_found(self):
        self.mock_repo.get_hall_type_by_id.return_value = None
        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.fetch_hall_type_by_id(1)
        self.assertEqual(str(context.exception), "HallType with ID 1 not found")
        self.mock_repo.get_hall_type_by_id.assert_called_once_with(1)

    def test_add_hall_type_success(self):
        self.mock_repo.create_hall_type.return_value = "new_hall_type"
        result = self.component.add_hall_type({"code": "A123"})
        self.assertEqual(result, "new_hall_type")
        self.mock_repo.create_hall_type.assert_called_once_with({"code": "A123"})

    def test_add_hall_type_code_exists(self):
        self.mock_repo.create_hall_type.return_value = None
        with self.assertRaises(DatabaseException) as context:
            self.component.add_hall_type({"code": "A123"})
        self.assertEqual(str(context.exception), "Code already exists for another hall type.")
        self.mock_repo.create_hall_type.assert_called_once_with({"code": "A123"})

    def test_modify_hall_type_success(self):
        self.mock_repo.update_hall_type.return_value = "updated_hall_type"
        result = self.component.modify_hall_type(1, {"code": "A123"})
        self.assertEqual(result, "updated_hall_type")
        self.mock_repo.update_hall_type.assert_called_once_with(1, {"code": "A123"})

    def test_modify_hall_type_not_found(self):
        self.mock_repo.update_hall_type.return_value = None
        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.modify_hall_type(1, {"code": "A123"})
        self.assertEqual(str(context.exception), "HallType with ID 1 not found or code in use")
        self.mock_repo.update_hall_type.assert_called_once_with(1, {"code": "A123"})

    def test_remove_hall_type_success(self):
        self.mock_repo.delete_hall_type.return_value = True
        result = self.component.remove_hall_type(1)
        self.assertTrue(result)
        self.mock_repo.delete_hall_type.assert_called_once_with(1)

    def test_remove_hall_type_not_found(self):
        self.mock_repo.delete_hall_type.return_value = False
        with self.assertRaises(ResourceNotFoundException) as context:
            self.component.remove_hall_type(1)
        self.assertEqual(str(context.exception), "HallType with ID 1 not found or still in use")
        self.mock_repo.delete_hall_type.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
