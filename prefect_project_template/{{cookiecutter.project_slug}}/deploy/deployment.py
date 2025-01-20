from settings import config
from prefect.runner.storage import GitRepository
from prefect_github import GitHubCredentials
from prefect import flow


if __name__ == "__main__":
    print("Starting deployment script")

    # Set up Git repository source
    print("Configuring Git repository source")
    branch = "main" if config.app.is_production else "develop"
    source = GitRepository(
        url=config.git.REPOSITORY_LINK,
        credentials=GitHubCredentials.load(config.blocks.GITHUB_CREDENTIALS),
        branch=branch,
    )
    print(
        "Git repository configured: %s on branch %s"
        % (config.git.REPOSITORY_LINK, branch)
    )

    # Load flow from source
    print("Loading flow from source")
    try:
        flow = flow.from_source(
            source=source,
            entrypoint="src/main.py:main",
        )
        print("Flow loaded successfully from source")
    except Exception as e:
        print("Failed to load flow from source: %s" % e)
        raise

    # Deploy the flow
    print("Starting deployment of flow")
    try:
        # I need to adjust this to use a DOCKERFILE: https://docs-3.prefect.io/3.0/deploy/infrastructure-examples/docker#automatically-build-a-custom-docker-image-with-a-local-dockerfile

        flow.deploy(
            name=config.app.ENVIRONMENT,
            build=True,  # Build a new image for the flow
            push=True,  # Push the built image to a registry
            work_pool_name=config.prefect.WORK_POOL,
            cron=config.prefect.CRON_SCHEDULE,
            tags=["app:%s" % config.app.SLUG, "env:%s" % config.app.ENVIRONMENT],
            job_variables={"env": {"APP_ENVIRONMENT": "%s" % config.app.ENVIRONMENT}},
            parameters={},
        )
        print("Deployment successful for environment: %s" % config.app.ENVIRONMENT)
    except Exception as e:
        print("Deployment failed: %s", e)
        raise
