from typing import Optional
import hjson
from dataclasses_json import LetterCase, Undefined, DataClassJsonMixin, config
from functools import wraps


def hjson_config(
    *, undefined=Undefined.EXCLUDE, letter_case=LetterCase.CAMEL, **kwargs
):
    """Return the configuration for dataclass-json."""
    data = config(undefined=undefined, letter_case=letter_case, **kwargs)
    return data["dataclasses_json"]


def using_config(
    *, undefined=Undefined.EXCLUDE, letter_case=LetterCase.CAMEL, **kwargs
) -> "DataClassHjsonMixin":
    """Decorator to set the configuration for dataclass-json."""

    def wrapper(cls) -> "DataClassHjsonMixin":
        cls.dataclass_json_config = hjson_config(
            undefined=undefined, letter_case=letter_case, **kwargs
        )
        return cls

    return wrapper


class DataClassHjsonMixin(DataClassJsonMixin):
    """Mixin class to add HJSON serialization and deserialization to dataclasses."""
    
    dataclass_json_config: Optional[dict] = hjson_config()
    """Configuration for dataclasses-json."""

    @classmethod
    def from_hjson(cls, hjson_str: str) -> "DataClassHjsonMixin":
        """Return an instance of the dataclass from a HJSON string."""
        return cls.from_dict(hjson.loads(hjson_str))

    @wraps(hjson.dumps)
    def to_hjson(self, **kwargs) -> str:
        """Return a HJSON string representation of the dataclass."""
        return hjson.dumps(self.to_dict(), **kwargs)
