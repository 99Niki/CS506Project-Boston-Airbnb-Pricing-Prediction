VENV        := .venv
BASE_PYTHON := python3
PYTHON      := $(VENV)/bin/python
PIP         := $(VENV)/bin/pip
JUPYTER     := $(VENV)/bin/jupyter
PYTEST      := $(VENV)/bin/pytest

NB          := CS506_Airbnb_Notebook.ipynb
DATA        := listings.csv
DATA_GZ     := $(DATA).gz
DATA_URL    := http://data.insideairbnb.com/united-states/ma/boston/2025-09-23/data/listings.csv.gz

.DEFAULT_GOAL := help

.PHONY: help setup install data run test check clean

help:
	@echo "Available targets:"
	@echo "  make setup    Create .venv, install dependencies, and make sure data exists"
	@echo "  make install  Create/update the local Python virtual environment"
	@echo "  make data     Use listings.csv if present, otherwise download it"
	@echo "  make run      Execute the notebook with the virtual environment"
	@echo "  make test     Run tests with the virtual environment"
	@echo "  make clean    Remove generated files and the virtual environment"

setup: install data

install: $(VENV)/.installed

$(VENV)/.installed: requirements.txt
	$(BASE_PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@touch $(VENV)/.installed

data:
	@if [ -f $(DATA) ]; then \
		echo "Using $(DATA) from the repository root."; \
	else \
		echo "$(DATA) not found. Downloading from Inside Airbnb."; \
		curl -L $(DATA_URL) -o $(DATA_GZ); \
		gunzip -f $(DATA_GZ); \
	fi

run: setup
	@mkdir -p outputs
	$(JUPYTER) nbconvert --to notebook --execute $(NB) \
		--output outputs/$(NB) --ExecutePreprocessor.timeout=900

test: install
	$(PYTEST) tests/ -v

check: test

clean:
	rm -rf $(VENV) .pytest_cache outputs/
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
