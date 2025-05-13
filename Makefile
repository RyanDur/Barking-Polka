.PHONY: dev

dev:
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8081 &
	pushd ./frontend && npm run dev && popd

test:
	pytest -v --disable-warnings --tb=short
	pushd frontend && npm run test && popd