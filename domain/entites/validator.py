from typing_extensions import Annotated

from pydantic import AfterValidator


def is_positive(value: int) -> int:
    if value <= 0:
        raise ValueError(f"{value} is not positive")
    return value


def is_filled(value: str) -> str:
    if not len(value.strip()):
        raise ValueError(f"{value} is blank")
    return value


def validate_equal_type(obj_a: object, obj_b: object) ->bool:
    if type(obj_a) != type(obj_b):
        raise ValueError(f"{obj_a} is {type(obj_a)}, {obj_b} is {type(obj_b)}")
    return True


PositveNumber = Annotated[int, AfterValidator(is_positive)]
NotBlankStr = Annotated[str, AfterValidator(is_filled)]
