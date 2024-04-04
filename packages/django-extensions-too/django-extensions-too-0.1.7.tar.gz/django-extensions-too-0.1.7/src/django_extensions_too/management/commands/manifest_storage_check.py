import json

from django.conf import settings
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from django.core.management import call_command
from django.core.management.base import BaseCommand


def recommend_storage(storage) -> str:
    """Recommend a storage backend."""
    storages = {"staticfiles": {"BACKEND": f"{storage}"}}
    return json.dumps(storages, indent=4)


class Command(BaseCommand):
    help = "Check manifest static files as if we were in production."

    def add_arguments(self, parser):
        parser.add_argument("--path", default="admin/css/base.css")

    def handle(self, *args, **options):
        """
        Test manifest static file storage locally against a specific file path.
        eg - python manage.py manifest_check admin/css/base.css
        """

        staticfiles_storages = [
            "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
            "whitenoise.storage.CompressedManifestStaticFilesStorage",
        ]

        # Force DV to be False and collect static files
        settings.DEBUG = False
        call_command("collectstatic", interactive=False)

        if settings.STATICFILES_STORAGE is not None and not any(
            x in settings.STATICFILES_STORAGE for x in staticfiles_storages
        ):
            self.stdout.write("Ensure ONE of the following backends is in settings")
            for storage in staticfiles_storages:
                storage_backend = recommend_storage(storage)
                self.stdout.write(f"STORAGES = {storage_backend}")

        # Ok, let's see...
        self.stdout.write(f"DEBUG: {settings.DEBUG}")
        self.stdout.write(f"STATIC_ROOT: {settings.STATIC_ROOT}")
        url = ManifestStaticFilesStorage().url(options["path"], force=True)
        self.stdout.write(f'{options["path"]} => {url}')
