from rest_framework import status  # type: ignore
from rest_framework import viewsets  # type: ignore
from rest_framework.response import Response  # type: ignore

from gym_app.components import MemberComponent
from gym_app.serializers import MemberSerializer


class MemberViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.member_component = MemberComponent()

    def list(self, request, gym_id=None):
        name_filter = request.GET.get("name", None)
        all_members = self.member_component.fetch_all_members(gym_id)

        if name_filter:
            filtered_members = [
                member
                for member in all_members
                if name_filter.lower() in member.name.lower()
            ]
        else:
            filtered_members = all_members

        serializer = MemberSerializer(filtered_members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, gym_id=None, pk=None):
        member = self.member_component.fetch_member_by_id(gym_id, pk)
        serializer = MemberSerializer(member)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, gym_id=None):
        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            member = self.member_component.add_member(gym_id, serializer.validated_data)
            response_serializer = MemberSerializer(member)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, gym_id=None, pk=None):
        serializer = MemberSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            member = self.member_component.modify_member(
                gym_id, pk, serializer.validated_data
            )
            response_serializer = MemberSerializer(member)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, gym_id=None, pk=None):
        return self.update(request, gym_id, pk)

    def destroy(self, request, gym_id=None, pk=None):
        self.member_component.remove_member(gym_id, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
