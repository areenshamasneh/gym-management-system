from unittest.mock import patch, MagicMock

import pytest  # type: ignore

from gym_app.components import MemberComponent
from gym_app.exceptions import (
    ResourceNotFoundException,
    DatabaseException,
)
from gym_app.models import Member, Gym


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_fetch_all_members(mock_logger, mock_repo):
    mock_member1 = MagicMock(spec=Member)
    mock_member1.name = "Member 1"
    mock_member1.gym = MagicMock(spec=Gym)
    mock_member1.gym.id = 1

    mock_member2 = MagicMock(spec=Member)
    mock_member2.name = "Member 2"
    mock_member2.gym = MagicMock(spec=Gym)
    mock_member2.gym.id = 2

    mock_repo.get_all_members.return_value = [mock_member1, mock_member2]

    component = MemberComponent(repo=mock_repo, logger=mock_logger)
    members = component.fetch_all_members(1)

    assert len(members) == 2
    assert members[0].name == "Member 1"
    assert members[1].name == "Member 2"
    mock_logger.log_info.assert_called_with("Fetching all members")


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_fetch_member_by_id(mock_logger, mock_repo):
    mock_member = MagicMock(spec=Member)
    mock_member.name = "Member 1"
    mock_member.gym = MagicMock(spec=Gym)
    mock_member.gym.id = 1

    mock_repo.get_member_by_id.return_value = mock_member

    component = MemberComponent(repo=mock_repo, logger=mock_logger)
    member = component.fetch_member_by_id(1, 1)

    assert member.name == "Member 1"
    assert member.gym.id == 1
    mock_logger.log_info.assert_called_with("Fetching member with ID 1")


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_add_member(mock_logger, mock_repo):
    mock_member = MagicMock(spec=Member)
    mock_member.name = "Member 1"
    mock_member.gym = MagicMock(spec=Gym)
    mock_member.gym.id = 1

    mock_repo.create_member.return_value = mock_member

    component = MemberComponent(repo=mock_repo, logger=mock_logger)
    data = {
        "name": "Member 1",
        "birth_date": "1990-01-01",
        "phone_number": "123456789",
    }

    member = component.create_member(1, data)

    assert member.name == "Member 1"
    assert member.gym.id == 1
    mock_logger.log_info.assert_called_with(f"Adding new member with data: {data}")


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_modify_member(mock_logger, mock_repo):
    mock_member = MagicMock(spec=Member)
    mock_member.name = "Member Updated"
    mock_member.gym = MagicMock(spec=Gym)
    mock_member.gym.id = 1

    mock_repo.update_member.return_value = mock_member

    component = MemberComponent(repo=mock_repo, logger=mock_logger)
    data = {
        "name": "Member Updated",
        "birth_date": "1990-01-01",
        "phone_number": "987654321",
    }

    member = component.modify_member(1, 1, data)

    assert member.name == "Member Updated"
    assert member.gym.id == 1
    mock_logger.log_info.assert_called_with(
        f"Modifying member with ID 1 with data: {data}"
    )


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_remove_member(mock_logger, mock_repo):
    component = MemberComponent(repo=mock_repo, logger=mock_logger)
    component.remove_member(1, 1)

    assert mock_repo.delete_member.called
    assert mock_repo.delete_member.call_count == 1
    mock_logger.log_info.assert_called_with("Removing member with ID 1")


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_add_member_with_missing_fields(mock_logger, mock_repo):
    mock_repo.create_member.side_effect = DatabaseException(
        "An error occurred while adding the member."
    )

    component = MemberComponent(repo=mock_repo, logger=mock_logger)
    data = {"name": "Member 1"}

    with pytest.raises(
            DatabaseException, match="An error occurred while adding the member."
    ):
        component.create_member(1, data)


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_modify_member_non_existent(mock_logger, mock_repo):
    mock_repo.update_member.side_effect = ResourceNotFoundException(
        "Member with ID 999 not found."
    )

    component = MemberComponent(repo=mock_repo, logger=mock_logger)
    data = {"name": "Non Existent Member"}

    with pytest.raises(
            ResourceNotFoundException, match="Member with ID 999 not found."
    ):
        component.modify_member(1, 999, data)


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_remove_member_non_existent(mock_logger, mock_repo):
    mock_repo.delete_member.side_effect = ResourceNotFoundException(
        "Member with ID 999 not found."
    )

    component = MemberComponent(repo=mock_repo, logger=mock_logger)
    with pytest.raises(
            ResourceNotFoundException, match="Member with ID 999 not found."
    ):
        component.remove_member(1, 999)


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
@patch("gym_app.components.member_component.SimpleLogger")
def test_fetch_member_by_id_non_existent(mock_logger, mock_repo):
    mock_repo.get_member_by_id.side_effect = ResourceNotFoundException(
        "Member with ID 999 not found."
    )

    component = MemberComponent(repo=mock_repo, logger=mock_logger)
    with pytest.raises(
            ResourceNotFoundException, match="Member with ID 999 not found."
    ):
        component.fetch_member_by_id(1, 999)
