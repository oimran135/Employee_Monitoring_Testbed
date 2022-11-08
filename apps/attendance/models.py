from django.db import models
from apps.authentication.models import User

class Attendance(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_today = models.DateField(auto_now_add=True)
    is_present = models.BooleanField(default=False)


class PaidLeaves(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()


class Checkout(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_today = models.DateTimeField(auto_now_add=True)

