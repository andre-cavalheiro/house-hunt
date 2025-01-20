from settings import config

from github import Github
from github import GithubException


def upsert_git_access_token(
    secret_name: str = "GIT_ACCESS_TOKEN",
    secret_value: str = config.git.ACCESS_TOKEN.get_secret_value(),
):
    _upsert_github_secret(secret_name, secret_value)


def upsert_git_repository_link(
    secret_name: str = "GIT_REPOSITORY_LINK",
    secret_value: str = config.git.REPOSITORY_LINK,
):
    _upsert_github_secret(secret_name, secret_value)


def upsert_prefect_api_url(
    secret_name: str = "PREFECT_API_URL",
    secret_value: str = config.prefect.API_URL,
):
    _upsert_github_secret(secret_name, secret_value)


def upsert_prefect_api_key(
    secret_name: str = "PREFECT_API_KEY",
    secret_value: str = config.prefect.API_KEY,
):
    _upsert_github_secret(secret_name, secret_value)


def upsert_prefect_work_pool(
    secret_name: str = "PREFECT_WORK_POOL",
    secret_value: str = config.prefect.WORK_POOL,
):
    _upsert_github_secret(secret_name, secret_value)


def upsert_prefect_block_with_github_credentials(
    secret_name: str = "PREFECT_BLOCK_GITHUB_CREDENTIALS",
    secret_value: str = config.blocks.GITHUB_CREDENTIALS,
):
    _upsert_github_secret(secret_name, secret_value)


def upsert_docker_username(
    secret_name: str = "DOCKER_USERNAME",
    secret_value: str = config.docker.USERNAME,
):
    _upsert_github_secret(secret_name, secret_value)


def upsert_docker_password(
    secret_name: str = "DOCKER_PASSWORD",
    secret_value: str = config.docker.PASSWORD.get_secret_value(),
):
    _upsert_github_secret(secret_name, secret_value)


def _upsert_github_secret(
    secret_name: str,
    secret_value: str,
    repo_name: str = "andre-cavalheiro/house-hunt",
    token: str = config.git.ACCESS_TOKEN.get_secret_value(),
):
    """
    Upserts (inserts or updates) a GitHub secret in a repository.
    :param secret_name: The name of the secret to create or update.
    :param secret_value: The value of the secret to store.
    :param repo_name: Repository name in the format 'owner/repo'.
    :param token: GitHub personal access token with repo access.
    """
    github = Github(token)
    repo = github.get_repo(repo_name)

    try:
        repo.create_secret(secret_name, secret_value, secret_type="actions")
        print("Secret %s upserted in %s" % (secret_name, repo_name))
    except GithubException as e:
        print("Error upserting secret: %s" % e)
