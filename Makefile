MAKEFLAGS += --warn-undefined-variables
SHELL := bash

# ================================
# Variables
# ================================
VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
RUN := $(VENV)/bin/python -m

SCHEMA_NAME = peh
SRC = linkml
DEST = _temp
SOURCE_SCHEMA_PATH = $(SRC)/schema/$(SCHEMA_NAME).yaml
SOURCE_SCHEMA_DIR = $(dir $(SOURCE_SCHEMA_PATH))
PYMODEL = $(SRC)/python

# ================================
# Phony targets
# ================================
.PHONY: help install setup make-dirs clean lint lint-fix test-schema gen-project check-config serialize

# ================================
# Help
# ================================
help: check-config
	@echo ""
	@echo "make install      -- create venv and install dependencies"
	@echo "make setup        -- full project generation and setup"
	@echo "make make-dirs    -- create necessary directories"
	@echo "make test-schema  -- regenerate models and check schema"
	@echo "make lint         -- lint the schema"
	@echo "make lint-fix     -- lint-fix the schema and fix issues"
	@echo "make serialize    -- serialize data examples"
	@echo "make clean        -- clean generated files"
	@echo ""

# ================================
# check-config
# ================================
check-config:
	@echo "Project: $(SCHEMA_NAME)"
	@echo "Source: $(SOURCE_SCHEMA_PATH)"

# ================================
# Setup
# ================================
setup: instal gen-project

# ================================
# Install dependencies
# ================================
install:
	@test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements/publish.txt

# ================================
# Generate project files
# ================================
gen-project: make-dirs
	
	gen-project \
		--exclude excel \
		--exclude graphql \
		--include jsonld \
		--exclude markdown \
		--exclude prefixmap \
		--exclude proto \
		--exclude shacl \
		--exclude shex \
		--exclude sqlddl \
		--include jsonldcontext \
		--exclude jsonschema \
		--exclude owl \
		--include python \
		--include rdf \
		-d $(DEST) $(SOURCE_SCHEMA_PATH)
# MAKE OWL
	gen-owl --mergeimports --no-metaclasses --no-type-objects --add-root-classes --mixins-as-expressions $(SOURCE_SCHEMA_PATH) > $(SRC)/owl/$(SCHEMA_NAME).owl
# MAKE RDF
	gen-rdf $(SOURCE_SCHEMA_PATH) > $(DEST)/peh.ttl
# MAKE PYDANTIC
	gen-pydantic --meta None $(SOURCE_SCHEMA_PATH) > $(PYMODEL)/pydanticmodel_v2.py
# MOVE OUTPUT TO CORRECT FOLDER
	mv $(DEST)/jsonld/*.jsonld $(SRC)/jsonld/.
	mv $(DEST)/peh.py $(PYMODEL)/.
	mv $(DEST)/peh.ttl	$(SRC)/rdf/.
# RUN BLACK
# skip black as linkml pydantic schema is not conform requirements	
#black $(PYMODEL)		

# ================================
# Linting
# ================================
lint:
	linkml-lint --no-fix --ignore-warnings $(SOURCE_SCHEMA_PATH)

# ================================
# Linting with fix
# ================================
lint-fix:
	cp $(SOURCE_SCHEMA_PATH) .
	linkml-lint --fix $(SCHEMA_NAME).yaml

# ================================
# Serialize test data
# ================================
# NOTE serializing to RDF will cause an error, this is a linkml issue
serialize:
	linkml-convert -f yaml -t json --target-class EntityList --index-slot biochementities -s $(SOURCE_SCHEMA_PATH) $(SRC)/data/BioChemEntityList_data.yaml

# ================================
# Test schema
# ================================
test-schema: lint gen-project serialize

# ================================
# Create directories
# ================================
make-dirs:
	@echo "Creating necessary directories..."
	mkdir -p $(DEST)
	mkdir -p $(SRC)/python
	mkdir -p $(SRC)/jsonld
	mkdir -p $(SRC)/owl
	mkdir -p $(SRC)/rdf

# ================================
# Cleaning
# ================================
clean:
	rm -rf $(DEST)
	rm -rf $(PYMODEL)/*
	rm -rf $(VENV)

