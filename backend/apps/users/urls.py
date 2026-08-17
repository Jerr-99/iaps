"""
URL configuration for Users app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserProfileViewSet, UserPermissionViewSet

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'permissions', UserPermissionViewSet, basename='permission')

urlpatterns = [
    path('', include(router.urls)),
]
