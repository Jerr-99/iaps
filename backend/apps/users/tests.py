from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.users.models import User, UserPermission
from apps.users.views import UserViewSet, UserPermissionViewSet


class UserRBACAPITestCase(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.admin = User.objects.create_user(
            username="test_admin",
            email="admin@example.com",
            password="testpass123",
            role=User.ROLE_ADMIN,
            is_staff=True,
        )

        cls.supervisor = User.objects.create_user(
            username="test_supervisor",
            email="supervisor@example.com",
            password="testpass123",
            role=User.ROLE_SUPERVISOR,
        )

        cls.auditor = User.objects.create_user(
            username="test_auditor",
            email="auditor@example.com",
            password="testpass123",
            role=User.ROLE_AUDITOR,
        )

        cls.finance_manager = User.objects.create_user(
            username="test_finance_manager",
            email="finance@example.com",
            password="testpass123",
            role=User.ROLE_FINANCE_MANAGER,
        )

        cls.factory = APIRequestFactory()

    # =========================================================================
    # HELPERS
    # =========================================================================

    def call_list(self, user):

        request = self.factory.get(
            "/api/users/users/"
        )

        force_authenticate(
            request,
            user=user,
        )

        view = UserViewSet.as_view({
            "get": "list"
        })

        return view(request)

    def call_create(self, user, username="created_user"):

        request = self.factory.post(
            "/api/users/users/",
            {
                "username": username,
                "email": f"{username}@example.com",
                "password": "testpass123",
                "password_confirm": "testpass123",
                "role": User.ROLE_AUDITOR,
            },
            format="json",
        )

        force_authenticate(
            request,
            user=user,
        )

        view = UserViewSet.as_view({
            "post": "create"
        })

        return view(request)

    # =========================================================================
    # ROLE TESTS
    # =========================================================================

    def test_user_roles_are_correct(self):

        self.assertTrue(self.admin.is_admin)
        self.assertTrue(self.supervisor.is_supervisor)
        self.assertTrue(self.auditor.is_auditor)
        self.assertTrue(
            self.finance_manager.is_finance_manager
        )

    # =========================================================================
    # USER LIST RBAC
    # =========================================================================

    def test_admin_can_view_all_users(self):

        response = self.call_list(
            self.admin
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertGreaterEqual(
            response.data["count"],
            4,
        )

    def test_supervisor_can_only_view_self(self):

        response = self.call_list(
            self.supervisor
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertEqual(
            response.data["results"][0]["id"],
            self.supervisor.id,
        )

    def test_auditor_can_only_view_self(self):

        response = self.call_list(
            self.auditor
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertEqual(
            response.data["results"][0]["id"],
            self.auditor.id,
        )

    def test_finance_manager_can_only_view_self(self):

        response = self.call_list(
            self.finance_manager
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.assertEqual(
            response.data["count"],
            1,
        )

        self.assertEqual(
            response.data["results"][0]["id"],
            self.finance_manager.id,
        )

    # =========================================================================
    # USER CREATION RBAC
    # =========================================================================

    def test_admin_can_create_user(self):

        response = self.call_create(
            self.admin,
            "created_by_admin",
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            User.objects.filter(
                username="created_by_admin"
            ).exists()
        )

    def test_supervisor_cannot_create_user(self):

        response = self.call_create(
            self.supervisor,
            "created_by_supervisor",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_auditor_cannot_create_user(self):

        response = self.call_create(
            self.auditor,
            "created_by_auditor",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_finance_manager_cannot_create_user(self):

        response = self.call_create(
            self.finance_manager,
            "created_by_finance_manager",
        )

        self.assertEqual(
            response.status_code,
            403,
        )
class UserManagementRBACAPITestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username="manage_admin",
            email="manage_admin@example.com",
            password="testpass123",
            role=User.ROLE_ADMIN,
            is_staff=True,
        )

        cls.supervisor = User.objects.create_user(
            username="manage_supervisor",
            email="manage_supervisor@example.com",
            password="testpass123",
            role=User.ROLE_SUPERVISOR,
        )

        cls.auditor = User.objects.create_user(
            username="manage_auditor",
            email="manage_auditor@example.com",
            password="testpass123",
            role=User.ROLE_AUDITOR,
        )

        cls.target = User.objects.create_user(
            username="manage_target",
            email="manage_target@example.com",
            password="testpass123",
            role=User.ROLE_AUDITOR,
        )

        cls.factory = APIRequestFactory()

    def call_view(self, user, method, action, pk, data=None):
        request = getattr(self.factory, method)(
            f"/api/users/users/{pk}/",
            data or {},
            format="json",
        )

        force_authenticate(request, user=user)

        view = UserViewSet.as_view({
            method: action,
        })

        return view(request, pk=pk)

    def test_admin_can_update_user(self):
        response = self.call_view(
            self.admin,
            "put",
            "update",
            self.target.id,
            {
                "username": self.target.username,
                "email": self.target.email,
                "first_name": "Updated",
                "last_name": self.target.last_name,
                "role": User.ROLE_AUDITOR,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.target.refresh_from_db()

        self.assertEqual(
            self.target.first_name,
            "Updated",
        )

    def test_supervisor_cannot_update_user(self):
        response = self.call_view(
            self.supervisor,
            "put",
            "update",
            self.target.id,
            {
                "username": self.target.username,
                "email": self.target.email,
                "first_name": "Blocked",
                "role": User.ROLE_AUDITOR,
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_auditor_cannot_update_user(self):
        response = self.call_view(
            self.auditor,
            "put",
            "update",
            self.target.id,
            {
                "username": self.target.username,
                "email": self.target.email,
                "first_name": "Blocked",
                "role": User.ROLE_AUDITOR,
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_user(self):
        target = User.objects.create_user(
            username="delete_target",
            email="delete_target@example.com",
            password="testpass123",
            role=User.ROLE_AUDITOR,
        )

        response = self.call_view(
            self.admin,
            "delete",
            "destroy",
            target.id,
        )

        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            User.objects.filter(id=target.id).exists()
        )

    def test_supervisor_cannot_delete_user(self):
        response = self.call_view(
            self.supervisor,
            "delete",
            "destroy",
            self.target.id,
        )

        self.assertEqual(response.status_code, 403)

    def test_auditor_cannot_delete_user(self):
        response = self.call_view(
            self.auditor,
            "delete",
            "destroy",
            self.target.id,
        )

        self.assertEqual(response.status_code, 403)

class UserPermissionRBACAPITestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_user(
            username="permission_admin",
            email="permission_admin@example.com",
            password="testpass123",
            role=User.ROLE_ADMIN,
            is_staff=True,
        )

        cls.supervisor = User.objects.create_user(
            username="permission_supervisor",
            email="permission_supervisor@example.com",
            password="testpass123",
            role=User.ROLE_SUPERVISOR,
        )

        cls.auditor = User.objects.create_user(
            username="permission_auditor",
            email="permission_auditor@example.com",
            password="testpass123",
            role=User.ROLE_AUDITOR,
        )

        cls.finance_manager = User.objects.create_user(
            username="permission_finance",
            email="permission_finance@example.com",
            password="testpass123",
            role=User.ROLE_FINANCE_MANAGER,
        )

        cls.target = User.objects.create_user(
            username="permission_target",
            email="permission_target@example.com",
            password="testpass123",
            role=User.ROLE_AUDITOR,
        )

        cls.permission = UserPermission.objects.create(
            user=cls.target,
            permission_code="risk.view_assessment",
            description="Test permission",
            is_granted=True,
        )

        cls.factory = APIRequestFactory()

    def call_view(self, user, method, action, pk=None, data=None):

        path = "/api/users/permissions/"

        if pk is not None:
            path += f"{pk}/"

        request = getattr(self.factory, method)(
            path,
            data or {},
            format="json",
        )

        force_authenticate(request, user=user)

        view = UserPermissionViewSet.as_view({
            method: action,
        })

        if pk is not None:
            return view(request, pk=pk)

        return view(request)

    def test_admin_can_create_permission(self):

        response = self.call_view(
            self.admin,
            "post",
            "create",
            data={
                "user": self.target.id,
                "permission_code": "risk.edit_assessment",
                "description": "Edit assessment",
                "is_granted": True,
            },
        )

        self.assertEqual(response.status_code, 201)

    def test_supervisor_cannot_create_permission(self):

        response = self.call_view(
            self.supervisor,
            "post",
            "create",
            data={
                "user": self.target.id,
                "permission_code": "risk.edit_assessment",
                "description": "Edit assessment",
                "is_granted": True,
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_auditor_cannot_create_permission(self):

        response = self.call_view(
            self.auditor,
            "post",
            "create",
            data={
                "user": self.target.id,
                "permission_code": "risk.edit_assessment",
                "description": "Edit assessment",
                "is_granted": True,
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_finance_manager_cannot_create_permission(self):

        response = self.call_view(
            self.finance_manager,
            "post",
            "create",
            data={
                "user": self.target.id,
                "permission_code": "risk.edit_assessment",
                "description": "Edit assessment",
                "is_granted": True,
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_can_update_permission(self):

        response = self.call_view(
            self.admin,
            "put",
            "update",
            self.permission.id,
            data={
                "user": self.target.id,
                "permission_code": "risk.view_assessment",
                "description": "Updated permission",
                "is_granted": False,
            },
        )

        self.assertEqual(response.status_code, 200)

        self.permission.refresh_from_db()

        self.assertFalse(self.permission.is_granted)

    def test_supervisor_cannot_update_permission(self):

        response = self.call_view(
            self.supervisor,
            "put",
            "update",
            self.permission.id,
            data={
                "user": self.target.id,
                "permission_code": "risk.view_assessment",
                "description": "Blocked update",
                "is_granted": False,
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_auditor_cannot_update_permission(self):

        response = self.call_view(
            self.auditor,
            "put",
            "update",
            self.permission.id,
            data={
                "user": self.target.id,
                "permission_code": "risk.view_assessment",
                "description": "Blocked update",
                "is_granted": False,
            },
        )

        self.assertEqual(response.status_code, 403)

    def test_admin_can_delete_permission(self):

        permission = UserPermission.objects.create(
            user=self.target,
            permission_code="risk.delete_assessment",
            description="Delete permission",
            is_granted=True,
        )

        response = self.call_view(
            self.admin,
            "delete",
            "destroy",
            permission.id,
        )

        self.assertEqual(response.status_code, 204)

        self.assertFalse(
            UserPermission.objects.filter(
                id=permission.id
            ).exists()
        )

    def test_supervisor_cannot_delete_permission(self):

        response = self.call_view(
            self.supervisor,
            "delete",
            "destroy",
            self.permission.id,
        )

        self.assertEqual(response.status_code, 403)

    def test_auditor_cannot_delete_permission(self):

        response = self.call_view(
            self.auditor,
            "delete",
            "destroy",
            self.permission.id,
        )

        self.assertEqual(response.status_code, 403)

    def test_finance_manager_cannot_delete_permission(self):

        response = self.call_view(
            self.finance_manager,
            "delete",
            "destroy",
            self.permission.id,
        )

        self.assertEqual(response.status_code, 403)