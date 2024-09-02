from unittest.mock import MagicMock, patch

import pytest

from gym_app.components.member_component import MemberComponent
from gym_app.exceptions import ResourceNotFoundException, DatabaseException


@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_fetch_all_members_with_members(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = MemberComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.get_all_members.return_value = [
        {"id": 1, "name": "Member 1", "birth_date": "1990-01-01", "phone_number": "123456789"},
        {"id": 2, "name": "Member 2", "birth_date": "1985-05-15", "phone_number": "987654321"}
    ]

    members = component.fetch_all_members(gym_id=1)
    expected_members = [
        {"id": 1, "name": "Member 1", "birth_date": "1990-01-01", "phone_number": "123456789"},
        {"id": 2, "name": "Member 2", "birth_date": "1985-05-15", "phone_number": "987654321"}
    ]
    assert members == expected_members

    mock_logger.log_info.assert_called_with("Fetching all members")
    mock_logger.log_error.assert_not_called()


@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_fetch_empty_members(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = MemberComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.get_all_members.return_value = []

    with pytest.raises(DatabaseException, match="No members found"):
        component.fetch_all_members(gym_id=1)

    mock_logger.log_error.assert_called_with("Database error fetching members: No members found")


@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_fetch_member_by_id(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = MemberComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.get_member_by_id.return_value = None

    with pytest.raises(ResourceNotFoundException, match="Member with ID 999 not found"):
        component.fetch_member_by_id(gym_id=1, member_id=999)

    mock_logger.log_error.assert_called_with("Resource not found: Member with ID 999 not found")


@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_add_member_database_exception(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = MemberComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.create_member.side_effect = DatabaseException("Database error")

    with pytest.raises(DatabaseException, match="Database error"):
        component.create_member(gym_id=1,
                                data={'name': 'Member 1', 'birth_date': '1990-01-01', 'phone_number': '123456789'})


@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_add_member(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = MemberComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.create_member.return_value = {'id': 1, 'name': 'Member 1'}

    data = {'name': 'Member 1', 'birth_date': '1990-01-01', 'phone_number': '123456789'}
    result = component.create_member(gym_id=1, data=data)

    assert result == {'id': 1, 'name': 'Member 1'}
    mock_logger.log_info.assert_called_with(f"Adding new member with data: {data}")


@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_modify_member(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = MemberComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.update_member.return_value = {'id': 1, 'name': 'Updated Member'}

    data = {'name': 'Updated Member'}
    result = component.modify_member(gym_id=1, member_id=1, data=data)

    assert result == {'id': 1, 'name': 'Updated Member'}
    mock_logger.log_info.assert_called_with(f"Modifying member with ID 1 with data: {data}")


@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_remove_member(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = MemberComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.delete_member.return_value = True

    component.remove_member(gym_id=1, member_id=1)

    mock_repo_class.return_value.delete_member.assert_called_with(1, 1)
    mock_logger.log_info.assert_called_with("Removing member with ID 1")


@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_modify_member_resource_not_found(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = MemberComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.update_member.side_effect = ResourceNotFoundException("Member not found")

    with pytest.raises(ResourceNotFoundException, match="Member not found"):
        component.modify_member(gym_id=1, member_id=1, data={'name': 'Updated Member'})

    mock_logger.log_error.assert_called_with("Resource not found: Member not found")


@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_remove_member_resource_not_found(mock_logger_class, mock_repo_class):
    mock_logger = MagicMock()
    mock_logger_class.return_value = mock_logger
    component = MemberComponent(mock_repo_class.return_value, mock_logger)

    mock_repo_class.return_value.delete_member.side_effect = ResourceNotFoundException("Member not found")

    with pytest.raises(ResourceNotFoundException, match="Member not found"):
        component.remove_member(gym_id=1, member_id=1)

    mock_logger.log_error.assert_called_with("Resource not found: Member not found")
