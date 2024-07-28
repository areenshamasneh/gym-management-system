from gym_app.repositories.member_repository import MemberRepository


class MemberComponent:

    def fetch_all_members():
        return MemberRepository.get_all_members()

    def fetch_member_by_id(member_id):
        return MemberRepository.get_member_by_id(member_id)

    def add_member(data):
        return MemberRepository.create_member(data)

    def modify_member(member_id, data):
        return MemberRepository.update_member(member_id, data)

    def remove_member(member_id):
        MemberRepository.delete_member(member_id)
