.PHONY: all test lint dev-bootstrap docker-build deploy

all: test

test:
	@uv run pytest test_ip.py -v

lint:
	@uv run ruff check ip.py test_ip.py

dev-bootstrap:
	@command -v uv >/dev/null 2>&1 || { curl -LsSf https://astral.sh/uv/install.sh | sh; }
	@uv sync --dev
	@echo "==> dev env ready"

docker-build:
	@docker compose build

deploy:
	@ssh -p 2222 ubuntu@10.0.0.91 "cd ~/proj/IP && git pull && docker compose pull && docker compose up -d"
