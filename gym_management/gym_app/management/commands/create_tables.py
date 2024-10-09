from sqlalchemy import create_engine
from gym_app.models.models_sqlalchemy import Base
from django.core.management.base import BaseCommand
from gym_management.settings import DATABASE_URL


class Command(BaseCommand):
    help = "Create SQLAlchemy tables"

    def handle(self, *args, **kwargs):
        engine = create_engine(DATABASE_URL)
        Base.metadata.create_all(engine)
        self.stdout.write(self.style.SUCCESS("Successfully created SQLAlchemy tables."))
