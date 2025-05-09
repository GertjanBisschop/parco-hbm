MAKEFLAGS += --warn-undefined-variables
SHELL := bash
# ================================
# Variables
# ================================
# Include the .env file
ifneq (,$(wildcard .env))
  include .env
  export
else
  $(error .env file not found)
endif

# List of required variables
REQUIRED_VARS = \
  NANOPUB_ORCID_ID \
  NANOPUB_NAME \
  NANOPUB_PRIVATE_KEY \
  NANOPUB_PUBLIC_KEY \
  NANOPUB_INTRO_URI

VENV := .venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
RUN := $(VENV)/bin/python -m
MAINTAINER:= gertjan.bisschop@vito.be
VERSION:=0.0.0

SCHEMA_NAME = peh
SRC = linkml
DEST = _temp
SOURCE_SCHEMA_PATH = $(SRC)/schema/$(SCHEMA_NAME).yaml
SOURCE_SCHEMA_DIR = $(dir $(SOURCE_SCHEMA_PATH))
PYMODEL = $(SRC)/python

CHANGELOG_SCRIPT_PATH=$(SRC)/scripts/changelog.py
PUBLISH_SCRIPT_PATH=$(SRC)/scripts/publish.py
CHANGELOG_SCHEMA_PATH=$(SRC)/changelog/changelog.schema.yaml
CHANGELOG_PATH=$(SRC)/changelog/_upcoming.yaml

# ================================
# Phony targets
# ================================
.PHONY: help install setup make-dirs clean lint lint-fix test-schema gen-project check-config serialize publish-nanopubs

# ================================
# Help
# ================================
help: check-config
	@echo ""
	@echo "make install      		-- create venv and install dependencies"
	@echo "make setup        		-- full project generation and setup"
	@echo "check-env"				-- check presence of required env variables"
	@echo "make make-dirs    		-- create necessary directories"
	@echo "make test-schema  		-- regenerate models and check schema"
	@echo "make lint         		-- lint the schema"
	@echo "make lint-fix     		-- lint-fix the schema and fix issues"
	@echo "make serialize    		-- serialize data examples"
	@echo "make publish-nanopubs    -- publish model updates"
	@echo "make clean        		-- clean generated files"
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
# Target to check env vars
# ================================
check-env:
	@missing=0; \
	for var in $(REQUIRED_VARS); do \
	  if [ -z "$${!var}" ]; then \
	    echo "ERROR: Required environment variable $$var is not set"; \
	    missing=1; \
	  fi; \
	done; \
	if [ $$missing -eq 1 ]; then \
	  exit 1; \
	else \
	  echo "Found all required environment variables."; \
	fi

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

# ================================
# PUBLISHING
# ================================
publish-nanopubs: check-env
	@VERSION=$$(python3 "$(CHANGELOG_SCRIPT_PATH)" extract-version $(CHANGELOG_PATH))
	echo "Publishing schema version: $$VERSION"
	python3 "$(CHANGELOG_SCRIPT_PATH)" validate-changelog -s "$(CHANGELOG_SCHEMA_PATH)" "$(CHANGELOG_PATH)"
	@echo "Publish terms in changelog."
	python3 $(PUBLISH_SCRIPT_PATH) publish \
		-s $(SRC)/rdf/$(SCHEMA_NAME).ttl \
		-c $(CHANGELOG_PATH) \
		--dry-run \
		--output-pairs $(DEST)/output-pairs.txt
	@echo "Generating release notes ..."
	python3 "$(CHANGELOG_SCRIPT_PATH)" generate-release-notes -o "$(DEST)" -f $(CHANGELOG_PATH)
	@echo "Generating new changelog ..."
	python3 "$(CHANGELOG_SCRIPT_PATH)" init-new-changelog -m "$(MAINTAINER)" -d "$(SRC)/changelog/"
