from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf.urls.static import static
from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation: Employee Monitoring Testbed",
        default_version="v1",
        description='This documentation contains all the APIs created in the backend \
        for the core functionality of "Employee Monitoring Testbed" application. The \
        rights for this application belong to "Expert System Solution", and nothing of \
        the code or application may be distributed without prior approval of the governing body. \
        That is, \"Expert System Solution\" at Zahoor Elahi road. \
        You can contact the developer at osamaimran135@gmail.com',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="osamaimran135@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("user/", include("apps.authentication.urls")),
    path("behavior/", include("apps.violations.urls")),
    path("live-API/", include("apps.attendance.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
