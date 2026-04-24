VENV     := .venv
PYTHON   := $(VENV)/bin/python
PIP      := $(VENV)/bin/pip
NB       := CS506_Airbnb_Merged.ipynb
DATA_URL := http://data.insideairbnb.com/united-states/ma/boston/2024-09-23/data/listings.csv.gz

.PHONY: install data run test clean

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

data:
	@echo "Using listings.csv from the repository root."
	@test -f listings.csv || (echo "ERROR: listings.csv not found in repo root!" && exit 1)

run:
	$(VENV)/bin/jupyter nbconvert --to notebook --execute $(NB) \
	    --output outputs/$(NB) --ExecutePreprocessor.timeout=900

test:
	$(VENV)/bin/pytest tests/ -v

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache outputs/