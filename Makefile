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
.PHONY: help install setup clean lint lint-fix test-schema gen-project check-config

# ================================
# Help
# ================================
help: check-config
	@echo ""
	@echo "make install      -- create venv and install dependencies"
	@echo "make setup        -- full project generation and setup"
	@echo "make test-schema  -- regenerate models and check schema"
	@echo "make lint         -- lint the schema"
	@echo "make lint-fix     -- lint the schema and fix issues"
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
setup: install gen-project

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
gen-project: $(PYMODEL)
	
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
		--exclude jsonldcontext \
		--exclude jsonschema \
		--exclude owl \
		--include python \
		--include rdf \
		-d $(DEST) $(SOURCE_SCHEMA_PATH)
# MAKE OWL
	gen-owl --mergeimports --no-metaclasses --no-type-objects --add-root-classes --mixins-as-expressions $(SOURCE_SCHEMA_PATH) > $(SOURCE)/owl/$(SCHEMA_NAME).owl
# MAKE PYDANTIC
	gen-pydantic --meta None $(SOURCE_SCHEMA_PATH) > $(PYMODEL)/pydanticmodel_v2.py
# MOVE OUTPUT TO CORRECT FOLDER
	mv peh.jdsonld $(SRC)/jsonld/.
	mv peh.owl $(SRC)/owl/.
	mv peh.py $(PYMODEL)/.
	mv peh.ttl	$(SRC)/ttl/.		

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
# Test schema
# ================================
test-schema: lint gen-project

# ================================
# Create directories
# ================================
$(PYMODEL):
	mkdir -p $@
	mkdir -p $(SRC)/jsonld
	mkdir -p $(SRC)/owl
	mkdir -p $(SRC)/ttl

# ================================
# Cleaning
# ================================
clean:
	rm -rf $(DEST)
	rm -rf $(PYMODEL)/*
	rm -rf $(VENV)

