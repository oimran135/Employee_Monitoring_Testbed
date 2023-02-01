from django.urls import path, include
from rest_framework import routers
from .views import (
    ComplaintsViewSet,
    ViolationsViewSet,
)


router = routers.DefaultRouter()

router.register(r'complaints', ComplaintsViewSet, basename='usercomplaints')
router.register(r'violations', ViolationsViewSet, basename='userviolations')

urlpatterns = [
    path('api1/', include(router.urls)),
]
