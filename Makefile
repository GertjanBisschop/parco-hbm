MAKEFLAGS += --warn-undefined-variables
SHELL := bash
# ================================
# Variables
# ================================

# List of required variables in .env for local publishing
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
VERSION:= 0.0.0
LINKML_VERSION:=1.9

SCHEMA_NAME = peh
SRC = linkml
DEST = _temp
SOURCE_SCHEMA_PATH = $(SRC)/schema/$(SCHEMA_NAME).yaml
INDEX_FILE_PATH = $(SRC)/changelog/nanopub-index.yaml
SOURCE_SCHEMA_DIR = $(dir $(SOURCE_SCHEMA_PATH))
PYMODEL = $(SRC)/src/peh_model
OWL_CANONICAL_PATH = $(SRC)/owl/$(SCHEMA_NAME).owl.ttl
OWL_LEGACY_PATH = $(SRC)/owl/$(SCHEMA_NAME).owl
WIDOCO_INPUT_PATH = $(SRC)/owl/$(SCHEMA_NAME).widoco-focus.ttl
WIDOCO_PROFILE_PATH = $(SRC)/docs/widoco-profile.yaml
WIDOCO_DOCS_OUT ?= _site/widoco
HOST_UID ?= $(shell id -u)
HOST_GID ?= $(shell id -g)

CHANGELOG_SCRIPT_PATH=$(SRC)/scripts/changelog.py
PUBLISH_SCRIPT_PATH=$(SRC)/scripts/publish.py
SYNC_VERSION_SCRIPT_PATH=$(SRC)/scripts/sync_versions.py
PACKAGE_INIT_PATH=$(PYMODEL)/__init__.py
CHANGELOG_SCHEMA_PATH=$(SRC)/changelog/changelog.schema.yaml
CHANGELOG_PATH=$(SRC)/changelog/_upcoming.yaml

# ================================
# Phony targets
# ================================
.PHONY: help install setup make-dirs clean lint lint-fix test-schema gen-project check-config serialize publish-nanopubs build-package publish-package-test publish-package push-index widoco-input check-widoco-input check-ontology-docs-input widoco-docs postprocess-widoco-docs serve-widoco-docs

# ================================
# Help
# ================================
help: check-config
	@echo ""
	@echo "make install      			-- create venv and install dependencies"
	@echo "make setup        			-- setup venv and necessary directories"
	@echo "make gen-project        		-- generate all model artefacts"
	@echo "check-env"					-- check presence of required env variables"
	@echo "make make-dirs    			-- create necessary directories"
	@echo "make test-schema  			-- regenerate models and check schema"
	@echo "make lint         			-- lint the schema"
	@echo "make lint-fix     			-- lint-fix the schema and fix issues"
	@echo "make serialize    			-- serialize data examples"
	@echo "make publish-nanopubs    	-- publish model updates"
	@echo "make clean        			-- clean generated files"
	@echo "make build-peh-model			-- build peh-model"
	@echo "make publish-peh-model-test	-- test publish peh-model"
	@echo "make publish-peh-model		-- publish peh-model"
	@echo "make push-index				-- push uris to nanopub index."
	@echo "make widoco-input			-- generate focused WIDOCO ontology input"
	@echo "make check-widoco-input		-- validate focused WIDOCO ontology input"
	@echo "make widoco-docs			-- generate local WIDOCO documentation preview"
	@echo "make postprocess-widoco-docs	-- rewrite WIDOCO term anchors to local names"
	@echo "make serve-widoco-docs		-- serve local WIDOCO documentation preview"
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
setup: install make-dirs

# ================================
# Install dependencies
# ================================
install:
	@test -d $(VENV) || python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r linkml==$(LINKML_VERSION) black toml

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
	gen-owl --mergeimports --no-metaclasses --no-type-objects --add-root-classes --mixins-as-expressions $(SOURCE_SCHEMA_PATH) > $(OWL_CANONICAL_PATH)
	cp $(OWL_CANONICAL_PATH) $(OWL_LEGACY_PATH)
# MAKE RDF
	gen-rdf $(SOURCE_SCHEMA_PATH) > $(DEST)/peh.ttl
# MAKE PYDANTIC
	gen-pydantic --meta None $(SOURCE_SCHEMA_PATH) > $(PYMODEL)/pydanticmodel_v2.py
# MOVE OUTPUT TO CORRECT FOLDER
	mv $(DEST)/jsonld/*.jsonld $(SRC)/jsonld/.
	mv $(DEST)/peh.py $(PYMODEL)/.
	mv $(DEST)/peh.ttl	$(SRC)/rdf/.
	cp $(SRC)/schema/peh.yaml $(PYMODEL)/schema/.
# RUN BLACK
	black $(PYMODEL)		

# ================================
# sync schema and pyproject.toml version
# ================================
sync-version:
	python3 $(SYNC_VERSION_SCRIPT_PATH) --yaml-file $(SOURCE_SCHEMA_PATH) --toml-file pyproject.toml --init-file $(PACKAGE_INIT_PATH)

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
	mkdir -p $(SRC)/src/peh_model
	mkdir -p $(SRC)/src/peh_model/schema
	mkdir -p $(SRC)/jsonld
	mkdir -p $(SRC)/owl
	mkdir -p $(SRC)/rdf

widoco-input:
	$(PYTHON) $(SRC)/scripts/build_widoco_focus.py $(SOURCE_SCHEMA_PATH) --profile $(WIDOCO_PROFILE_PATH) -o $(WIDOCO_INPUT_PATH)

check-widoco-input: widoco-input
	$(PYTHON) $(SRC)/scripts/validate_widoco_focus.py $(WIDOCO_INPUT_PATH) --schema $(SOURCE_SCHEMA_PATH) --profile $(WIDOCO_PROFILE_PATH)

check-ontology-docs-input:
	@test -f "$(WIDOCO_INPUT_PATH)" || (echo "Missing $(WIDOCO_INPUT_PATH). Run make widoco-input first." && exit 1)

widoco-docs: check-widoco-input check-ontology-docs-input
	mkdir -p $(WIDOCO_DOCS_OUT)
	WIDOCO_DOCS_OUT=./$(WIDOCO_DOCS_OUT) HOST_UID=$(HOST_UID) HOST_GID=$(HOST_GID) docker compose -f docker-compose.widoco.yml run --rm widoco
	$(PYTHON) $(SRC)/scripts/postprocess_widoco_html.py $(WIDOCO_DOCS_OUT)
	@echo "WIDOCO documentation generated in $(WIDOCO_DOCS_OUT)"

postprocess-widoco-docs:
	$(PYTHON) $(SRC)/scripts/postprocess_widoco_html.py $(WIDOCO_DOCS_OUT)

serve-widoco-docs:
	python3 -m http.server 8000 -d $(WIDOCO_DOCS_OUT)

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
publish-nanopubs:
	@echo "Publishing schema"
	python3 "$(CHANGELOG_SCRIPT_PATH)" validate-changelog -s "$(CHANGELOG_SCHEMA_PATH)" "$(CHANGELOG_PATH)"
	@echo "Publish terms in changelog."
	@if [ -f .env ]; then \
		echo "Loading .env file for local development"; \
		set -a && source .env && set +a; \
	else \
		echo "Using environment variables (CI/CD mode)"; \
	fi && \
	python3 $(PUBLISH_SCRIPT_PATH) publish \
		-g $(OWL_CANONICAL_PATH) \
		-s $(SOURCE_SCHEMA_PATH) \
		-c $(CHANGELOG_PATH) \
		--htaccess-path htaccess.txt

push-index:
	@echo "Pushing nanopub index for schema"
	set -a && source .env && set +a && \
	python3 $(PUBLISH_SCRIPT_PATH) push-index \
		-s $(SOURCE_SCHEMA_PATH) \
		--index-file $(INDEX_FILE_PATH)

# ================================
# EXAMPLE NANOPUB
# ================================
example-nanopubs:
	set -a && source .env && set +a && \
	python3 $(PUBLISH_SCRIPT_PATH) example \
		-g $(OWL_CANONICAL_PATH) \
		-s $(SOURCE_SCHEMA_PATH) \
		--element-type class \
		--example-for https://w3id.org/peh/terms/Matrix
	@echo "Matrix example produced."
	set -a && source .env && set +a && \
	python3 $(PUBLISH_SCRIPT_PATH) example \
		-g $(OWL_CANONICAL_PATH) \
		-s $(SOURCE_SCHEMA_PATH) \
		--element-type slot \
		--example-for https://w3id.org/peh/terms/parent_matrix
	@echo "parent_matrix example produced."
	set -a && source .env && set +a && \
	python3 $(PUBLISH_SCRIPT_PATH) example \
		-g $(OWL_CANONICAL_PATH) \
		-s $(SOURCE_SCHEMA_PATH) \
		--element-type enum \
		--example-for https://w3id.org/peh/terms/ValidationStatus
	@echo "ValidationStatus example produced."

# ======================
#     publishing
# ======================
build-peh-model:
	pip install --upgrade build
	python -m build

publish-peh-model-test:
	pip install --upgrade twine
	python -m twine upload --repository testpypi dist/*

publish-peh-model:
	pip install --upgrade twine
	python -m twine upload dist/*
