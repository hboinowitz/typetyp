VENV_NAME?=.venv
PATH_TO_ACTIVATE = $(VENV_NAME)/bin/activate

create_venv:
	python3 -m venv $(VENV_NAME)

install: create_venv
	(. $(PATH_TO_ACTIVATE) && pip3 install -e .)