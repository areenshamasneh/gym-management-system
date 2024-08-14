import importlib
import logging
from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)


class SchemaValidator:
    def __init__(self, schemas_module_name):
        self.schemas_module_name = schemas_module_name

    def _get_schema(self, schema_name):
        schemas_module = importlib.import_module(self.schemas_module_name)
        schema = getattr(schemas_module, schema_name, None)
        if schema is None:
            logger.error(f"Schema {schema_name} not found in module {self.schemas_module_name}")
        return schema

    def validate_data(self, schema_name, data):
        schema = self._get_schema(schema_name)
        try:
            validate(instance=data, schema=schema)
        except ValidationError as e:
            logger.error(f"Schema validation error: {e.message}")
            return e.message
        except Exception as e:
            logger.error(f"Unexpected error during validation: {e}")
            return "An unexpected error occurred during validation."
        return None
