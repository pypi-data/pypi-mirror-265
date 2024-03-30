import json

from pydantic import BaseModel

from .scheduler import Scheduler
from .session import Session

_ignored_runloop_types = [Session, Scheduler]


def _concrete_to_json_compatible(value: int | str | bool | BaseModel) -> any:
    """Recursively convert a value to a JSON parseable type (ie a value fully able to json.dumps()).
    For scalar types, this is simply the value.
    For BaseModel types, this is the result of model_dump().
    For lists / dicts, this needs to be recursively evaluated.
    """
    if isinstance(value, BaseModel):
        return value.model_dump()
    elif isinstance(value, list):
        # Pull out type, recurse
        return [_concrete_to_json_compatible(x) for x in value]
    elif isinstance(value, dict):
        return {k: _concrete_to_json_compatible(v) for k, v in value.items()
                if not any(isinstance(v, x) for x in _ignored_runloop_types)}
    elif any(isinstance(value, t) for t in _ignored_runloop_types):
        return str(value)
    return value


def value_to_json_string(value: int | str | bool | dict | list | BaseModel) -> str:
    """Convert a value to a fully formed JSON string."""
    return json.dumps(_concrete_to_json_compatible(value))
