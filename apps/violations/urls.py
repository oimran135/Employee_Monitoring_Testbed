from django.urls import path, include
from rest_framework import routers
from .views import (
    ComplaintsViewSet,
    ViolationsLogsViewSet,
    ViolationsViewset,
)


router = routers.DefaultRouter()

router.register(r'complaints', ComplaintsViewSet, basename='usercomplaints')
router.register(r'violations/logs', ViolationsLogsViewSet,
                basename='userviolations')
router.register(r'violations', ViolationsViewset, basename='core-violations')

urlpatterns = [
    path('api1/', include(router.urls)),
]
