.PHONY: help install test coverage lint format clean run dev migrate seed docker-local docker-dev docker-prod docker-down docker-logs docker-clean

# Default target
.DEFAULT_GOAL := help

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m

help: ## Show this help message
	@echo "$(CYAN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Development
install: ## Install dependencies with Poetry
	@echo "$(CYAN)Installing dependencies...$(NC)"
	poetry install

update: ## Update dependencies
	@echo "$(CYAN)Updating dependencies...$(NC)"
	poetry update

run: ## Run the API server locally
	@echo "$(CYAN)Starting API server...$(NC)"
	poetry run python -m src.main

dev: ## Run API with auto-reload (development mode)
	@echo "$(CYAN)Starting API in development mode...$(NC)"
	poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

consumer: ## Run event consumer
	@echo "$(CYAN)Starting event consumer...$(NC)"
	poetry run python scripts/run_consumer.py

# Database
migrate: ## Run database migrations
	@echo "$(CYAN)Running migrations...$(NC)"
	poetry run alembic upgrade head

migrate-create: ## Create new migration (usage: make migrate-create msg="description")
	@echo "$(CYAN)Creating new migration...$(NC)"
	poetry run alembic revision --autogenerate -m "$(msg)"

migrate-down: ## Rollback last migration
	@echo "$(CYAN)Rolling back migration...$(NC)"
	poetry run alembic downgrade -1

seed: ## Seed database with test data
	@echo "$(CYAN)Seeding database...$(NC)"
	poetry run python scripts/seed_data.py

db-reset: ## Reset database (drop all tables and re-migrate)
	@echo "$(RED)Resetting database...$(NC)"
	poetry run alembic downgrade base
	poetry run alembic upgrade head

# Testing
test: ## Run all tests
	@echo "$(CYAN)Running tests...$(NC)"
	poetry run pytest -v

test-unit: ## Run unit tests only
	@echo "$(CYAN)Running unit tests...$(NC)"
	poetry run pytest src/tests/unit -v

test-integration: ## Run integration tests only
	@echo "$(CYAN)Running integration tests...$(NC)"
	poetry run pytest src/tests/integration -v

coverage: ## Run tests with coverage report
	@echo "$(CYAN)Running tests with coverage...$(NC)"
	poetry run pytest --cov=src --cov-report=html --cov-report=term

coverage-report: ## Open coverage report in browser
	@echo "$(CYAN)Opening coverage report...$(NC)"
	xdg-open htmlcov/index.html 2>/dev/null || open htmlcov/index.html 2>/dev/null || echo "Please open htmlcov/index.html manually"

# Code Quality
lint: ## Run linter (ruff)
	@echo "$(CYAN)Running linter...$(NC)"
	poetry run ruff check src/

lint-fix: ## Run linter and fix issues
	@echo "$(CYAN)Running linter with auto-fix...$(NC)"
	poetry run ruff check --fix src/

format: ## Format code with ruff
	@echo "$(CYAN)Formatting code...$(NC)"
	poetry run ruff format src/

format-check: ## Check code formatting
	@echo "$(CYAN)Checking code formatting...$(NC)"
	poetry run ruff format --check src/

# Docker - Local (only infrastructure)
docker-local: ## Start local infrastructure (PostgreSQL + RabbitMQ)
	@echo "$(CYAN)Starting local infrastructure...$(NC)"
	cd deployment/local && docker-compose up -d

docker-local-down: ## Stop local infrastructure
	@echo "$(CYAN)Stopping local infrastructure...$(NC)"
	cd deployment/local && docker-compose down

docker-local-logs: ## Show logs for local infrastructure
	cd deployment/local && docker-compose logs -f

# Docker - Dev (full stack)
docker-dev: ## Start dev environment (all services)
	@echo "$(CYAN)Starting dev environment...$(NC)"
	cd deployment/dev && docker-compose up -d

docker-dev-build: ## Build and start dev environment
	@echo "$(CYAN)Building and starting dev environment...$(NC)"
	cd deployment/dev && docker-compose up -d --build

docker-dev-down: ## Stop dev environment
	@echo "$(CYAN)Stopping dev environment...$(NC)"
	cd deployment/dev && docker-compose down

docker-dev-logs: ## Show logs for dev environment
	cd deployment/dev && docker-compose logs -f

docker-dev-restart: ## Restart dev environment
	@echo "$(CYAN)Restarting dev environment...$(NC)"
	cd deployment/dev && docker-compose restart

# Docker - Prod
docker-prod: ## Start prod environment
	@echo "$(CYAN)Starting prod environment...$(NC)"
	cd deployment/prod && docker-compose up -d

docker-prod-build: ## Build and start prod environment
	@echo "$(CYAN)Building and starting prod environment...$(NC)"
	cd deployment/prod && docker-compose up -d --build

docker-prod-down: ## Stop prod environment
	@echo "$(CYAN)Stopping prod environment...$(NC)"
	cd deployment/prod && docker-compose down

docker-prod-logs: ## Show logs for prod environment
	cd deployment/prod && docker-compose logs -f

# Docker - General
docker-ps: ## Show running containers
	@echo "$(CYAN)Running containers:$(NC)"
	docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"

docker-clean: ## Remove all containers, volumes and images
	@echo "$(RED)Cleaning up Docker resources...$(NC)"
	docker-compose -f deployment/local/docker-compose.yml down -v 2>/dev/null || true
	docker-compose -f deployment/dev/docker-compose.yml down -v 2>/dev/null || true
	docker-compose -f deployment/prod/docker-compose.yml down -v 2>/dev/null || true
	docker system prune -af --volumes

docker-rebuild: ## Rebuild all Docker images without cache
	@echo "$(CYAN)Rebuilding all images...$(NC)"
	cd deployment/dev && docker-compose build --no-cache

# Kubernetes
k8s-local: ## Deploy to local Kubernetes (minikube)
	@echo "$(CYAN)Deploying to local Kubernetes...$(NC)"
	kubectl apply -k deployment/kubernetes/overlays/local

k8s-prod: ## Deploy to prod Kubernetes
	@echo "$(CYAN)Deploying to prod Kubernetes...$(NC)"
	kubectl apply -k deployment/kubernetes/overlays/prod

k8s-delete: ## Delete Kubernetes resources
	@echo "$(RED)Deleting Kubernetes resources...$(NC)"
	kubectl delete -k deployment/kubernetes/overlays/local 2>/dev/null || true
	kubectl delete -k deployment/kubernetes/overlays/prod 2>/dev/null || true

k8s-status: ## Show Kubernetes pods status
	@echo "$(CYAN)Kubernetes resources:$(NC)"
	kubectl get pods,svc,pvc -n tz

k8s-watch: ## Watch pods status
	kubectl get pods -n tz -w

k8s-logs: ## Show logs for API pod
	kubectl logs -n tz -f -l app=tz-api

k8s-logs-consumer: ## Show logs for Consumer pod
	kubectl logs -n tz -f -l app=tz-consumer

k8s-describe: ## Describe all resources in tz namespace
	kubectl describe all -n tz

k8s-restart: ## Restart deployments
	@echo "$(CYAN)Restarting deployments...$(NC)"
	kubectl rollout restart deployment/tz-api -n tz
	kubectl rollout restart deployment/tz-consumer -n tz

# Utility
clean: ## Clean up generated files
	@echo "$(CYAN)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2