from typing import Any

from pydantic import BaseModel
from pydantic.networks import HttpUrl


class TokenData(BaseModel):
    iss: str
    sub: str
    aud: str
    iat: float = 0
    exp: float = 0
    scope: HttpUrl


class ValuesRange(BaseModel):
    range: str
    values: list[list[Any]]
