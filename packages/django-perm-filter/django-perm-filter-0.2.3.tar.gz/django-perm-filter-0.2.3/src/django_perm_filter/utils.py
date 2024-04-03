import logging

from django.conf import settings
from django.contrib import admin
from django.db.models import QuerySet
from django.utils.module_loading import import_string

from django_perm_filter.settings import api_settings

logger = logging.getLogger(__name__)


def sort_perms(actions):
    # Split each string by "_" and sort based on the second element, then the first
    return sorted(actions, key=lambda x: (x.split("_")[1], x.split("_")[0]))


def filter_perms(qs: QuerySet) -> QuerySet:
    """
    Filters a queryset by excluding permissions specified in the HIDE_PERMS setting.

    Parameters:
    qs (QuerySet): The initial queryset to filter.

    Returns:
    QuerySet: The filtered queryset.
    """
    for perm in api_settings.HIDE_PERMS:
        if "." in perm:
            app, model = perm.split(".")
            qs = qs.exclude(content_type__app_label=app, codename=model)
        else:
            qs = qs.exclude(content_type__app_label=perm)

    return qs


def unregister_models() -> None:
    """
    Unregisters models specified in the UNREGISTER_MODELS setting.

    This function will attempt to import and unregister each model specified in the setting.
    If a model cannot be found or an error occurs during unregistering, a warning will be logged.

    Raises:
    ModuleNotFoundError: If the model module cannot be imported.
    RuntimeError: If an error occurs during unregistering.
    """
    if hasattr(settings, "PERM_FILTER"):
        for model_str in api_settings.UNREGISTER_MODELS:
            try:
                model = import_string(model_str)
                if admin.site.is_registered(model):
                    admin.site.unregister(model)
            except (ModuleNotFoundError, RuntimeError) as e:
                logger.warning(
                    "%s %s",
                    str(e),
                    "Ensure the module is installed and/or added to INSTALLED_APPS if need be.",
                )
