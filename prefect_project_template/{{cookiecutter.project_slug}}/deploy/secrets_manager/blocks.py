from prefect_github import GitHubCredentials
from settings import config


def upsert_github_access_key(
    block_name: str = config.blocks.GITHUB_CREDENTIALS,
    access_token: str = config.git.ACCESS_TOKEN.get_secret_value(),
):
    """
    Upserts (inserts or updates) a GitHub access key in Prefect's GitHub credentials block.
    :param block_name : The name of the Prefect GitHub credentials block to save or update.
    :param access_token : The GitHub access token to store in the credentials block.
    """
    GitHubCredentials(token=access_token).save(name=block_name, overwrite=True)
