from rest_framework import viewsets, status
from rest_framework.response import Response

from gym_app.components import MemberComponent
from gym_app.exceptions import ResourceNotFoundException, InvalidInputException
from gym_app.serializers import MemberSerializer
from gym_app.validators import SchemaValidator


class MemberViewSet(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.member_component = MemberComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.schemas.member_schemas')

    def list(self, request, gym_pk=None):
        name_filter = request.GET.get("name", None)

        try:
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

            serializer = MemberSerializer(filtered_members, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except InvalidInputException as e:
            return Response({"errors": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, gym_pk=None, pk=None):
        try:
            member = self.member_component.fetch_member_by_id(gym_pk, pk)
            serializer = MemberSerializer(member)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request, gym_pk=None):
        data = request.data.copy()
        data["gym"] = gym_pk

        validation_error = self.validator.validate_data('CREATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MemberSerializer(data=data)
        if serializer.is_valid():
            try:
                member = self.member_component.create_member(gym_pk, serializer.validated_data)
                response_serializer = MemberSerializer(member)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
            except InvalidInputException as e:
                return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"detail": "An unexpected error occurred."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, gym_pk=None, pk=None):
        data = request.data.copy()
        data["gym"] = gym_pk

        validation_error = self.validator.validate_data('UPDATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MemberSerializer(data=data, partial=True)
        if serializer.is_valid():
            try:
                member = self.member_component.modify_member(gym_pk, pk, serializer.validated_data)
                response_serializer = MemberSerializer(member)
                return Response(response_serializer.data, status=status.HTTP_200_OK)
            except ResourceNotFoundException as e:
                return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
            except InvalidInputException as e:
                return Response({"errors": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"detail": "An unexpected error occurred."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, gym_pk=None, pk=None):
        return self.update(request, gym_pk=gym_pk, pk=pk)

    def destroy(self, request, gym_pk=None, pk=None):
        try:
            self.member_component.remove_member(gym_pk, pk)
            return Response({"message": "Member deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except ResourceNotFoundException as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except InvalidInputException as e:
            return Response({"errors": str(e)}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
