from rest_framework import serializers
from .models import (
    EmployeeOfTheMonth,
    PerformanceMetrics,
)


class EmployeeofMonthSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeOfTheMonth
        fields = '__all__'


class PerformanceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PerformanceMetrics
        fields = '__all__'
