# Personal Exposure and Health (or PEH) Data Model

## Introduction:
The PEH data model is the result of consolidation and harmonisation efforts in the Human Biomonitoring research field as well as an initiative to broaden the scope and support the inclusion of additional, relevant sources of information. Examples are project contexts and data from exposure related domains, such as environmental and geospatial observations.

The [PEH data model](https://github.com/eu-parc/parco-hbm/tree/main/linkml/schema) is defined using the [linkml](https://linkml.io/) modeling language.

## The data model and its purpose
The aim of this data model is to provide a domain specific structure for the data and metadata involved in typical human biomonitoring and personal exposure research projects, a terminology that supports expressing and annotating the (meta)data using harmonised vocabularies and a simple, more generic abstraction layer (at the "observed data records" level) that facilitates broader, cross-domain interoperability efforts.

In addition to adding semantic context and meaning to projects, studies and datasets that leverage it, the data model provides a stable ground for the development of supporting tools.

## Repository scope
This repository currently serves a dual purpose.

First, it supports the development and publication of the domain-specific ontology for PEH data, including the serializations needed by downstream systems. The ontology mainly supports the annotation of observations and their observable properties. In that role, it aligns with established semantic models such as SOSA and I-ADOPT, while also supporting the construction and maintenance of project vocabularies such as matrices, biochem entities, indicators and related controlled terms.

Second, the repository builds the Python bindings (as data classes) for the model as the published `peh-model` package, installable from PyPI. These generated data models make it possible to configure PEH studies, validate associated data and process it in a way that is compatible with the ontology from the outset. For higher-level tooling built on top of this model, see [`pypeh`](https://github.com/eu-parc/pypeh).

## Citing the PEH model
If you use the PEH model, its ontology serializations or the generated `peh-model` Python package in your work, please cite the version that you used.

Suggested citation:

> Bisschop, G., & contributors. Personal Exposure and Health (PEH) Data Model. Version 0.6.2. GitHub. https://github.com/eu-parc/parco-hbm

BibTeX:

```bibtex
@software{peh_model,
  title = {Personal Exposure and Health (PEH) Data Model},
  author = {Bisschop, Gertjan and contributors},
  version = {0.6.2},
  url = {https://github.com/eu-parc/parco-hbm},
  note = {Ontology, LinkML schema and generated Python data models for PEH data}
}
```

If a DOI is available for the release you used, prefer citing the DOI for that release.
