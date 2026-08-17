"""
URL Configuration for IAPS
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Schema Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API endpoints
    path('api/auth/', include('apps.users.urls', namespace='auth')),
    path('api/engagements/', include('apps.engagements.urls', namespace='engagements')),
    path('api/financial/', include('apps.financial.urls', namespace='financial')),
    path('api/risk/', include('apps.risk.urls', namespace='risk')),
    path('api/planning/', include('apps.planning.urls', namespace='planning')),
    path('api/documents/', include('apps.documents.urls', namespace='documents')),
    path('api/audit-trail/', include('apps.audit_trail.urls', namespace='audit_trail')),
]

# Static and media files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# API root
api_urlpatterns = [
    path('', include(urlpatterns)),
]
