from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.module_loading import import_string

from django_perm_filter.mixins import PermissionFilterMixin
from django_perm_filter.settings import api_settings

# import contextlib
# from django.contrib.admin.sites import NotRegistered

User = get_user_model()

user_admin = import_string(api_settings.USER_ADMIN)
group_admin = import_string(api_settings.GROUP_ADMIN)


class UserAdmin(PermissionFilterMixin, user_admin):
    """Custom User Admin with permission filtering."""


class GroupAdmin(PermissionFilterMixin, group_admin):
    """Custom Group Admin with permission filtering."""


# Override default registered Admin for User and Group
# with contextlib.suppress(NotRegistered):
#     admin.site.unregister(User)

# with contextlib.suppress(NotRegistered):
#     admin.site.unregister(Group)

# Register the custom User/Group Admin
if admin.site.is_registered(User):
    admin.site.unregister(User)

admin.site.register(User, UserAdmin)

if admin.site.is_registered(Group):
    admin.site.unregister(Group)

admin.site.register(Group, GroupAdmin)
