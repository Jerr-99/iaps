"""URLs for Audit Trail app."""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.audit_trail.views import AuditLogViewSet


app_name = "audit_trail"


router = DefaultRouter()

router.register(
    r"",
    AuditLogViewSet,
    basename="audit-log",
)


urlpatterns = [
    path(
        "",
        include(router.urls),
    ),
]