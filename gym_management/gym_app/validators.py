import json
import logging
import os

from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


class SchemaValidator:
    def __init__(self, schema_dir):
        self.schema_dir = schema_dir

    def _load_schema(self, schema_name):
        schema_path = os.path.join(self.schema_dir, schema_name)
        with open(schema_path) as schema_file:
            return json.load(schema_file)

    def validate_data(self, schema_name, data):
        schema = self._load_schema(schema_name)
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            logger.error(f"Schema validation error: {e.message}")
            return e.message
        except Exception as e:
            logger.error(f"Unexpected error during validation: {e}")
            return "An unexpected error occurred during validation."
        return None
