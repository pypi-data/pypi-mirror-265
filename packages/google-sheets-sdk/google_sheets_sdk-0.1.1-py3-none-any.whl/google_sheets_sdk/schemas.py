from pydantic import BaseModel
from pydantic.networks import HttpUrl


class TokenData(BaseModel):
    iss: str
    sub: str
    aud: str
    iat: float = 0
    exp: float = 0
    scope: HttpUrl
