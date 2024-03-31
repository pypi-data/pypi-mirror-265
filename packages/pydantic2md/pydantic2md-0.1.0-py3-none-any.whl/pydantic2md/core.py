import textwrap
from collections.abc import Sequence
from typing import Any, List, Optional, Type

from pydantic import BaseModel
from pydantic.fields import FieldInfo

INDENT = 2
NEWLINE = "<br>\r\n"


def indent_to_level(text, level):
    return textwrap.indent(text, " " * INDENT * level)


def get_type_name(type: Type):
    if hasattr(type, '__name__'):
        # Regular types.
        return type.__name__ 
    elif hasattr(type, '_name'):
        if hasattr(type, '__args__'):
            return f"{type._name}[{','.join(map(get_type_name, type.__args__))}]"
        else:
            return type._name
    else:
        return str(type)


def pydantic2md(
    obj: BaseModel, with_title=True, exclude: Optional[List[str]] = None, level=0
) -> str:
    """Convert Pydantic Object to Pydantic

    Args:
        obj: Pydantic Object
        with_title: To Output Class name type as title. Defaults to True.
        exclude: List of fields to exclude. Defaults to None.
        level: Indent level to use. Defaults to 0.

    Returns:
        String of the object converted to markdown.
    """
    exclude = exclude or {}
    response = []
    if with_title:
        response.append(f"{'#' * (level + 1)} {obj.__class__.__name__}" + NEWLINE)
    for field, field_info in obj.model_fields.items():
        if field in exclude:
            continue
        value = getattr(obj, field)
        response.append(parse_field(field, field_info, value, level=level))
    return "".join(response)


def parse_field(field_name: str, field_type: FieldInfo, field_value: Any, level=0) -> str:
    """Translate one field to a string.

    Args:
        field_name: Name of the field.
        field_info: Pydantic FieldInfo.
        field_value: Value of the field.
        level: Indent level to use.

    Info:
        Default translation is to convert to string.

    Returns:
        String of the field translated to Markdown.
    """
    parsed_type = field_type.annotation or type(field_value)
    field_name_parsed = f"{field_name} ({get_type_name(parsed_type)})"
    if isinstance(field_value, Sequence):
        response = [f"{field_name_parsed}:"]
        response += [
            "* " + pydantic2md(v, with_title=False, level=1)
            if isinstance(v, BaseModel)
            else indent_to_level(f"* {v}", level=1)
            for v in field_value
        ]
        str_response = NEWLINE.join(response + [""]) + "\r\n"  # List ends with new lines.
    else:
        # Singular field
        str_response = f"{field_name_parsed}: {field_value}" + NEWLINE
    return indent_to_level(str_response, level=level)
