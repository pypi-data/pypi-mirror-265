import time as t
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar

from httpx import HTTPStatusError
from jose import jwt

from google_sheets_sdk.helpers import check_token_expiration
from google_sheets_sdk.schemas import TokenData
from google_sheets_sdk.settings import get_settings

if TYPE_CHECKING:
    from google_sheets_sdk import Settings
    from httpx import AsyncClient


@dataclass
class Client:
    settings: ClassVar["Settings"] = get_settings()
    base_url: ClassVar[str] = "https://sheets.googleapis.com/"
    token_data: ClassVar[TokenData] = TokenData(
        iss=settings.CLIENT_EMAIL,
        sub=settings.CLIENT_EMAIL,
        aud=f"{base_url}",
        scope=settings.SCOPE,
    )

    http_client: "AsyncClient"

    def get_token(self) -> str:
        return jwt.encode(
            self.token_data.model_dump(
                mode="json",
            ),
            self.settings.PRIVATE_KEY.replace(r"\n", "\n"),
            headers={
                "kid": self.settings.PRIVATE_KEY_ID,
            },
            algorithm="RS256",
        )

    def update_token_data(self) -> None:
        iat = t.time()
        self.token_data.iat = iat
        self.token_data.exp = iat + 3600

    def is_token_expired(self) -> bool:
        return bool(self.token_data.exp) and (self.token_data.exp - t.time()) > 60

    @check_token_expiration
    async def batch_clear_values(
        self,
        spreadsheet_id: str,
        ranges: list[str],
    ) -> dict[str, Any]:
        try:
            response = await self.http_client.post(
                url=f"{self.base_url}v4/spreadsheets/{spreadsheet_id}/values:batchClear",
                json={
                    "ranges": ranges,
                },
                headers={
                    "Authorization": f"Bearer {self.get_token()}",
                },
            )
            response.raise_for_status()
        except HTTPStatusError as exc:
            print(exc.response.text)
            raise exc
        else:
            return response.json()

    @check_token_expiration
    async def batch_update_values(
        self,
        spreadsheet_id: str,
        data: list[dict[str, list]],
    ) -> dict[str, Any]:
        try:
            response = await self.http_client.post(
                url=f"{self.base_url}v4/spreadsheets/{spreadsheet_id}/values:batchUpdate",
                json={
                    "valueInputOption": "USER_ENTERED",
                    "data": data,
                },
                headers={
                    "Authorization": f"Bearer {self.get_token()}",
                },
            )
            response.raise_for_status()
        except HTTPStatusError as exc:
            print(exc.response.text)
            raise exc
        else:
            return response.json()
