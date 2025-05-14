.PHONY: dev

dev:
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8081 &
	pushd ./frontend && npm run dev && popd

test:
	pytest -v --disable-warnings --tb=short
	pushd frontend && npm run test && popd

db_migrate:
	cd db; DATABASE_URL=postgresql://postgres:postgres@localhost/dev uv run alembic upgrade head
	cd db; DATABASE_URL=postgresql://postgres:postgres@localhost/test uv run alembic upgrade head
