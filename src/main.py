import asyncio
import logging

from prefect import flow, tags
from prefect.logging import get_run_logger
from settings import config
from core.simao import main as main_simao


@flow(name=config.app.SLUG, log_prints=False)
async def main(repo_owner: str = "PrefectHQ", repo_name: str = "prefect"):
    """
    Given a GitHub repository, logs the number of stargazers
    and contributors for that repo.
    """
    logger: logging.Logger = get_run_logger()
    logger.setLevel(logging.DEBUG if config.app.DEBUG else logging.INFO)

    main_simao()


if __name__ == "__main__":
    with tags(f"app:{config.app.SLUG}", f"env:{config.app.ENVIRONMENT}"):
        asyncio.run(main())
