"""
Serializers for User app
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, UserProfile, UserPermission


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'role_display', 'is_active', 'two_fa_enabled',
            'department', 'phone_number', 'job_title',
            'created_at', 'updated_at', 'last_login_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for UserProfile model
    """
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'keycloak_id', 'keycloak_username',
            'bio', 'avatar_url', 'preferred_language',
            'email_notifications', 'dashboard_theme',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'keycloak_id', 'keycloak_username', 'created_at', 'updated_at']


class UserPermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for UserPermission model
    """
    
    class Meta:
        model = UserPermission
        fields = [
            'id', 'user', 'permission_code', 'description',
            'is_granted', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new users
    """
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'role'
        ]
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('password_confirm')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Serializer for user login (will be replaced with Keycloak)
    """
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        data['user'] = user
        return data
