PROJECT_NAME=app

prepare:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

run:
	python3 $(PROJECT_NAME)

lint:
	flake8 --max-line-length 119 $(PROJECT_NAME)

test:
	pytest -v tests