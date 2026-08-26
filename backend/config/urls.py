"""
URL configuration for IAPS project.

Intelligent Audit Planning and Risk Assessment System
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from django.http import JsonResponse
from rest_framework.permissions import AllowAny


def api_root(request):
    """
    API root endpoint.
    """
    return JsonResponse({
        "name": "IAPS API",
        "version": "1.0.0",
        "status": "online",
        "description": (
            "Intelligent Audit Planning and Risk Assessment System"
        ),
        "endpoints": {
            "admin": "/admin/",
            "api": "/api/",
            "authentication": "/api/auth/",
            "users": "/api/users/",
            "engagements": "/api/engagements/",
            "financial": "/api/financial/",
            "risk": "/api/risk/",
            "planning": "/api/planning/",
            "documents": "/api/documents/",
            "audit_trail": "/api/audit-trail/",
            "schema": "/api/schema/",
            "swagger": "/api/docs/",
            "redoc": "/api/redoc/",
        }
    })


urlpatterns = [
    # ------------------------------------------------------------------
    # Root
    # ------------------------------------------------------------------
    path('', api_root, name='api-root'),

    # ------------------------------------------------------------------
    # Django Admin
    # ------------------------------------------------------------------
    path('admin/', admin.site.urls),

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    path(
        'api/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),

    path(
        'api/auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),

    # ------------------------------------------------------------------
    # Application APIs
    # ------------------------------------------------------------------
    path(
        'api/users/',
        include('apps.users.urls')
    ),

    path(
        'api/engagements/',
        include('apps.engagements.urls')
    ),

    path(
        'api/financial/',
        include('apps.financial.urls')
    ),

    path(
        'api/risk/',
        include('apps.risk.urls')
    ),

    path(
        'api/planning/',
        include('apps.planning.urls')
    ),

    path(
        'api/documents/',
        include('apps.documents.urls')
    ),

    path(
        'api/audit-trail/',
        include('apps.audit_trail.urls')
    ),

    path(
        "api/", 
        include("config.api.urls")
        ),

    # ------------------------------------------------------------------
    # OpenAPI / Swagger
    # ------------------------------------------------------------------
    path(
        'api/schema/',
        SpectacularAPIView.as_view(
            permission_classes=[AllowAny]
        ),
        name='schema'
    ),

    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(
            url_name='schema',
            permission_classes=[AllowAny]
        ),
        name='swagger-ui'
    ),

    path(
        'api/redoc/',
        SpectacularRedocView.as_view(
            url_name='schema',
            permission_classes=[AllowAny]
        ),
        name='redoc'
    ),
]


# ----------------------------------------------------------------------
# Development media serving
# ----------------------------------------------------------------------

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )