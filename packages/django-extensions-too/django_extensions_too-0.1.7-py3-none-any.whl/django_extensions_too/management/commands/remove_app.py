from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import connection

from django_extensions_too.management.color import color_style

# -----------------------------------------------------------------------------


class Command(BaseCommand):
    """Removes all traces of an app from the DB."""

    help = "Remove an app (Must be in INSTALLED_APPS before running)"

    def add_arguments(self, parser):
        parser.add_argument("apps", nargs="+", type=str)

    def handle(self, *args, **options):
        self.style = color_style()

        # Get models for all apps we wish to remove
        del_apps = options["apps"]

        for a in del_apps:
            try:
                del_models = apps.get_app_config(a).get_models()
            except LookupError as err:
                del_models = []
                self.stdout.write(self.style.WARN(err))

        if not del_models:
            self.stdout.write(self.style.WARN("Nothing to do..."))
            return

        # Remove Content Types
        self.stdout.write(self.style.INFO("=> Remove Content Types..."))
        ct = ContentType.objects.all().order_by("app_label", "model")
        for c in ct:
            if (c.app_label in del_apps) or (c.model in del_models):
                self.stdout.write(f"Deleting Content Type {c.app_label} {c.model}")
                c.delete()

        # Remove Model Tables
        self.stdout.write(self.style.INFO("=> Remove Model Tables..."))
        for c in ct:
            if (c.app_label in del_apps) or (c.model in del_models):
                self.stdout.write(f"Deleting Table '{c.app_label}_{c.model}'")
                sql = f"""
                SET FOREIGN_KEY_CHECKS=0;
                DROP TABLE {c.app_label}_{c.model};
                SET FOREIGN_KEY_CHECKS=1;"""
                cursor = connection.cursor()
                cursor.execute(sql)

        self.stdout.write(self.style.INFO("=> Remove Migration History..."))
        for a in del_apps:
            sql = "DELETE FROM django_migrations WHERE app=%s;"
            self.stdout.write(f"Deleting Migrations for app '{a}'")
            cursor = connection.cursor()
            cursor.execute(sql, [a])

        self.stdout.write(self.style.INFO("=> Remove Django Log Entries..."))
        sql = "DELETE FROM django_admin_log WHERE content_type_id IS NULL;"
        cursor = connection.cursor()
        cursor.execute(sql)
