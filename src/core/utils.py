import logging

from prefect import task
from utils.requests import with_session, make_request, RetryPolicy, RequestError


@task
async def get_repo_info(repo_owner: str, repo_name: str, logger: logging.Logger):
    """Get info about a repo - will retry twice on failure."""
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

    # Define retry policy (optional)
    retry_policy = RetryPolicy(max_attempts=2, logger=logger)

    async with with_session() as session:
        try:
            repo_info = await make_request(
                session, "GET", url, retry_policy=retry_policy, logger=logger
            )
            return repo_info
        except RequestError as e:
            logger.error(f"Failed to fetch repo info: {e}")
            raise


@task
async def get_contributors(repo_info: dict, logger: logging.Logger):
    """Get contributors for a repo."""
    contributors_url = repo_info["contributors_url"]

    async with with_session() as session:
        try:
            contributors = await make_request(
                session, "GET", contributors_url, logger=logger
            )
            return contributors
        except RequestError as e:
            logger.error(f"Failed to fetch contributors: {e}")
            raise
