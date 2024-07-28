import os
import django
from django.conf import settings
import pytest  # type: ignore

# Set up Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gym_management.settings")
django.setup()


@pytest.fixture(autouse=True)
def setup_django_db():
    # Use an in-memory database for testing
    settings.DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
