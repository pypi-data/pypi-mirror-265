import logging
import sys
from collections import defaultdict
from pathlib import Path

from django.apps import apps
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand
from django.db import models

logger = logging.getLogger(__name__)

# -----------------------------------------------------------------------------


def walk_folder(storage, base="/"):
    """
    Recursively walks a folder, using Django's File Storage.
    :param storage: <Storage>
    :param base: <str> The base folder
    :yields: A tuple of base, subfolders, files
    """

    folders, files = storage.listdir(base)

    for subfolder in folders:
        new_base = str(Path(base, subfolder))
        yield from walk_folder(storage, new_base)
    yield base, folders, files


class Command(BaseCommand):
    help = "Deletes all files in MEDIA_ROOT that are not referenced in the database."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", help="Do not delete anything", action="store_true"
        )

    def handle(self, *args, **options):  # noqa: PLR0912, C901
        # This would call the unreferenced_files management command from
        # django-extensions, but doing it this way means we don't rely on it
        # management.call_command("unreferenced_files", verbosity=0)

        # Get a list of all files under MEDIA_ROOT
        media = set()
        for base, _, files in walk_folder(default_storage, "."):
            for f in files:
                # Ignore sorl thumbnail cache files
                if "cache/" not in str(Path(base)):
                    path = Path(base) / Path(f)
                    media.add(str(path))

        # Get list of all fields (value) for each model (key)
        # that is a FileField or subclass of a FileField
        model_dict = defaultdict(list)
        for model in apps.get_models():
            for field in model._meta.fields:  # noqa: SLF001
                if issubclass(field.__class__, models.FileField):
                    model_dict[model].append(field)

        # Get a list of all files referenced in the database
        referenced = set()
        for model, value in model_dict.items():
            results = model.objects.all().iterator()
            for obj in results:
                for field in value:
                    target_file = getattr(obj, field.name)
                    if target_file:
                        referenced.add(target_file.name)

        # Print each file in MEDIA_ROOT that is not referenced in the database
        not_referenced = media - referenced
        for f in not_referenced:
            if options["dry_run"]:
                sys.stdout.write(f"**DRY-RUN** would delete {f}")
            else:
                default_storage.delete(f)
