from django.db import models
from apps.authentication.models import User


class PerformanceMetrics(models.Model):
    pass


class EmployeeOfTheMonth(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()