from gym_app.repositories.member_repository import MemberRepository


class MemberComponent:
    @staticmethod
    def fetch_all_members():
        return MemberRepository.get_all_members()

    @staticmethod
    def fetch_member_by_id(member_id):
        return MemberRepository.get_member_by_id(member_id)

    @staticmethod
    def add_member(data):
        return MemberRepository.create_member(data)

    @staticmethod
    def modify_member(member_id, data):
        return MemberRepository.update_member(member_id, data)

    @staticmethod
    def remove_member(member_id):
        MemberRepository.delete_member(member_id)
