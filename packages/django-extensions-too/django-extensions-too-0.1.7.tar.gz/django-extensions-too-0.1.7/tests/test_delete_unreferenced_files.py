import pytest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management import call_command
from django_extensions_too.management.commands.delete_unreferenced_files import (
    walk_folder,
)

from django_project.myapp.models import FakeModel


@pytest.fixture(autouse=True)
def _media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.mark.django_db()
def test_walk_folder():
    # Setup: create some files and folders in the default storage
    base_folder = "test_folder"
    subfolder = "test_subfolder"
    file1 = "file1.txt"
    file2 = "file2.txt"
    default_storage.save(f"{base_folder}/{file1}", ContentFile("Hello, World!"))
    default_storage.save(
        f"{base_folder}/{subfolder}/{file2}", ContentFile("Hello, World!")
    )

    # Call walk_folder and collect the results
    results = list(walk_folder(default_storage, base_folder))

    # Check that the results include the expected folders and files
    assert (base_folder, [subfolder], [file1]) in results
    assert (f"{base_folder}/{subfolder}", [], [file2]) in results


@pytest.mark.django_db()
def test_delete_unreferenced_files(capsys):
    # Setup: create a file that is not referenced by any model
    unreferenced_file_path = "unreferenced.txt"
    with default_storage.open(unreferenced_file_path, "w") as f:
        f.write("This file is not referenced by any model")

    # Setup: create a file that is referenced by a model
    referenced_file_path = "referenced.txt"
    with default_storage.open(referenced_file_path, "w") as f:
        f.write("This file is referenced by a model")
    obj = FakeModel(file=referenced_file_path)
    obj.save()

    # Call the command in dry-run mode and check that it identifies the unreferenced file
    call_command("delete_unreferenced_files", dry_run=True)
    assert unreferenced_file_path in capsys.readouterr().out

    # Call the command not in dry-run mode and check that it deletes the unreferenced file
    call_command("delete_unreferenced_files")
    assert not default_storage.exists(unreferenced_file_path)

    # Check that the referenced file was not deleted
    assert default_storage.exists(referenced_file_path)
