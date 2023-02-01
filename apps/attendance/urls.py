from django.urls import path, include
from rest_framework import routers

from .views import (
    AnnouncementViewset,
    AttendanceViewset,
    CheckoutView,
)

router = routers.DefaultRouter()

router.register(r'announcements', AnnouncementViewset,
                basename='company_announcements')
router.register(r'attendance', AttendanceViewset,
                basename='employee-attendance')

urlpatterns = [
    path('api2/', include(router.urls)),
    path('api2/attendance/checkout/<int:pk>', CheckoutView.as_view()),
]
