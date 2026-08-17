"""
Views for User app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model
from .models import User, UserProfile, UserPermission
from .serializers import (
    UserSerializer, UserProfileSerializer, UserPermissionSerializer,
    UserCreateSerializer, LoginSerializer
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User management
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Admin can see all users, others can only see themselves
        if self.request.user.is_staff or self.request.user.role == 'admin':
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['GET'])
    def me(self, request):
        """Get current user info"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def register(self, request):
        """Register a new user"""
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'], permission_classes=[AllowAny])
    def login(self, request):
        """User login (temporary, will be replaced with Keycloak)"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # In production, this should return JWT token from Keycloak
            return Response({
                'user': UserSerializer(user).data,
                'message': 'Login successful. Please configure Keycloak for production.'
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['PUT'], permission_classes=[IsAuthenticated])
    def update_profile(self, request, pk=None):
        """Update user profile"""
        user = self.get_object()
        if request.user != user and not request.user.is_staff:
            return Response(
                {'detail': 'You do not have permission to edit this user.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        """Change user password"""
        user = self.get_object()
        if request.user != user and not request.user.is_staff:
            return Response(
                {'detail': 'You do not have permission to change this user\'s password.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {'detail': 'Both old_password and new_password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(old_password):
            return Response(
                {'detail': 'Old password is incorrect.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully.'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserProfile management
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only view their own profile
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def me(self, request):
        """Get current user's profile"""
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class UserPermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserPermission management
    """
    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Admin can see all, users can see their own
        if self.request.user.is_staff or self.request.user.role == 'admin':
            return UserPermission.objects.all()
        return UserPermission.objects.filter(user=self.request.user)
