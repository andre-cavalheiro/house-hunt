import logging
import traceback
from contextlib import asynccontextmanager
from typing import Any, Generator, TypeAlias

from aiohttp import ClientTimeout, ContentTypeError

from aiohttp import ClientSession as AiohttpClientSession
from aiohttp.client_exceptions import ClientError as AiohttpClientError
from .exceptions import (
    RequestError,
    ServerError,
    RateLimitError,
    NotFoundError,
)
from tenacity import (
    AsyncRetrying,
    before_sleep_log,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)
from .serializers import json_serialize

ClientSession: TypeAlias = AiohttpClientSession  # Alias for easy reference


class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 5,
        exceptions_to_retry: tuple[type[Exception], ...] = (
            ServerError,
            RateLimitError,
        ),
        wait_multiplier: int = 1,
        wait_max: int = 10,
        wait_min: int = 60,
        reraise: bool = True,
        logger: logging.Logger | None = None,
    ):
        self.max_attempts = max_attempts
        self.exceptions_to_retry = exceptions_to_retry
        self.wait_multiplier = wait_multiplier
        self.wait_max = wait_max
        self.wait_min = wait_min
        self.reraise = reraise
        self.logger = logger

    def retry_attempts(self) -> AsyncRetrying:
        return AsyncRetrying(
            stop=stop_after_attempt(self.max_attempts),
            wait=wait_random_exponential(
                min=self.wait_min, max=self.wait_max, multiplier=self.wait_multiplier
            ),
            before_sleep=before_sleep_log(self.logger, logging.WARNING)
            if self.logger
            else None,
            reraise=self.reraise,
            retry=retry_if_exception_type(self.exceptions_to_retry),
        )


def create_session(
    *, timeout: int = 30, headers: dict[str, str] | None = None, **kwargs: Any
) -> ClientSession:
    return ClientSession(
        timeout=ClientTimeout(total=timeout),
        json_serialize=kwargs.pop(
            "json_serialize", lambda obj: json_serialize(obj).decode()
        ),
        headers=headers,
        **kwargs,
    )


@asynccontextmanager
async def with_session(
    *, timeout: int = 30, headers: dict[str, str] | None = None, **kwargs: Any
) -> Generator[ClientSession, None, None]:
    async with create_session(timeout=timeout, headers=headers, **kwargs) as session:
        yield session


async def make_request(
    session: ClientSession,
    method: str,
    url: str,
    *,
    logger: logging.Logger | None = None,
    retry: bool = True,
    retry_policy: RetryPolicy | None = None,
    none_on_404: bool = False,
    **kwargs: Any,
) -> Any:
    response_content: Any | None = None
    try:
        if not retry:
            response_content = await _make_request(session, method, url, **kwargs)

        if retry_policy is None:
            retry_policy = RetryPolicy(logger=logger)

        async for attempt in retry_policy.retry_attempts():
            with attempt:
                response_content = await _make_request(session, method, url, **kwargs)

        return response_content
    except NotFoundError as e:
        if none_on_404:
            if logger:
                logger.warning(e.message)
            return None
    except RequestError:
        raise
    except Exception as e:
        traceback.print_exc()
        raise RequestError(
            message=f"Unexpected error during {method} {url}: {str(e)}",
            response_content=response_content,
            method=method,
            url=url,
        )


async def _make_request(
    session: ClientSession, method: str, url: str, **kwargs: Any
) -> Any:
    response_content: Any | None = None
    try:
        async with session.request(method, url, **kwargs) as response:
            response.raise_for_status()

            response_content = None
            try:
                response_content = await response.json()
            except ContentTypeError:
                # Fallback to plain text if unsuccessful
                response_content = await response.text()

            return response_content
    except AiohttpClientError as e:
        raise RequestError(
            message=f"Request failed for {method} {url}: {str(e)}",
            response_content=response_content,
            method=method,
            url=url,
        )
