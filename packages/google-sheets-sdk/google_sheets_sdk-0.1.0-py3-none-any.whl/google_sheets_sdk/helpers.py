import functools
from typing import TYPE_CHECKING, Any, Awaitable, Callable

if TYPE_CHECKING:
    from google_sheets_sdk import Client


def check_token_expiration(
    function: Callable[..., Awaitable[dict[str, Any]]],
) -> Callable[..., Awaitable[dict[str, Any]]]:
    @functools.wraps(function)
    async def _check_token_expiration(
        self: "Client",
        *args,
        **kwargs,
    ):
        if not self.is_token_expired():
            self.update_token_data()

        return await function(
            self,
            *args,
            **kwargs,
        )

    return _check_token_expiration
