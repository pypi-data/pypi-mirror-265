import pytest
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.utils.module_loading import import_string
from django_perm_filter.utils import filter_perms
from django_perm_filter.utils import sort_perms
from django_perm_filter.utils import unregister_models


def test_sort_perms():
    actions = ["view_model1", "change_model1", "add_model2", "delete_model2"]
    expected_result = ["change_model1", "view_model1", "add_model2", "delete_model2"]

    result = sort_perms(actions)

    assert result == expected_result


@pytest.mark.django_db()
def test_filter_perms(settings):
    """Test the filter_perms function."""
    settings.PERM_FILTER = {
        "HIDE_PERMS": [
            # Django built-in apps
            "admin",
            "contenttypes",
            "sessions",
            "sites",
            # All-auth
            "account",
            "socialaccount",
            # Django built-in auth permissions
            "auth.view_permission",
            "auth.add_permission",
            "auth.change_permission",
            "auth.delete_permission",
        ],
    }

    qs = Permission.objects.all()
    # print(sort_perms([perm.codename for perm in qs]))

    results = filter_perms(qs)
    # print("-" * 40)
    # print(sort_perms([perm.codename for perm in results]))

    # Ensure that no permissions with the following codenames are returned
    codenames = [
        # admin permissions
        "add_logentry",
        "change_logentry",
        "delete_logentry",
        "view_logentry",
        # contenttype permissions
        "add_contenttype",
        "change_contenttype",
        "delete_contenttype",
        "view_contenttype",
        # session permissions
        "add_session",
        "change_session",
        "delete_session",
        "view_session",
        # site permissions
        "add_site",
        "change_site",
        "delete_site",
        "view_site"
        # auth permissions
        "view_permission",
        "add_permission",
        "change_permission",
        "delete_permission",
        # all auth (account) permissions
        "add_emailaddress",
        "change_emailaddress",
        "delete_emailaddress",
        "view_emailaddress",
        "add_emailconfirmation",
        "change_emailconfirmation",
        "delete_emailconfirmation",
        "view_emailconfirmation",
        # all auth (socialaccount) permissions
        "add_socialaccount",
        "change_socialaccount",
        "delete_socialaccount",
        "view_socialaccount",
    ]
    assert all(
        not any(codename in perm.codename for codename in codenames) for perm in results
    )


def test_unregister_models(settings):
    """Test the unregister_models function."""
    settings.PERM_FILTER = {
        "UNREGISTER_MODELS": [
            "django.contrib.sites.models.Site",
            # All-auth
            "allauth.account.models.EmailAddress",
            "allauth.socialaccount.models.SocialAccount",
            "allauth.socialaccount.models.SocialApp",
            "allauth.socialaccount.models.SocialToken",
        ],
    }
    unregister_models()

    for model_string in settings.PERM_FILTER["UNREGISTER_MODELS"]:
        model = import_string(model_string)
        assert not admin.site.is_registered(model)


def test_unregister_models_logs_if_not_found(settings, caplog):
    # Test model not found
    settings.PERM_FILTER = {"UNREGISTER_MODELS": ["fake_app.models.FakeModel"]}

    # with pytest.raises(ModuleNotFoundError):
    unregister_models()

    assert (
        "No module named 'fake_app' Ensure the module is installed and/or added to INSTALLED_APPS if need be."
        in caplog.text
    )
