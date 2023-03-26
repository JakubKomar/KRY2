# project:
# autor: Bc. Jakub Komárek (xkomar33)
# description:
VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
MAIN = kry.py
 
.PHONY: all build run pack clean h help create_env clean_env

all: build

build:create_env

pack: clean
	zip -r xkomar33.zip src/ doc/ tests/  Makefile 	

help:h
h:
	@echo "make run - run main script"
	@echo "make build - build venv and install libs"
	@echo "make clean - cleans up venv"

run:
	$(PYTHON) $(MAIN) TYPE=$(TYPE) PORT=$(PORT)

create_env:
	python3 -m venv $(VENV) &\
	$(PYTHON) -m pip install  -r requirements.txt

clean_env:
	rm -rf $(VENV)

clean: clean_env
	cd data && rm -rf download_data