from rest_framework.serializers import ModelSerializer
from .models import (
    Announcements,
    Attendance,
)


class AttendanceSerializer(ModelSerializer):

    class Meta:
        model = Attendance
        fields = '__all__'


class AnnouncementSerializer(ModelSerializer):

    class Meta:
        model = Announcements
        fields = '__all__'
