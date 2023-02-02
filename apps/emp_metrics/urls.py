from django.urls import path, include
from rest_framework import routers
from .views import (
    EmployeeOfTheMonthViewset,
)

router = routers.DefaultRouter()

router.register(r'achievements', EmployeeOfTheMonthViewset, basename='best-employee')

urlpatterns = [
    path('api/', include(router.urls)),
]