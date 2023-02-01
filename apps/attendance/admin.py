from django.contrib import admin
from .models import (
    Announcements,
    Attendance,
    PaidLeaves,
)


admin.site.register(Attendance)
admin.site.register(Announcements)
admin.site.register(PaidLeaves)
