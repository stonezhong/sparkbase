import re
from jsonschema import validate, validators
from jsonschema.exceptions import ValidationError
from datetime import datetime

def is_datetime_string(validator, value, instance, schema):
    p = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}$")
    if not p.match(instance):
        raise ValidationError(f"{instance} does not match the datetime pattern")
    try:
        dt = datetime.strptime(instance, "%Y-%m-%d %H:%M:%S")
    except ValueError as e:
        raise ValidationError(str(e))
    if "min" in value and dt < value['min']:
        raise ValidationError(f"minium value should be {value['min']}")
    if "max" in value and dt > value['max']:
        raise ValidationError(f"maxium value should be {value['max']}, actual value is {dt}")

VALIDATORS = {
    'is_datetime_string': is_datetime_string
}
