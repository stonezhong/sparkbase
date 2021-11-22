import re
from jsonschema import validate, validators, Draft7Validator
from jsonschema.exceptions import ValidationError
from datetime import datetime
from copy import deepcopy

from .validators import VALIDATORS

from .models import CreateDataLakeInput

types = {
    "datetime_string": {
        "type": "string",
        "is_datetime_string": { }
    }
}


model_classes = [
    CreateDataLakeInput
]

def validate_model(model_class, data):
    MyValidator = validators.extend(
        Draft7Validator,
        validators = VALIDATORS,
    )
    models = {}
    for tmp_model_class in model_classes:
        models[tmp_model_class.__name__] = tmp_model_class.schema

    schema = {
        "types": deepcopy(types),
        "models": models,
        "$ref": f"#/models/{model_class.__name__}"
    }
    my_validator = MyValidator(schema=schema)
    my_validator.validate(data)


def json_to_model(model_class, data):
    validate_model(model_class, data)
    return model_class.from_json(data)

