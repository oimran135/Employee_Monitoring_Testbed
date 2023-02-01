from django.db import models
from datetime import datetime
from apps.authentication.models import User


class Attendance(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_today = models.DateField(auto_now_add=True)
    check_in = models.DateTimeField(default=datetime.now, blank=True)
    check_out = models.DateTimeField(null=True)
    is_present = models.BooleanField(default=True)


class PaidLeaves(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)


class Checkout(models.Model):
    emp_id = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime_today = models.DateTimeField(auto_now_add=True)


class Announcements(models.Model):
    headline = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
