# Makefile for setting up the templated project with a virtual environment

# Default repository information (replace with your actual repo URL if needed)
REPO_URL := $(shell git config --get remote.origin.url)
AUTHOR := $(shell git config --get user.name)
PROJECT_NAME ?= my_project  # Default project name if none is provided
PROJECT_SLUG := $(shell echo $(PROJECT_NAME) | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_]/_/g')

# Virtual environment directory
VENV_DIR := .venv

# Color codes for echo statements
YELLOW := \033[1;33m
GREEN := \033[1;32m
RESET := \033[0m

.PHONY: setup
setup:
	@echo "$(GREEN)Setting up the project...$(RESET)"
	@echo "$(YELLOW)Project Name: $(PROJECT_NAME)$(RESET)"
	@echo "$(YELLOW)Project Slug: $(PROJECT_SLUG)$(RESET)"
	@echo "$(YELLOW)Repository URL: $(REPO_URL)$(RESET)"
	@echo "$(YELLOW)Author: $(AUTHOR)$(RESET)"

	# Step 1: Create a virtual environment
	@echo "$(GREEN)Creating virtual environment...$(RESET)"
	@python3 -m venv $(VENV_DIR)

	# Step 2: Install cookiecutter in the virtual environment
	@echo "$(GREEN)Installing cookiecutter in virtual environment...$(RESET)"
	@$(VENV_DIR)/bin/pip install cookiecutter

	# Step 3: Run cookiecutter using the virtual environment
	@echo "$(GREEN)Running cookiecutter template...$(RESET)"
	@$(VENV_DIR)/bin/cookiecutter --no-input \
		--output-dir ./prefect_project_template \
		./prefect_project_template/ \
		project_name="$(PROJECT_NAME)" \
		project_slug="$(PROJECT_SLUG)" \
		self_repository_url="$(REPO_URL)" \
		author="$(AUTHOR)" \
		env_file=".env"

	# Step 4: Copy generated project files to the root of the repository
	@echo "$(GREEN)Moving generated project to root directory...$(RESET)"
	@rsync -a ./prefect_project_template/$(PROJECT_SLUG)/ ./
	@rm -rf ./prefect_project_template/$(PROJECT_SLUG)

	# Step 5: Remove the original template directory
	@echo "$(GREEN)Removing the original template directory...$(RESET)"
	@rm -rf ./prefect_project_template

	# Step 6: Clean up the virtual environment
	@echo "$(GREEN)Removing virtual environment...$(RESET)"
	@rm -rf $(VENV_DIR)

	# Step 7: Commit the changes
	@echo "$(GREEN)Committing the changes...$(RESET)"
	@git add .
	@git commit -m "Generate project using cookiecutter template"
	@echo "$(GREEN)Setup complete. Don't forget to push your changes!$(RESET)"
