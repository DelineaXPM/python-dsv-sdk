import json
import re

from dataclasses import dataclass
from datetime import datetime

# Based on https://gist.github.com/jaytaylor/3660565
def to_snake_case(camel_case_dict):
    """ Transform to snake case

    Transforms the keys of the given map from camelCase to snake_case.
    """
    return [
        (
            re.compile("([a-z0-9])([A-Z])")
            .sub(r"\1_\2", re.compile(r"(.)([A-Z][a-z]+)").sub(r"\1_\2", k))
            .lower(),
            v,
        )
        for (k, v) in camel_case_dict.items()
    ]


@dataclass
class VaultSecret:
    id: str
    path: str
    attributes: str
    description: str
    data: dict
    created: datetime
    last_modified: datetime
    created_by: str
    last_modified_by: str
    version: float

    DEFAULT_DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    def __init__(self, **kwargs):
        # The REST API returns attributes with camelCase names which we replace
        # with snake_case per Python conventions
        datetime_format = self.DEFAULT_DATETIME_FORMAT
        if "datetime_format" in kwargs:
            datetime_format = kwargs["datetime_format"]
        for k, v in to_snake_case(kwargs):
            # @dataclass does not marshal timestamps into datetimes automatically
            if k in ["created", "last_modified"]:
                v = datetime.strptime(v, datetime_format)
            setattr(self, k, v)
