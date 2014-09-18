import json
from py.path import local

from jsonschema.validators import Draft4Validator as validator


def validate_against_schema(raw_data="", schema_name="release-package-schema"):
    status = 'input-valid'
    error = None

    try:
        data = json.loads(raw_data)
    except (TypeError, ValueError), e:
        status = 'input-error'
        error = e
        return status, error, None

    schema = json.load(
        open(local(__file__).dirname +
             '/schemas/{schema_name}.json'.format(schema_name=schema_name))
    )

    error_list = []
    for n, e in enumerate(validator(schema).iter_errors(data)):
        error_list.append(e)
        if n >= 100:
            break

    if error_list:
        status = 'validation-error'
        return status, error_list, schema

    return status, error, schema
