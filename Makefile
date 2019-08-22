ifeq ($(OS),Windows_NT)
set_path:
	set PYTHONPATH=%PYTHONPATH%:app
else
set_path:
	export PYTHONPATH=$PYTHONPATH:app
endif

prepare:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

run: set_path
	python3 app

lint:
	flake8 --max-line-length 119 app

test: set_path
	pytest -v --cov=app tests