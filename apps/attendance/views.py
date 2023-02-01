from datetime import datetime
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)
from rest_framework import viewsets
from .models import (
    Announcements,
    Attendance,
)

from .serializers import (
    AnnouncementSerializer,
    AttendanceSerializer,
)


class AnnouncementViewset(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    queryset = Announcements.objects.all()

    def get_permissions(self):
        if self.action == 'post':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class AttendanceViewset(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Attendance.objects.all()
        else:
            return Attendance.objects.filter(emp_id=self.request.user.id)


class CheckoutView(APIView):

    def patch(self, request, pk=None):
        queryset = Attendance.objects.get(pk=pk)
        serializer = AttendanceSerializer(queryset, data=request.data, partial=True)
        serializer.data['check_out'] = datetime.now
        if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)