from django.contrib import admin
from .models import (
    RegisteredComplaints,
    Violations,
    ViolationLogs,
)


admin.site.register(RegisteredComplaints)
admin.site.register(Violations)
admin.site.register(ViolationLogs)
