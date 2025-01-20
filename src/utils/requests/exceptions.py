from dataclasses import dataclass
from functools import partial
from typing import Any, ClassVar

error_dataclass = partial(dataclass, kw_only=True, slots=True)


@error_dataclass
class RequestError(Exception):
    message: str
    response_content: Any
    method: str
    url: str
    headers: dict[str, str] | None = None

    def __str__(self) -> str:
        return self.message


@error_dataclass
class RequestHTTPError(RequestError):
    status: int


@error_dataclass
class ServerError(RequestError):
    pass


@error_dataclass
class ClientError(RequestError):
    status: ClassVar[int] = 400


@error_dataclass
class UnauthorizedError(ClientError):
    status: ClassVar[int] = 401


@error_dataclass
class NotFoundError(ClientError):
    status: ClassVar[int] = 404


@error_dataclass
class ContentTooLargeError(ClientError):
    status: ClassVar[int] = 413


@error_dataclass
class UnprocessableEntityError(ClientError):
    status: ClassVar[int] = 422


@error_dataclass
class RateLimitError(ClientError):
    status: ClassVar[int] = 429
