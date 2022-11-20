from django.db import models
from apps.authentication.models import User


class RegisteredComplaints(models.Model):

    case_status_choices = (("Pending", "Pending"),
                           ("In-Progress", "In-Progress"),
                           ("Closed", "Closed"))

    registered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_against =  models.ForeignKey(User, on_delete=models.CASCADE)
    complaint_date = models.DateField()
    case_status = models.CharField(max_lenght=20, choices=case_status_choices)
    negative_score = models.FloatField()


class Violations(models.Model):
    name = models.CharField(max_length=30)
    desc = models.TextField()


class ViolationLogs(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    violation = models.ForeignKey(Violations, on_delete=models.CASCADE)
