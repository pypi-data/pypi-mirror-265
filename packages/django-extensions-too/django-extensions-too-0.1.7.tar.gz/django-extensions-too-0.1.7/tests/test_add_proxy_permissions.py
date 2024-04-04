import pytest
from django.core.management import call_command


@pytest.mark.django_db()
def test_add_proxy_permissions(capsys):
    # Call the command capture the output
    call_command("add_proxy_permissions", verbosity=0)

    expected_output = """
    Adding permission myapp | fake proxy model | Can add fake proxy model
Adding permission myapp | fake proxy model | Can change fake proxy model
Adding permission myapp | fake proxy model | Can delete fake proxy model
Adding permission myapp | fake proxy model | Can view fake proxy model
    """

    assert capsys.readouterr().out.strip() == expected_output.strip()
