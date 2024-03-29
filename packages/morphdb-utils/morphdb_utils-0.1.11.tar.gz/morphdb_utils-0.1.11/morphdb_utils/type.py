from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, TypedDict


class NullValue(Enum):
    NULL_VALUE = 0


class ListValue(TypedDict):
    values: List["Value"]


class Struct(TypedDict):
    fields: Dict[str, "Value"]


class Value(TypedDict):
    kind: Dict[str, Any]


class SqlResultRowResponse(TypedDict):
    value: Dict[str, Value]


@dataclass
class SqlResultResponse:
    headers: List[str]
    rows: List[SqlResultRowResponse]


@dataclass
class SignedUrlResponse:
    url: str
