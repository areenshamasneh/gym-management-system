from datetime import datetime

from rest_framework import viewsets, status  # type: ignore
from rest_framework.response import Response  # type: ignore

from gym_app.components import MemberComponent
from gym_app.serializers import MemberSchema
from gym_app.validators import SchemaValidator


class MemberController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.member_component = MemberComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.json_schemas.member_schemas')
        self.schema = MemberSchema()

    def list(self, request, gym_pk=None):
        name_filter = request.GET.get("name", None)
        all_members = self.member_component.fetch_all_members(gym_pk)
        if name_filter:
            name_filter_lower = name_filter.lower()
            filtered_members = [
                member
                for member in all_members
                if name_filter_lower in member.name.lower()
            ]
        else:
            filtered_members = all_members

        serialized_data = self.schema.dump(filtered_members, many=True)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def retrieve(self, request, gym_pk=None, pk=None):
        member = self.member_component.fetch_member_by_id(gym_pk, pk)
        serialized_data = self.schema.dump(member)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def create(self, request, gym_pk=None):
        data = request.data.copy()
        data["gym"] = gym_pk

        validation_error = self.validator.validate_data('CREATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)
        if 'birth_date' in data and isinstance(data['birth_date'], str):
            data['birth_date'] = datetime.fromisoformat(data['birth_date']).date()
        member = self.member_component.create_member(gym_pk, data)
        serialized_data = self.schema.dump(member)
        return Response(serialized_data, status=status.HTTP_201_CREATED)

    def update(self, request, gym_pk=None, pk=None):
        data = request.data.copy()
        data["gym"] = gym_pk

        validation_error = self.validator.validate_data('UPDATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)
        if 'birth_date' in data and isinstance(data['birth_date'], str):
            data['birth_date'] = datetime.fromisoformat(data['birth_date']).date()
        member = self.member_component.modify_member(gym_pk, pk, data)
        serialized_data = self.schema.dump(member)
        return Response(serialized_data, status=status.HTTP_200_OK)

    def partial_update(self, request, gym_pk=None, pk=None):
        return self.update(request, gym_pk=gym_pk, pk=pk)

    def destroy(self, request, gym_pk=None, pk=None):
        self.member_component.remove_member(gym_pk, pk)
        return Response({"message": "Member deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
