#/**
# * TangoMan Python Boilerplate
# *
# * A collection of useful scripts to manage Python projects
# *
# * @version  0.1.0
# * @author   "Matthias Morin" <mat@tangoman.io>
# * @licence  MIT
# * @link     https://github.com/TangoMan75/makefile-generator
# * @link     https://www.linkedin.com/in/morinmatthias
# */

.PHONY: help install run freeze dev-install pip-update tests check-install venv-run venv-create venv-start venv-stop venv-install venv-remove

# Colors
TITLE     = \033[1;42m
CAPTION   = \033[1;44m
BOLD      = \033[1;34m
LABEL     = \033[1;32m
DANGER    = \033[31m
SUCCESS   = \033[32m
WARNING   = \033[33m
SECONDARY = \033[34m
INFO      = \033[35m
PRIMARY   = \033[36m
DEFAULT   = \033[0m
NL        = \033[0m\n

# Local operating system (Windows_NT, Darwin, Linux)
ifeq ($(OS),Windows_NT)
	SYSTEM=$(OS)
else
	SYSTEM=$(shell uname -s)
endif

# virtualenv name
virtualenv?=venv

## Print this help
help:
	@printf "${TITLE} TangoMan $(shell basename ${CURDIR}) ${NL}\n"

	@printf "${CAPTION} Infos:${NL}"
	@printf "${PRIMARY} %-12s${INFO} %s${NL}" "virtualenv" "${virtualenv}"
	@printf "${NL}"

	@printf "${CAPTION} Description:${NL}"
	@printf "${WARNING} A collection of useful scripts to use in your Python projects${NL}\n"

	@printf "${CAPTION} Usage:${NL}"
	@printf "${WARNING} make [command] `awk -F '?' '/^[ \t]+?[a-zA-Z0-9_-]+[ \t]+?\?=/{gsub(/[ \t]+/,"");printf"%s=[%s]\n",$$1,$$1}' ${MAKEFILE_LIST}|sort|uniq|tr '\n' ' '`${NL}\n"

	@printf "${CAPTION} Commands:${NL}"
	@awk '/^### /{printf"\n${BOLD}%s${NL}",substr($$0,5)} \
	/^[a-zA-Z0-9_-]+:/{HELP="";if(match(PREV,/^## /))HELP=substr(PREV, 4); \
		printf " ${LABEL}%-13s${DEFAULT} ${PRIMARY}%s${NL}",substr($$1,0,index($$1,":")),HELP \
	}{PREV=$$0}' ${MAKEFILE_LIST}

##################################################
### Python3 Module
##################################################

## Install module locally
install:
ifeq (${SYSTEM}, Linux)
	@printf "${INFO}sudo python3 setup.py install${NL}"
	-@sudo python3 setup.py install
endif

## Uninstall module locally
uninstall:
ifeq (${SYSTEM}, Linux)
	@printf "${INFO}sudo pip3 uninstall -y tangoman-$(shell basename ${CURDIR})${NL}"
	-@sudo pip3 uninstall -y tangoman-$(shell basename ${CURDIR})
	@printf "${INFO}sudo rm -rf build dist *.egg-info${NL}"
	@sudo rm -rf build dist *.egg-info
endif

##################################################
### Python3 Cache
##################################################

## Clear python cache
clean:
	@printf "${INFO}find . -type d -name __pycache__ | xargs rm -rf${NL}"
	@find . -type d -name __pycache__ | xargs rm -rf
	@printf "${INFO}find . -type f -iname \"*.pyc\" -delete${NL}"
	@find . -type f -iname "*.pyc" -delete

##################################################
### Python3 Unit Test
##################################################

## Run unit tests
tests:
	@printf "${INFO}python3 -m unittest -v tests/*.py${NL}"
	@python3 -m unittest -v tests/*.py

## Check static typing with mypy
mypy:
	@# Check mypy module installed
	@python3 -c 'import mypy'
	@if [ $? == 0 ]; then \
		printf "${INFO}python3 -m mypy${NL}" && \
		python3 -m mypy; \
	else \
		printf "${INFO}mypy module not found${NL}"; \
	fi

##################################################
### Python3 Local Install
##################################################

## Install development environment locally (python3, pip3 and virtualenv)
python-install:
ifeq (${SYSTEM}, Linux)
	@printf "${INFO}sudo apt-get update${NL}"
	-@sudo apt-get update
	@printf "${INFO}sudo apt-get install -y python3${NL}"
	@sudo apt-get install -y python3
	@printf "${INFO}sudo apt-get install -y python3-pip${NL}"
	@sudo apt-get install -y python3-pip
	@printf "${INFO}python3 -m pip install --upgrade pip${NL}"
	@python3 -m pip install --upgrade pip
	@printf "${INFO}sudo apt-get install -y python-virtualenv${NL}"
	@sudo apt-get install -y python-virtualenv
endif

## Update all pip packages locally
pip-update:
	@printf "${INFO}python3 -m pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 python3 -m pip install -U${NL}"
	@python3 -m pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 python3 -m pip install -U

##################################################
### Python Virtualenv
##################################################

## Create virtualenv
venv-create: venv-remove
	@printf "${INFO}virtualenv -p python3 ${virtualenv}${NL}"
	@virtualenv -p python3 ${virtualenv}
	-@make --no-print-directory venv-start
	-@make --no-print-directory venv-install

## Activate virtualenv
venv-start:
ifeq ($(shell test -f ${virtualenv}/bin/activate && echo true),true)
	@printf "${INFO}source ${virtualenv}/bin/activate${NL}"
	@source ${virtualenv}/bin/activate
else
	@printf "${DANGER}error: virtualenv not found${NL}"
	@exit 1
endif

## Deactivate virtualenv
venv-stop:
	@printf "${INFO}bash -c \"source ${virtualenv}/bin/activate && deactivate\"${NL}"
	-@bash -c "source ${virtualenv}/bin/activate && deactivate"

## Install in virtualenv
venv-install:
ifeq ($(shell test -f ${virtualenv}/bin/pip && echo true),true)
	@printf "${INFO}${virtualenv}/bin/pip install -r requirements.txt${NL}"
	@${virtualenv}/bin/pip install -r requirements.txt
else
	@printf "${DANGER}error: virtualenv not found${NL}"
	@exit 1
endif

## Run tests from virtualenv
venv-tests:
ifeq ($(shell test -f ${virtualenv}/bin/python && echo true),true)
	@printf "${INFO}venv/bin/python -m unittest -v tests/*.py${NL}"
	@venv/bin/python -m unittest -v tests/*.py
else
	@printf "${DANGER}error: virtualenv not found${NL}"
	@exit 1
endif

## Remove virtualenv
venv-remove: venv-stop
	@printf "${INFO}rm -rf ${virtualenv}${NL}"
	@rm -rf ${virtualenv}
	@printf "${INFO}rm -rf __pycache__${NL}"
	@rm -rf __pycache__

##################################################
### Check Python install
##################################################

## Check correct python environment installation
check-install:
	@if [ -n "$(shell pip --version 2>/dev/null)" ]; then \
		printf "${INFO}pip --version${NL}"; \
		pip --version; \
	else \
		printf "${WARNING}pip is not installed on your system${NL}"; \
	fi
	@if [ -n "$(shell pip3 --version 2>/dev/null)" ]; then \
		printf "${INFO}pip3 --version${NL}"; \
		pip3 --version; \
	else \
		printf "${WARNING}pip3 is not installed on your system${NL}"; \
	fi
	@if [ -n "$(shell python --version 2>/dev/null)" ]; then \
		printf "${INFO}python --version${NL}"; \
		python --version; \
	else \
		printf "${WARNING}python is not installed on your system${NL}"; \
	fi
	@if [ -n "$(shell python2 --version 2>/dev/null)" ]; then \
		printf "${INFO}python2 --version${NL}"; \
		python2 --version; \
	else \
		printf "${WARNING}python2 is not installed on your system${NL}"; \
	fi
	@if [ -n "$(shell python3 --version 2>/dev/null)" ]; then \
		printf "${INFO}python3 --version${NL}"; \
		python3 --version; \
	else \
		printf "${WARNING}python3 is not installed on your system${NL}"; \
	fi
	@if [ -n "$(shell virtualenv --version 2>/dev/null)" ]; then \
		printf "${INFO}virtualenv --version${NL}"; \
		virtualenv --version; \
	else \
		printf "${WARNING}virtualenv is not installed on your system${NL}"; \
	fi

