from rest_framework import status, viewsets
from rest_framework.response import Response

from gym_app.components import UserComponent
from gym_app.permissions import BasicAuthPermission
from gym_app.serializers import UserSchema
from gym_app.validators import SchemaValidator


class UserController(viewsets.ViewSet):
    permission_classes = [BasicAuthPermission]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_component = UserComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.json_schemas.user_schemas')
        self.schema = UserSchema()

    def list(self, request, *args, **kwargs):
        try:
            users = self.user_component.fetch_all_users()
            serialized_users = self.schema.dump(users, many=True)
            return Response(serialized_users)
        except Exception as e:
            print(f"Error in listing users: {e}")
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None):
        try:
            user = self.user_component.fetch_user_by_id(pk)
            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            serialized_user = self.schema.dump(user)
            return Response(serialized_user)
        except Exception as e:
            print(f"Error in retrieving user: {e}")
            return Response({"detail": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        data = request.data.copy()

        validation_error = self.validator.validate_data('CREATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        user = self.user_component.add_user(data)
        serialized_user = self.schema.dump(user)
        return Response(serialized_user, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        data = request.data.copy()

        validation_error = self.validator.validate_data('UPDATE_SCHEMA', data)
        if validation_error:
            return Response({"error": validation_error}, status=status.HTTP_400_BAD_REQUEST)

        user = self.user_component.modify_user(pk, data)
        serialized_user = self.schema.dump(user)
        return Response(serialized_user)

    def destroy(self, request, pk=None):
        self.user_component.remove_user(pk)
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
