COMPOSE_DEV = docker compose --env-file .env -f docker-compose.yaml -f docker-compose.dev.yaml

.PHONY: run-dev down-dev build-dev logs-dev shell-service-dev env-init migrate load-fixtures test test-api lint lint-fix fmt format-check check

run-dev:
	$(COMPOSE_DEV) up -d $(ARGS)

down-dev:
	$(COMPOSE_DEV) down $(ARGS)

build-dev:
	$(COMPOSE_DEV) build $(ARGS)

logs-dev:
	$(COMPOSE_DEV) logs $(SERVICE)

shell-service-dev:
	$(COMPOSE_DEV) exec -it $(SERVICE) sh -lc 'command -v bash >/dev/null 2>&1 && exec bash || exec sh'

env-init:
	./scripts/init-env.sh

migrate:
	$(COMPOSE_DEV) exec -T main-api sh -lc 'cd /app/zaharovo && uv run python manage.py migrate'

load-fixtures:
	$(COMPOSE_DEV) exec -T main-api sh -lc 'cd /app/zaharovo && uv run python manage.py loaddata generated_products.json'

test: test-api

test-api:
	$(COMPOSE_DEV) exec -T main-api sh -lc 'cd /app/zaharovo && uv run python manage.py test'

lint:
	cd main-api && UV_PROJECT_ENVIRONMENT=.venv-dev uv run --group dev ruff check .
	cd frontend && UV_PROJECT_ENVIRONMENT=.venv-dev uv run --group dev ruff check .

lint-fix:
	cd main-api && UV_PROJECT_ENVIRONMENT=.venv-dev uv run --group dev ruff check . --fix
	cd frontend && UV_PROJECT_ENVIRONMENT=.venv-dev uv run --group dev ruff check . --fix

fmt:
	cd main-api && UV_PROJECT_ENVIRONMENT=.venv-dev uv run --group dev ruff format .
	cd frontend && UV_PROJECT_ENVIRONMENT=.venv-dev uv run --group dev ruff format .

format-check:
	cd main-api && UV_PROJECT_ENVIRONMENT=.venv-dev uv run --group dev ruff format . --check
	cd frontend && UV_PROJECT_ENVIRONMENT=.venv-dev uv run --group dev ruff format . --check

check: lint test
