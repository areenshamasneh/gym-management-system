import pytest  # type: ignore
from unittest.mock import patch, MagicMock
from gym_app.components import MemberComponent
from gym_app.models import Member, Gym


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_fetch_all_members(mock_repo):
    mock_member1 = MagicMock(spec=Member)
    mock_member1.name = "Member 1"
    mock_member1.gym = MagicMock(spec=Gym)
    mock_member1.gym.id = 1

    mock_member2 = MagicMock(spec=Member)
    mock_member2.name = "Member 2"
    mock_member2.gym = MagicMock(spec=Gym)
    mock_member2.gym.id = 2

    mock_repo.get_all_members.return_value = [mock_member1, mock_member2]

    members = MemberComponent.fetch_all_members(1)

    assert len(members) == 2
    assert members[0].name == "Member 1"
    assert members[1].name == "Member 2"


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_fetch_member_by_id(mock_repo):
    mock_member = MagicMock(spec=Member)
    mock_member.name = "Member 1"
    mock_member.gym = MagicMock(spec=Gym)
    mock_member.gym.id = 1

    mock_repo.get_member_by_id.return_value = mock_member

    member = MemberComponent.fetch_member_by_id(1, 1)

    assert member.name == "Member 1"
    assert member.gym.id == 1


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_add_member(mock_repo):
    mock_member = MagicMock(spec=Member)
    mock_member.name = "Member 1"
    mock_member.gym = MagicMock(spec=Gym)
    mock_member.gym.id = 1

    mock_repo.create_member.return_value = mock_member

    data = {
        "name": "Member 1",
        "gym_id": 1,
        "birth_date": "1990-01-01",
        "phone_number": "123456789",
    }

    member = MemberComponent.add_member(1, data)

    assert member.name == "Member 1"
    assert member.gym.id == 1


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_modify_member(mock_repo):
    mock_member = MagicMock(spec=Member)
    mock_member.name = "Member Updated"
    mock_member.gym = MagicMock(spec=Gym)
    mock_member.gym.id = 1

    mock_repo.update_member.return_value = mock_member

    data = {
        "name": "Member Updated",
        "gym_id": 1,
        "birth_date": "1990-01-01",
        "phone_number": "987654321",
    }

    member = MemberComponent.modify_member(1, 1, data)

    assert member.name == "Member Updated"
    assert member.gym.id == 1


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_remove_member(mock_repo):
    MemberComponent.remove_member(1, 1)

    assert mock_repo.delete_member.called
    assert mock_repo.delete_member.call_count == 1


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_add_member_with_missing_fields(mock_repo):
    mock_repo.create_member.side_effect = KeyError("Missing required field")

    data = {"name": "Member 1"}

    with pytest.raises(KeyError, match="Missing required field"):
        MemberComponent.add_member(1, data)


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_modify_member_non_existent(mock_repo):
    mock_repo.update_member.side_effect = Member.DoesNotExist

    data = {"name": "Non Existent Member"}

    with pytest.raises(Member.DoesNotExist):
        MemberComponent.modify_member(1, 999, data)


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_remove_member_non_existent(mock_repo):
    mock_repo.delete_member.side_effect = Member.DoesNotExist

    with pytest.raises(Member.DoesNotExist):
        MemberComponent.remove_member(1, 999)


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_fetch_member_by_id_non_existent(mock_repo):
    mock_repo.get_member_by_id.side_effect = Member.DoesNotExist

    with pytest.raises(Member.DoesNotExist):
        MemberComponent.fetch_member_by_id(1, 999)


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_add_member_invalid_data(mock_repo):
    mock_repo.create_member.side_effect = ValueError("Invalid data")

    data = {
        "name": "Member 1",
        "gym_id": 1,
        "birth_date": "invalid_date",
        "phone_number": "123456789",
    }

    with pytest.raises(ValueError, match="Invalid data"):
        MemberComponent.add_member(1, data)


@pytest.mark.django_db
@patch("gym_app.components.member_component.MemberRepository")
def test_modify_member_invalid_data(mock_repo):
    mock_repo.update_member.side_effect = ValueError("Invalid data")

    data = {"birth_date": "invalid_date"}

    with pytest.raises(ValueError, match="Invalid data"):
        MemberComponent.modify_member(1, 1, data)
