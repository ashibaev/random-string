prepare:
	( \
		python3.7 -m venv .venv; \
		. .venv/bin/activate; \
		pip install -r requirements.txt; \
		pip install -r requirements-dev.txt; \
	)

lint:
	( \
		. .venv/bin/activate; \
		flake8 --max-line-length 119 app; \
	)

test:
	( \
		. .venv/bin/activate; \
		pytest -v --cov=app tests; \
	)