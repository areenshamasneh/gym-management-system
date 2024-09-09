import unittest
from unittest.mock import MagicMock

from gym_app.components import MemberComponent
from gym_app.exceptions import ResourceNotFoundException


class TestMemberComponent(unittest.TestCase):
    def setUp(self):
        self.mock_repo = MagicMock()
        self.component = MemberComponent(repo=self.mock_repo)

    def test_fetch_all_members_success(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.get_all_members.return_value = ["member1", "member2"]
        result = self.component.fetch_all_members(1)
        self.assertEqual(result, ["member1", "member2"])

    def test_fetch_all_members_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None
        with self.assertRaises(ResourceNotFoundException):
            self.component.fetch_all_members(1)

    def test_fetch_member_by_id_success(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.get_member_by_id.return_value = "member"
        result = self.component.fetch_member_by_id(1, 101)
        self.assertEqual(result, "member")

    def test_fetch_member_by_id_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None
        with self.assertRaises(ResourceNotFoundException):
            self.component.fetch_member_by_id(1, 101)

    def test_fetch_member_by_id_member_not_found(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.get_member_by_id.return_value = None
        with self.assertRaises(ResourceNotFoundException):
            self.component.fetch_member_by_id(1, 101)

    def test_create_member_success(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.create_member.return_value = "new_member"
        result = self.component.create_member(1, {"name": "John Doe"})
        self.assertEqual(result, "new_member")

    def test_create_member_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None
        with self.assertRaises(ResourceNotFoundException):
            self.component.create_member(1, {"name": "John Doe"})

    def test_modify_member_success(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.update_member.return_value = "updated_member"
        result = self.component.modify_member(1, 101, {"name": "Jane Doe"})
        self.assertEqual(result, "updated_member")

    def test_modify_member_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None
        with self.assertRaises(ResourceNotFoundException):
            self.component.modify_member(1, 101, {"name": "Jane Doe"})

    def test_modify_member_member_not_found(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.update_member.return_value = None
        with self.assertRaises(ResourceNotFoundException):
            self.component.modify_member(1, 101, {"name": "Jane Doe"})

    def test_remove_member_success(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.delete_member.return_value = True
        result = self.component.remove_member(1, 101)
        self.assertTrue(result)

    def test_remove_member_gym_not_found(self):
        self.mock_repo.get_gym.return_value = None
        with self.assertRaises(ResourceNotFoundException):
            self.component.remove_member(1, 101)

    def test_remove_member_member_not_found(self):
        self.mock_repo.get_gym.return_value = "gym"
        self.mock_repo.delete_member.return_value = False
        with self.assertRaises(ResourceNotFoundException):
            self.component.remove_member(1, 101)


if __name__ == '__main__':
    unittest.main()
