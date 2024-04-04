import pytest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management import call_command

from django_project.myapp.models import FakeModel


@pytest.mark.django_db()
def test_missing_files(capsys):
    # Create a model instance with a file
    referenced_file_path = "referenced.txt"
    default_storage.save(
        referenced_file_path, ContentFile("This file is referenced by a model")
    )
    obj = FakeModel(file=referenced_file_path)
    obj.save()

    # Delete the referenced file from storage (Oops!)
    default_storage.delete(referenced_file_path)

    call_command("missing_files")

    # Check that the output includes the referenced file
    assert referenced_file_path in capsys.readouterr().out
