import asyncio
import logging

from prefect import flow, tags
from prefect.logging import get_run_logger
from settings import config
from core.utils import get_contributors, get_repo_info


@flow(name=config.app.SLUG, log_prints=False)
async def main(repo_owner: str = "PrefectHQ", repo_name: str = "prefect"):
    """
    Given a GitHub repository, logs the number of stargazers
    and contributors for that repo.
    """
    logger: logging.Logger = get_run_logger()
    logger.setLevel(logging.DEBUG if config.app.DEBUG else logging.INFO)

    repo_info = await get_repo_info(repo_owner, repo_name, logger)
    logger.info(f"Stars 🌠 : {repo_info['stargazers_count']}")

    contributors = await get_contributors(repo_info, logger)
    logger.info(f"Number of contributors 👷: {len(contributors)}")


if __name__ == "__main__":
    with tags(f"app:{config.app.SLUG}", f"env:{config.app.ENVIRONMENT}"):
        asyncio.run(main())
