from rest_framework import (
    views,
    viewsets,
)

from .models import (
    EmployeeOfTheMonth,
    PerformanceMetrics,
)

from .serializers import (
    EmployeeofMonthSerializer,
    PerformanceSerializer,
)

from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
)


class EmployeePerformanceView(views.APIView):
    pass


class EmployeeOfTheMonthViewset(viewsets.ModelViewSet):
    queryset = EmployeeOfTheMonth.objects.all()
    serializer_class = EmployeeofMonthSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return EmployeeOfTheMonth.objects.all()
        else:
            return EmployeeOfTheMonth.objects.filter(emp_id=self.request.user.id)

    def get_permissions(self):
        if (self.action == 'list') or (self.action == 'retrieve'):
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]
