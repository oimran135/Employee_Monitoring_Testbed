from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from .models import *
from .serializers import *


class AttendanceSelf():
    pass


class AttendanceByID():
    pass
