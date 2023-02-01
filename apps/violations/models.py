from django.db import models
from apps.authentication.models import User


class RegisteredComplaints(models.Model):

    case_status_choices = (("Pending", "Pending"),
                           ("In-Progress", "In-Progress"),
                           ("Closed", "Closed"))

    registered_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    registered_against = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, related_name='user_object_set')
    complaint_date = models.DateField(null=True, blank=True)
    case_status = models.CharField(
        max_length=20, choices=case_status_choices, null=True, blank=True)
    negative_score = models.FloatField(null=True, blank=True,)
    comments = models.TextField(null=True, blank=True)


class Violations(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True,)
    desc = models.TextField(null=True, blank=True)
    neg_score = models.IntegerField(default=0)


class ViolationLogs(models.Model):
    employee = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE)
    registered_by = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE, related_name='admin-registerar+')
    violation = models.ForeignKey(
        Violations, null=True, blank=True, on_delete=models.CASCADE)
    violation_date = models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
