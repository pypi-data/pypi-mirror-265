from http import HTTPStatus

from django.urls import reverse


class TestUserAdmin:
    def test_change(self, admin_client, user):
        """Test our PermissionFilterMixin"""
        url = reverse("admin:auth_user_change", kwargs={"object_id": user.pk})
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK


class TestGroupAdmin:
    def test_change(self, admin_client, group):
        """Test our PermissionFilterMixin"""
        url = reverse("admin:auth_group_change", kwargs={"object_id": group.pk})
        response = admin_client.get(url)
        assert response.status_code == HTTPStatus.OK
