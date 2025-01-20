MAKEFLAGS += --no-print-directory --silent

################################################################################
# Makefile Variables
################################################################################
SHELL := $(or $(shell echo $$SHELL),/bin/sh)

POETRY_VERSION = 1.8.3

VENV_PATH ?= .venv
POETRY_HOME ?= .venv_poetry

PYTHON = $(shell command -v python3)
POETRY = $(POETRY_HOME)/bin/poetry


################################################################################
# Default
################################################################################
.DEFAULT_GOAL := default

.PHONY: default
default:
	@echo "Running default task"
	@$(MAKE) build
	@$(MAKE) install-root
	@$(MAKE) format


################################################################################
# Setup & Install
################################################################################
.PHONY: build
build:
	$(POETRY) build;

.PHONY: install-root
install-root:
	$(POETRY) install --only-root

.PHONY: install-minimal
install-minimal:
	$(POETRY) install --without dev

.PHONY: install
install:
	$(MAKE) install-poetry
	$(MAKE) clean
	$(MAKE) new-venv
	$(MAKE) install-deps
	$(MAKE) build
	$(MAKE) install-root
	$(MAKE) install-hooks

.PHONY: reinstall
reinstall:
	$(MAKE) delete-venv
	$(MAKE) remove-poetry
	$(MAKE) clean
	$(MAKE) install

.PHONY: install-poetry
install-poetry:
	@if [ -f "$(POETRY)" ]; then \
		echo "Poetry already installed in virtual environment"; \
	else \
		echo "Installing poetry in virtual environment"; \
		$(PYTHON) -m venv "$(POETRY_HOME)"; \
		$(POETRY_HOME)/bin/pip install --upgrade pip; \
		$(POETRY_HOME)/bin/pip install poetry==$(POETRY_VERSION); \
	fi

.PHONY: install-deps
-include .env
install-deps:
	@echo "Installing dependencies"
	@$(POETRY) install --no-root --no-interaction --no-ansi --all-extras -v


################################################################################
# Development - Virtual Environment
################################################################################
.PHONY: new-venv
new-venv:
	@echo "Creating virtual environment"
	@$(PYTHON) -m venv "$(VENV_PATH)"

.PHONY: delete-venv
delete-venv:
	@echo "Deleting virtual environment"
	@rm -rf "$(VENV_PATH)"

.PHONY: remove-poetry
remove-poetry:
	@echo "Removing poetry from virtual environment"
	@rm -rf "$(POETRY_HOME)"


################################################################################
# Development - Utilities
################################################################################
.PHONY: clean
clean:
	@echo "Cleaning up"
	@rm -rf .pytest_cache .ruff_cache .coverage htmlcov/
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type f -name '*.py[co]' -delete
	@find . -type f -name '*~' -delete


################################################################################
# Development - Pre-commit Hooks
################################################################################
.PHONY: install-hooks
install-hooks:
	@echo "Installing pre-commit hooks"
	@$(POETRY) run pre-commit install

.PHONY: update-hooks
update-hooks:
	@echo "Updating pre-commit hooks"
	@$(POETRY) run pre-commit autoupdate


################################################################################
# Development - Dependencies
################################################################################
.PHONY: lock
lock:
	@echo "Locking dependencies"
	@$(POETRY) lock --no-update

.PHONY: lock-update
lock-update:
	@echo "Locking and updating dependencies"
	@$(POETRY) update


################################################################################
# Linting & Formatting
################################################################################
.PHONY: lint
lint:
	@echo "Running ruff check and format check"
	@$(POETRY) run ruff check . --exit-non-zero-on-fix
	@$(POETRY) run ruff format . --check

.PHONY: format
format:
	@echo "Running ruff format"
	@$(POETRY) run ruff format .
	@$(POETRY) run ruff check . --fix

.PHONY: autofix-unsafe
autofix-unsafe:
	@echo "Running ruff with autofix-unsafe"
	@$(POETRY) run ruff check . --unsafe-fixes


################################################################################
# Testing
################################################################################
.PHONY: test
test:
	$(POETRY) run pytest -vvv;


################################################################################
# Execution
################################################################################
.PHONY: run
run:
	@echo "Running flow locally"
	@PYTHONPATH=$(PYTHONPATH):src $(POETRY) run python -m main

.PHONY: push-secrets
push-secrets:
	@PYTHONPATH=$(PYTHONPATH):deploy $(POETRY) run python -m push_secrets $(word 2, $(MAKECMDGOALS))
# e.g. make push-secrets upsert_prefect_api_url


################################################################################
# Environment Based Execution
################################################################################
# Using make deploy/trigger dev as shown will pass dev as a command, which will cause make to attempt to execute a target named dev.
# To prevent errors, this line ensures make treats dev and prod as simple arguments rather than separate targets.
dev prod:
	@:


.PHONY: trigger trigger-dev trigger-prod
trigger:
ifeq ($(word 2, $(MAKECMDGOALS)),prod)
	@$(MAKE) trigger-prod
else ifeq ($(word 2, $(MAKECMDGOALS)),dev)
	@$(MAKE) trigger-dev
else
	@echo "Environment not provided; defaulting to Dev."
	@$(MAKE) deploy-dev
endif

trigger-dev:
	@echo "Triggering flow-run to be executed remotely in Dev"
	$(POETRY) run prefect deployment run '{{cookiecutter.project_slug}}/dev'

trigger-prod:
	@echo "Triggering flow-run to be executed remotely in Prod"
	$(POETRY) run prefect deployment run '{{cookiecutter.project_slug}}/prod'


.PHONY: deploy confirm-env deploy-dev deploy-prod
deploy:
ifeq ($(word 2, $(MAKECMDGOALS)),prod)
	@$(MAKE) deploy-prod
else ifeq ($(word 2, $(MAKECMDGOALS)),dev)
	@$(MAKE) deploy-dev
else
	@$(MAKE) confirm-env
endif

confirm-env:
ifndef APP_ENVIRONMENT
	@echo "No environment specified and APP_ENVIRONMENT is not set."
	@echo "Defaulting to Dev environment."
	@echo -n "Do you want to proceed with Dev environment? (y/n) "; \
	read confirm; \
	if [ "$$confirm" = "y" ]; then \
		$(MAKE) deploy-dev; \
	else \
		echo "Deployment canceled."; \
	fi
else
ifeq ($(APP_ENVIRONMENT),prod)
	@$(MAKE) deploy-prod
else ifeq ($(APP_ENVIRONMENT),dev)
	@$(MAKE) deploy-dev
else
	@echo "Invalid APP_ENVIRONMENT value: $(APP_ENVIRONMENT)"
	@echo "Please set APP_ENVIRONMENT to 'dev' or 'prod'."
	@exit 1
endif
endif

deploy-dev:
	@echo "Deploying to Dev environment"
	@APP_ENVIRONMENT=dev PYTHONPATH=$(PYTHONPATH):deploy $(POETRY) run python -m deployment

deploy-prod:
	@echo "Deploying to Prod environment"
	@APP_ENVIRONMENT=prod PYTHONPATH=$(PYTHONPATH):deploy $(POETRY) run python -m deployment
