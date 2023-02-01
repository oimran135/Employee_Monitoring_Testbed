from rest_framework.serializers import ModelSerializer
from apps.authentication.serializers import UserSerializer
from .models import (
    RegisteredComplaints,
    Violations,
    ViolationLogs,
)


class ComplaintsSerializer(ModelSerializer):
    class Meta:
        model = RegisteredComplaints
        fields = '__all__'


class ViolationsSerializer(ModelSerializer):\

    class Meta:
        model = Violations
        fields = '__all__'


class UserViolationsSerializer(ModelSerializer):
    registered_by = UserSerializer()
    violation = ViolationsSerializer()

    class Meta:
        model = ViolationLogs
        fields = ('employee', 'violation', 'violation_date',
                  'registered_by', 'comments')
