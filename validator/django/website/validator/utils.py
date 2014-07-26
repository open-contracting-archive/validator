import json

from jsonschema import validate
from jsonschema.exceptions import ValidationError


def validate_against_schema(schema_name="release-schema", raw_data=""):
    status = 'input-valid'
    error = None

    schema = json.load(open("validator/schemas/%s.json" % schema_name))

    try:
        data = json.loads(raw_data)
    except ValueError, e:
        status = 'input-error'
        error = e
        return status, error
    
    try:
        validate(data, schema)
    except ValidationError, e:
        status = 'validation-error'
        error = e

        return status, error

    return status, error
