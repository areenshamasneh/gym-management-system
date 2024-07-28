from gym_app.repositories.member_repository import MemberRepository


class MemberComponent:

    def fetch_all_members(gym_id):
        return MemberRepository.get_all_members(gym_id)

    def fetch_member_by_id(gym_id, member_id):
        return MemberRepository.get_member_by_id(gym_id, member_id)

    def add_member(gym_id, data):
        return MemberRepository.create_member(gym_id, data)

    def modify_member(gym_id, member_id, data):
        return MemberRepository.update_member(gym_id, member_id, data)

    def remove_member(gym_id, member_id):
        MemberRepository.delete_member(gym_id, member_id)
