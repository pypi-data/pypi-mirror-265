from collections import defaultdict

from django.core.files.storage import default_storage as storage
from django.core.management.base import BaseCommand
from django.db import models

# -----------------------------------------------------------------------------


def get_apps_from_cache():
    try:
        from django.apps import apps

        return [
            app.models_module for app in apps.get_app_configs() if app.models_module
        ]
    except ImportError:
        from django.db.models.loading import cache

        return cache.get_apps()


def get_models_from_cache(app):
    try:
        from django.apps import apps

        return apps.get_models(app)
    except ImportError:
        from django.db.models.loading import cache

        return cache.get_models(app)


# -----------------------------------------------------------------------------


class Command(BaseCommand):
    help = "Prints a list of missing files in MEDIA_ROOT."

    def handle(self, *args, **options):  # noqa: C901
        file_list = []

        # Get list of all fields (value) for each model (key)
        # that is a FileField or subclass of a FileField
        model_dict = defaultdict(list)
        for app in get_apps_from_cache():
            for model in get_models_from_cache(app):
                for field in model._meta.fields:  # noqa: SLF001
                    if issubclass(field.__class__, models.FileField):
                        model_dict[model].append(field)

        # Get a list of all files missing in MEDIA_ROOT
        for model, value in model_dict.items():
            all_files = model.objects.all().iterator()
            for obj in all_files:
                for field in value:
                    if target_file := getattr(obj, field.name):
                        file_list.append(target_file.name)  # noqa: PERF401

        # Print list of missing files
        file_list = sorted(set(file_list))
        for f in file_list:
            if not storage.exists(f):
                self.stdout.write(f)
