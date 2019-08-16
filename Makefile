prepare:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

run:
	python3 app

lint:
	flake8 --max-line-length 119 app

test:
	pytest -v --cov=app tests