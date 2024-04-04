import pytest
from django.contrib.auth.models import Permission
from django.core.management import call_command


@pytest.mark.django_db()
def test_get_all_permissions(superuser, capsys):
    # Call the command and capture the output
    call_command("get_all_permissions", verbosity=0)

    # Get all permissions from the database and sort them
    all_permissions = Permission.objects.all().order_by(
        "content_type__app_label", "codename"
    )
    expected_output = "\n".join(
        f"{perm.content_type.app_label}.{perm.codename}" for perm in all_permissions
    ).strip()

    assert capsys.readouterr().out.strip() == expected_output
