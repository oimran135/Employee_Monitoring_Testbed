from django.db import models
from apps.authentication.models import User


class PerformanceMetrics(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    overall_performance = models.IntegerField(default=0)
    punctuality_score = models.IntegerField(default=0)
    productivity_score = models.IntegerField(default=0)
    violations_freq = models.IntegerField(default=0)
    complaint_freq = models.IntegerField(default=0)
    employee_of_month_count = models.IntegerField(default=0)

    # for future application
    dependability = models.IntegerField(default=0)


class EmployeeOfTheMonth(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return self.date
