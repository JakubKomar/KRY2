#Project name: Implementace hybrydního šifrování
#autor: Bc. Jakub Komárek
#File description: Implementace kryptografických metod

VENV = venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
MAIN = kry.py
 
.PHONY: all build run pack clean  create_env clean_env

all: build

build:create_env

pack: clean
	zip -r 222161.zip client.py server.py kry.py methods.py keyGen.py README doc.pdf Makefile requirements.txt

run:
	$(PYTHON) $(MAIN) TYPE=$(TYPE) PORT=$(PORT)

create_env:
	python3 -m venv $(VENV) 
	$(PYTHON) -m pip install  -r requirements.txt

clean_env:
	rm -rf $(VENV)

clean: clean_env
	if [ -d "cert" ]; then rm -r "cert"; fi  &\
	rm -rf 222161.zip
