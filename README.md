# Prefect Project Template

## Getting Started

1. Create another repo, using this repo as template
2. Clone the repository
3. Run `make setup PROJECT_NAME="My New App"`.
4. Run `git push`
5. Run `make install`
6. Update your default `.env` with all the required configurations
7. Run `make push-secrets`
8. You should now be setup to focus on your bussiness logic, to ensure this do the following:
   - Run `make run`: Just to make sure bussiness logic template runs locally
   - Run `make deploy dev`: To ensure you're able to deploy to prefect
   - Run `make trigger dev`: To trigger a flow run in prefect and make sure everything works as intended