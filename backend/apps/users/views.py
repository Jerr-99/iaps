"""
Views for User app
"""

from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import UserProfile, UserPermission
from .permissions import CanManageUsers
from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserPermissionSerializer,
    UserCreateSerializer,
    LoginSerializer,
)

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for IAPS User management.

    RBAC rules:

    Administrator:
        - Can list all users
        - Can retrieve any user
        - Can create users
        - Can update users
        - Can delete users
        - Can manage user accounts

    Supervisor:
        - Can view their own user record
        - Cannot create, update, or delete users

    Auditor:
        - Can view their own user record
        - Cannot create, update, or delete users

    Finance Manager:
        - Can view their own user record
        - Cannot create, update, or delete users

    Unauthenticated:
        - Cannot access protected user endpoints
        - May use registration/login endpoints
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        """
        Apply permissions according to the current action.
        """

        # Public endpoints
        if self.action in ["register", "login"]:
            return [AllowAny()]

        # User-management operations are Administrator-only
        if self.action in [
            "create",
            "update",
            "partial_update",
            "destroy",
        ]:
            return [CanManageUsers()]

        # All other user operations require authentication
        return [IsAuthenticated()]

    def get_queryset(self):
        """
        Administrators can see all users.

        Other authenticated users can only see themselves.
        """

        if not self.request.user.is_authenticated:
            return User.objects.none()

        if (
            self.request.user.is_superuser
            or self.request.user.role == User.ROLE_ADMIN
        ):
            return User.objects.all()

        return User.objects.filter(
            id=self.request.user.id
        )

    # =========================================================================
    # CURRENT USER
    # =========================================================================

    @action(
        detail=False,
        methods=["GET"],
    )
    def me(self, request):
        """
        Get the currently authenticated user's information.
        """

        serializer = self.get_serializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    # =========================================================================
    # PUBLIC REGISTRATION
    # =========================================================================

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[AllowAny],
    )
    def register(self, request):
        """
        Register a new user.

        NOTE:
        This endpoint is intentionally public for now.

        For the production IAPS RBAC model, registration should
        normally be disabled or restricted so that only an
        Administrator can create accounts.

        The protected ModelViewSet create endpoint is Administrator-only.
        """

        serializer = UserCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                UserSerializer(user).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # =========================================================================
    # LOGIN
    # =========================================================================

    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[AllowAny],
    )
    def login(self, request):
        """
        Temporary username/password login.

        This will eventually be replaced by the Keycloak
        authentication flow.
        """

        serializer = LoginSerializer(
            data=request.data
        )

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            return Response(
                {
                    "user": UserSerializer(user).data,
                    "message": (
                        "Login successful. "
                        "Please configure Keycloak for production."
                    ),
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # =========================================================================
    # UPDATE OWN PROFILE
    # =========================================================================

    @action(
        detail=True,
        methods=["PUT"],
        permission_classes=[IsAuthenticated],
    )
    def update_profile(self, request, pk=None):
        """
        Update a user's profile information.

        A normal user may update their own profile.

        Administrators may update another user's profile.
        """

        user = self.get_object()

        if (
            request.user != user
            and not request.user.is_superuser
            and request.user.role != User.ROLE_ADMIN
        ):
            return Response(
                {
                    "detail": (
                        "You do not have permission "
                        "to edit this user."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    # =========================================================================
    # CHANGE PASSWORD
    # =========================================================================

    @action(
        detail=True,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
    )
    def change_password(self, request, pk=None):
        """
        Change a user's password.

        Users can change their own password.

        Administrators can change another user's password.
        """

        user = self.get_object()

        is_admin = (
            request.user.is_superuser
            or request.user.role == User.ROLE_ADMIN
        )

        if request.user != user and not is_admin:
            return Response(
                {
                    "detail": (
                        "You do not have permission "
                        "to change this user's password."
                    )
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        old_password = request.data.get(
            "old_password"
        )

        new_password = request.data.get(
            "new_password"
        )

        # When an administrator changes another user's password,
        # the old password is not required.
        if request.user == user and not old_password:
            return Response(
                {
                    "detail": (
                        "old_password is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not new_password:
            return Response(
                {
                    "detail": (
                        "new_password is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Normal user must provide the correct old password.
        if request.user == user:
            if not user.check_password(old_password):
                return Response(
                    {
                        "detail": (
                            "Old password is incorrect."
                        )
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        user.set_password(new_password)
        user.save()

        return Response(
            {
                "message": (
                    "Password changed successfully."
                )
            },
            status=status.HTTP_200_OK,
        )


# =============================================================================
# USER PROFILE
# =============================================================================

class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserProfile management.

    Users can only access their own profile.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Return only the authenticated user's profile.
        """

        return UserProfile.objects.filter(
            user=self.request.user
        )

    @action(
        detail=False,
        methods=["GET"],
    )
    def me(self, request):
        """
        Get or create the current user's profile.
        """

        profile, _ = UserProfile.objects.get_or_create(
            user=request.user
        )

        serializer = self.get_serializer(profile)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


# =============================================================================
# USER PERMISSIONS
# =============================================================================

class UserPermissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing custom user permissions.

    Only IAPS Administrators may create, modify, or delete
    custom user permissions.

    Other authenticated users cannot manage permission
    assignments.
    """

    queryset = UserPermission.objects.all()
    serializer_class = UserPermissionSerializer
    permission_classes = [CanManageUsers]

    def get_queryset(self):
        """
        Administrators can view all custom user permissions.

        Non-administrators are denied by CanManageUsers before
        reaching this queryset.
        """
        return UserPermission.objects.all()