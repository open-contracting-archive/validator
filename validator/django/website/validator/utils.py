import json
from py.path import local

from jsonschema.validators import Draft4Validator as validator


def validate_against_schema(schema_name="release-schema", raw_data=""):
    status = 'input-valid'
    error = None

    try:
        data = json.loads(raw_data)
    except (TypeError, ValueError), e:
        status = 'input-error'
        error = e
        return status, error, None

    schema_filename = 'release-schema.json'

    scheme_identifier = data.get('publisher', {}).get('scheme')
    if scheme_identifier:
        if 'record-schema.json' in scheme_identifier:
            schema_filename = 'record-schema.json'
        else:
            schema_filename = 'release-schema.json'

    schema = json.load(open(local(__file__).dirname +
                        '/schemas/{schema_filename}'.format(schema_filename=schema_filename)))
    
    error_list = []
    for n, e in enumerate(validator(schema).iter_errors(data)):
        error_list.append(e)
        if n >= 100:
            break
    
    if error_list:
        status = 'validation-error'
        return status, error_list, schema

    return status, error, schema
