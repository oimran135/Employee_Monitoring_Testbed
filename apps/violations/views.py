from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import (
    RegisteredComplaints,
    Violations,
    ViolationLogs,
)

from .serializers import (
    ComplaintsSerializer,
    UserViolationsSerializer,
    ViolationsSerializer,
)


class ComplaintsViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintsSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return RegisteredComplaints.objects.all()
        else:
            return RegisteredComplaints.objects.filter(registered_against=self.request.user.id)

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ViolationsLogsViewSet(viewsets.ModelViewSet):

    serializer_class = UserViolationsSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return ViolationLogs.objects.all()
        else:
            return ViolationLogs.objects.filter(employee=self.request.user.id)

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ViolationsViewset(viewsets.ModelViewSet):
    serializer_class = ViolationsSerializer
    queryset = Violations.objects.all()
    permission_classes = [IsAdminUser]
