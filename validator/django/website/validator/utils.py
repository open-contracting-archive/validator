import json
from py.path import local

from jsonschema.validators import Draft4Validator as validator


def validate_against_schema(schema_name="release-schema", raw_data=""):
    status = 'input-valid'
    error = None

    schema = json.load(open(local(__file__).dirname + '/schemas/%s.json' % schema_name))

    try:
        data = json.loads(raw_data)
    except (TypeError, ValueError), e:
        status = 'input-error'
        error = e
        return status, error
    
    error_list = []
    for n, e in enumerate(validator(schema).iter_errors(data)):
        error_list.append(e)
        if n >= 100:
            break
    
    if error_list:
        status = 'validation-error'
        return status, error_list

    return status, error
