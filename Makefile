ifdef OS
	PYTHON ?= venv/Scripts/python.exe
	TYPE_CHECK_COMMAND ?= echo Pytype package doesn't support Windows OS
else
	PYTHON ?= venv/bin/python3
	TYPE_CHECK_COMMAND ?= ${PYTHON} -m pytype --config=pytype.cfg src
endif

SETTINGS_FILENAME = pyproject.toml
COMPOSE_FILENAME = docker-compose.yml

enable-pre-commit-hooks:
	${PYTHON} -m pre_commit install

format:
	${PYTHON} -m isort [TODO: ADD PATHs] --force-single-line-imports --settings-file ${SETTINGS_FILENAME}
	${PYTHON} -m autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place [TODO: ADD PATHs] --exclude=__init__.py
	${PYTHON} -m black [TODO: ADD PATHs] --config ${SETTINGS_FILENAME}
	${PYTHON} -m isort [TODO: ADD PATHs] --settings-file ${SETTINGS_FILENAME}

lint:
	${PYTHON} -m flake8 --toml-config ${SETTINGS_FILENAME} --max-complexity 5 --max-cognitive-complexity=5 [TODO: ADD PATHs]
	${PYTHON} -m black [TODO: ADD PATHs] --check --diff --config ${SETTINGS_FILENAME}
	${PYTHON} -m isort [TODO: ADD PATHs] --check --diff --settings-file ${SETTINGS_FILENAME}

secure:
	${PYTHON} -m bandit -r [TODO: ADD PATHs] --config ${SETTINGS_FILENAME}

run-build:
	docker-compose -f ${COMPOSE_FILENAME} down
	docker-compose -f ${COMPOSE_FILENAME} build
	docker-compose -f ${COMPOSE_FILENAME} up