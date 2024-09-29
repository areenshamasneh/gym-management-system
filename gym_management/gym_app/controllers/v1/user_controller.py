from rest_framework import status, viewsets  # type: ignore
from rest_framework.response import Response  # type: ignore

from gym_app.components import UserComponent
from gym_app.serializers import UserSchema
from gym_app.validators import SchemaValidator


class UserController(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_component = UserComponent()
        self.validator = SchemaValidator(schemas_module_name='gym_app.json_schemas.user_schemas')
        self.schema = UserSchema()

    def retrieve(self, request, pk=None):
        user = self.user_component.fetch_user_by_id(pk)
        serialized_user = self.schema.dump(user)
        return Response(serialized_user)

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

    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = self.user_component.authenticate_user(username, password)
        if user:
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
