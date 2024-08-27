from rest_framework import status  # type: ignore
from rest_framework import viewsets  # type: ignore
from rest_framework.response import Response  # type: ignore


class HealthCheckViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)
