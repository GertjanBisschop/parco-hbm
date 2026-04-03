from __future__ import annotations

import re
import sys
from datetime import date, datetime, time
from decimal import Decimal
from enum import Enum
from typing import Any, ClassVar, Literal, Optional, Union

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer,
)

metamodel_version = "1.7.0"
version = "0.5.1"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias=True,
        validate_by_name=True,
        validate_assignment=True,
        validate_default=True,
        extra="forbid",
        arbitrary_types_allowed=True,
        use_enum_values=True,
        strict=False,
    )


class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key: str):
        return getattr(self.root, key)

    def __getitem__(self, key: str):
        return self.root[key]

    def __setitem__(self, key: str, value):
        self.root[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self.root


linkml_meta = None


class ValidationStatus(str, Enum):
    unvalidated = "unvalidated"
    in_progress = "in_progress"
    validated = "validated"
    deprecated = "deprecated"


class ValidationCommand(str, Enum):
    is_equal_to = "is_equal_to"
    is_equal_to_or_both_missing = "is_equal_to_or_both_missing"
    is_greater_than_or_equal_to = "is_greater_than_or_equal_to"
    is_greater_than = "is_greater_than"
    is_less_than_or_equal_to = "is_less_than_or_equal_to"
    is_less_than = "is_less_than"
    is_not_equal_to = "is_not_equal_to"
    is_not_equal_to_and_not_both_missing = "is_not_equal_to_and_not_both_missing"
    is_unique = "is_unique"
    is_duplicated = "is_duplicated"
    is_in = "is_in"
    is_null = "is_null"
    is_not_null = "is_not_null"
    conjunction = "conjunction"
    disjunction = "disjunction"


class ValidationErrorLevel(str, Enum):
    info = "info"
    warning = "warning"
    error = "error"
    fatal = "fatal"


class DataLayoutElementStyle(str, Enum):
    standard = "standard"
    main_title = "main_title"
    section_title = "section_title"
    sub_title = "sub_title"
    comment = "comment"
    warning = "warning"
    alert = "alert"


class IndicatorType(str, Enum):
    effectmarker = "effectmarker"
    exposuremarker = "exposuremarker"
    geomarker = "geomarker"
    observation = "observation"


class BioChemEntityType(str, Enum):
    compound_group = "compound_group"
    compound = "compound"
    conjugated_compound = "conjugated_compound"
    unconjugated_compound = "unconjugated_compound"


class ResearchPopulationType(str, Enum):
    general_population = "general_population"
    person = "person"
    newborn = "newborn"
    adolescent = "adolescent"
    mother = "mother"
    parent = "parent"
    pregnant_person = "pregnant_person"
    household = "household"


class ObservableEntityType(str, Enum):
    project = "project"
    organisation = "organisation"
    study = "study"
    environment = "environment"
    location = "location"
    persongroup = "persongroup"
    person = "person"
    samplegroup = "samplegroup"
    sample = "sample"
    dataset = "dataset"
    collection_process = "collection_process"
    lab_analysis_process = "lab_analysis_process"
    model_execution_process = "model_execution_process"
    data_process = "data_process"


class ObservationType(str, Enum):
    sampling = "sampling"
    questionnaire = "questionnaire"
    fieldwork = "fieldwork"
    geospatial = "geospatial"
    metadata = "metadata"


class ObservablePropertySpecificationCategory(str, Enum):
    identifying = "identifying"
    """
    Used to uniquely identify the ObservableEntity
    """
    required = "required"
    """
    Must be provided for the observation to be valid
    """
    optional = "optional"
    """
    May be provided but not required
    """
    derived = "derived"
    """
    Is calculated from other ObservableProperties
    """


class ObservationResultType(str, Enum):
    measurement = "measurement"
    control = "control"
    calculation = "calculation"
    simulation = "simulation"


class DataLayoutSectionType(str, Enum):
    data_form = "data_form"
    data_table = "data_table"
    property_table = "property_table"


class DataLayoutElementType(str, Enum):
    text = "text"
    spacer = "spacer"
    data_field = "data_field"


class ObjectiveType(str, Enum):
    research_objective = "research_objective"
    project_result = "project_result"
    publication = "publication"


class LinkType(str, Enum):
    is_about = "is_about"
    is_same_as = "is_same_as"
    is_part_of = "is_part_of"
    is_located_at = "is_located_at"


class ContactRole(str, Enum):
    administrative = "administrative"
    data = "data"
    general = "general"
    lead = "lead"
    legal = "legal"
    technical = "technical"


class ProjectRole(str, Enum):
    member = "member"
    partner = "partner"
    funding_partner = "funding_partner"
    principal_investigator = "principal_investigator"
    data_governance = "data_governance"
    data_controller = "data_controller"
    data_processor = "data_processor"
    data_user = "data_user"
    lab = "lab"


class StudyRole(str, Enum):
    funding_partner = "funding_partner"
    principal_investigator = "principal_investigator"
    data_controller = "data_controller"
    data_processor = "data_processor"
    data_user = "data_user"
    lab = "lab"


class DataRole(str, Enum):
    main_stakeholder = "main_stakeholder"
    supplying_data_controller = "supplying_data_controller"
    receiving_data_controller = "receiving_data_controller"
    external_data_controller = "external_data_controller"


class EntityList(ConfiguredBaseModel):
    """
    A generic top level object for collecting named entities under one root entity
    """

    metadata_fields: Optional[list[ObservablePropertyMetadataField]] = Field(
        default=None
    )
    groupings: Optional[list[Grouping]] = Field(default=None)
    observable_properties: Optional[list[ObservableProperty]] = Field(default=None)
    stakeholders: Optional[list[Stakeholder]] = Field(default=None)
    projects: Optional[list[Project]] = Field(default=None)
    studies: Optional[list[Study]] = Field(default=None)
    study_entities: Optional[list[StudyEntity]] = Field(default=None)
    physical_entities: Optional[list[PhysicalEntity]] = Field(default=None)
    observation_groups: Optional[list[ObservationGroup]] = Field(default=None)
    observations: Optional[list[Observation]] = Field(default=None)
    derived_observations: Optional[list[DerivedObservation]] = Field(default=None)
    observation_designs: Optional[list[ObservationDesign]] = Field(default=None)
    observation_results: Optional[list[ObservationResult]] = Field(default=None)
    observed_values: Optional[list[ObservedValue]] = Field(default=None)
    layouts: Optional[list[DataLayout]] = Field(default=None)
    import_configs: Optional[list[DataImportConfig]] = Field(default=None)
    data_requests: Optional[list[DataRequest]] = Field(default=None)
    matrix_subclasses: Optional[list[MatrixSubClass]] = Field(default=None)
    biochementity_subclasses: Optional[list[BioChemEntitySubClass]] = Field(
        default=None
    )
    indicator_subclasses: Optional[list[IndicatorSubClass]] = Field(default=None)


class NamedThing(ConfiguredBaseModel):
    """
    An abstract model for any of the identifiable entities
    """

    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class HasValidationStatus(ConfiguredBaseModel):
    """
    The capacity of including both a current validation status and a history of validation records
    """

    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[list[ValidationHistoryRecord]] = Field(default=None)


class ValidationHistoryRecord(ConfiguredBaseModel):
    """
    A list of events representing a historical record on the entity validation status
    """

    validation_datetime: Optional[datetime] = Field(default=None)
    validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_actor: Optional[str] = Field(default=None)
    validation_institute: Optional[str] = Field(default=None)
    validation_remark: Optional[str] = Field(default=None)


class HasAliases(ConfiguredBaseModel):
    """
    The capacity of including one or more alternative naming terms (without qualifying the usage context)
    """

    aliases: Optional[list[str]] = Field(default=None)


class HasContextAliases(ConfiguredBaseModel):
    """
    The capacity of including a list of terms being used in known scopes or contexts
    """

    context_aliases: Optional[list[ContextAlias]] = Field(default=None)


class ContextAlias(ConfiguredBaseModel):
    """
    An alternative term as it is used in a known scope or context (e.g. a community, project or study) for any of the entities and its properties
    """

    property_name: Optional[str] = Field(default=None)
    context: Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)


class HasTranslations(ConfiguredBaseModel):
    """
    The capacity of including a list of translated terms for one or more entity properties and languages
    """

    translations: Optional[list[Translation]] = Field(default=None)


class Grouping(HasTranslations, HasContextAliases, NamedThing):
    """
    A generic grouping entity that allows categorising entities in a hierarchical structure
    """

    parent_grouping_id_list: Optional[list[str]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class Translation(ConfiguredBaseModel):
    """
    A translation for any of the entity properties, defining the property, the language and the translated term
    """

    property_name: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    translated_value: Optional[str] = Field(default=None)


class BioChemEntity(
    HasTranslations, HasContextAliases, HasAliases, HasValidationStatus, NamedThing
):
    """
    A biological, chemical or biochemical entity that is relevant to the Personal Exposure and Health domain
    """

    aliases: Optional[list[str]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[list[ValidationHistoryRecord]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class BioChemEntitySubClass(
    HasTranslations, HasContextAliases, HasAliases, HasValidationStatus, NamedThing
):
    """
    Template class used to generate OWL Classes.
    """

    grouping_id_list: Optional[list[str]] = Field(default=None)
    biochementity_type: Optional[BioChemEntityType] = Field(default=None)
    molweight_grampermol: Optional[Decimal] = Field(default=None)
    parent_compounds: Optional[list[str]] = Field(default=None)
    group_compound_members: Optional[list[str]] = Field(
        default=None,
        description="""For a compound that groups other compounds, links to members of the group. Inverse of the BioChemEntity member_of_group_compounds slot""",
    )
    member_of_group_compounds: Optional[list[str]] = Field(
        default=None,
        description="""Declares the compound being part of one or more group compounds. Inverse of the BioChemEntity group_compound_members slot""",
    )
    aliases: Optional[list[str]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[list[ValidationHistoryRecord]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class Matrix(HasTranslations, HasContextAliases, NamedThing):
    """
    The physical medium or biological substrate from which a biomarker, or other analyte is quantified in observational studies
    """

    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class MatrixSubClass(HasTranslations, HasContextAliases, NamedThing):
    """
    Template class used to generate OWL Classes.

    """

    parent_matrix: Optional[str] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class Indicator(NamedThing):
    """
    Any measurable or observable variable that can describe data or context in the Personal Exposure and Health domain
    """

    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class IndicatorSubClass(HasTranslations, HasContextAliases, NamedThing):
    """
    Template class used to generate OWL Classes
    """

    indicator_type: Optional[IndicatorType] = Field(default=None)
    property: Optional[str] = Field(default=None)
    quantity_kind: Optional[str] = Field(default=None)
    matrix: Optional[str] = Field(default=None)
    constraints: Optional[list[str]] = Field(default=None)
    grouping_id_list: Optional[list[str]] = Field(default=None)
    relevant_observable_entity_types: Optional[list[ObservableEntityType]] = Field(
        default=None
    )
    biochementity: Optional[str] = Field(default=None)
    parent_indicator: Optional[str] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class QUDTUnit(ConfiguredBaseModel):
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )


class QUDTQuantityKind(ConfiguredBaseModel):
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )


class PhysicalEntity(NamedThing):
    """
    A digital placeholder for a physical entity as it exists in the real world,
    """

    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class PhysicalEntityLink(ConfiguredBaseModel):
    """
    A relational property that allows creating qualified links to physical entities
    """

    linktype: Optional[LinkType] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)


class Sample(PhysicalEntity):
    """
    A portion of a measurement matrix collected from a subject or environment for the purpose of lab analysis
    """

    matrix: Optional[str] = Field(default=None)
    constraints: Optional[list[str]] = Field(default=None)
    sampled_in_project: Optional[str] = Field(default=None)
    physical_label: Optional[str] = Field(default=None)
    collection_date: Optional[date] = Field(default=None)
    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class Person(PhysicalEntity):
    """
    A human subject or stakeholder in Personal Exposure and Health research
    """

    recruited_in_project: Optional[str] = Field(default=None)
    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class Geolocation(PhysicalEntity):
    """
    A geographic location relevant to the Personal Exposure and Health projects or studies
    """

    location: Optional[str] = Field(default=None)
    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class Environment(PhysicalEntity):
    """
    An environment relevant to the research, typically related to the exposure of a person
    """

    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class HomeEnvironment(Environment):
    """
    A home environment relevant to the research, typically related to the at-home exposure of a person
    """

    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class WorkEnvironment(Environment):
    """
    A work environment relevant to the research, typically related to the at-work or commute exposure of a person
    """

    physical_entity_links: Optional[list[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class ObservableProperty(HasTranslations, HasContextAliases, NamedThing):
    """
    A fully defined variable that allows registering an observation about any of the entities relevant to Personal Exposure and Health research
    """

    value_type: Optional[str] = Field(default=None)
    categorical: Optional[bool] = Field(default=None)
    multivalued: Optional[bool] = Field(default=None)
    value_options: Optional[list[ObservablePropertyValueOption]] = Field(default=None)
    value_metadata: Optional[list[ObservablePropertyMetadataElement]] = Field(
        default=None
    )
    quantity_kind: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    required: Optional[bool] = Field(default=None)
    zeroallowed: Optional[bool] = Field(default=None)
    min_value: Optional[str] = Field(
        default=None,
        description="""String representation of the expected lower bound in observations, usable for data validation""",
    )
    max_value: Optional[str] = Field(
        default=None,
        description="""String representation of the expected upper bound in observations, usable for data validation""",
    )
    significantdecimals: Optional[int] = Field(
        default=None,
        description="""Variable precision indication, expressed as the number of significant decimals""",
    )
    immutable: Optional[bool] = Field(
        default=None,
        description="""Variable values are not expected to change over time (e.g. birthdate of a person)""",
    )
    grouping_id_list: Optional[list[str]] = Field(default=None)
    observation_result_type: Optional[ObservationResultType] = Field(default=None)
    relevant_observable_entity_types: Optional[list[ObservableEntityType]] = Field(
        default=None
    )
    relevant_observation_types: Optional[list[ObservationType]] = Field(default=None)
    calculation_design: Optional[CalculationDesign] = Field(default=None)
    validation_designs: Optional[list[ValidationDesign]] = Field(default=None)
    has_observable_property_type: Optional[list[str]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class ObservablePropertyValueOption(HasContextAliases):
    """
    Potential selection choices for Observable Properties that are categorical variables
    """

    key: Optional[str] = Field(default=None)
    value: Optional[str] = Field(
        default=None,
        description="""String representation of a measured or configured value, to be parsed according to the corresponding value type""",
    )
    label: Optional[str] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)


class ObservablePropertyMetadataElement(ConfiguredBaseModel):
    """
    Key-value element that adds contextual metadata to an Observable Property instance
    """

    field: Optional[str] = Field(default=None)
    value: Optional[str] = Field(
        default=None,
        description="""String representation of a measured or configured value, to be parsed according to the corresponding value type""",
    )


class ObservablePropertyMetadataField(NamedThing):
    """
    Predefined contextual qualifier for Observable Property metadata
    """

    value_type: Optional[str] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class CalculationDesign(ConfiguredBaseModel):
    """
    Definition of a calculation method for deriving an observational value from other variables and/or contexts
    """

    calculation_name: Optional[str] = Field(default=None)
    calculation_implementation_as_json: Optional[str] = Field(default=None)
    calculation_implementation: Optional[CalculationImplementation] = Field(
        default=None
    )
    conditional: Optional[str] = Field(default=None)


class CalculationImplementation(ConfiguredBaseModel):
    """
    Reference and parameters mapping to the implementation that can perform the intended calculation
    """

    function_name: Optional[str] = Field(default=None)
    function_kwargs: Optional[list[CalculationKeywordArgument]] = Field(default=None)
    function_results: Optional[list[CalculationResult]] = Field(default=None)


class CalculationKeywordArgument(ConfiguredBaseModel):
    """
    The definition of a named argument used in the calculation, including the information needed to pick it from the project or study data structure
    """

    mapping_name: Optional[str] = Field(default=None)
    process_state: Optional[str] = Field(default=None)
    imputation_state: Optional[str] = Field(default=None)
    value_type: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)
    contextual_field_reference: Optional[ContextualFieldReference] = Field(default=None)


class CalculationResult(ConfiguredBaseModel):
    """
    The definition for the output the calculation, optionally including mapping information
    """

    mapping_name: Optional[str] = Field(default=None)
    value_type: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    round_decimals: Optional[int] = Field(default=None)
    scale_factor: Optional[Decimal] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)
    contextual_field_reference: Optional[ContextualFieldReference] = Field(default=None)


class ValidationDesign(ConfiguredBaseModel):
    """
    Definition of a validation rule for automatically imposing business logic constraints
    """

    validation_name: Optional[str] = Field(default=None)
    validation_expression: Optional[ValidationExpression] = Field(default=None)
    validation_error_level: Optional[ValidationErrorLevel] = Field(default=None)
    validation_error_message_template: Optional[str] = Field(default=None)
    conditional: Optional[str] = Field(default=None)


class ValidationExpression(ConfiguredBaseModel):
    """
    A logical expression, allowing for combining arguments into more complex validation rules
    """

    validation_subject_contextual_field_references: Optional[
        list[ContextualFieldReference]
    ] = Field(default=None)
    validation_condition_expression: Optional[ValidationExpression] = Field(
        default=None
    )
    validation_command: Optional[ValidationCommand] = Field(default=None)
    validation_arg_values: Optional[list[str]] = Field(default=None)
    validation_arg_contextual_field_references: Optional[
        list[ContextualFieldReference]
    ] = Field(default=None)
    validation_arg_expressions: Optional[list[ValidationExpression]] = Field(
        default=None
    )


class ContextualFieldReference(ConfiguredBaseModel):
    """
    A two-level reference, identifying a field or column in a named series of two-dimensional datasets
    """

    dataset_label: Optional[str] = Field(default=None)
    field_label: Optional[str] = Field(default=None)


class Contact(HasContextAliases):
    """
    A stakeholder having a contact role in the research process
    """

    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    orcid: Optional[str] = Field(default=None)
    contact_roles: Optional[list[ContactRole]] = Field(default=None)
    contact_email: Optional[str] = Field(default=None)
    contact_phone: Optional[str] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)


class Stakeholder(HasTranslations, NamedThing):
    """
    Any organisation involved in the research process
    """

    rorid: Optional[str] = Field(default=None)
    geographic_scope: Optional[str] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class ProjectStakeholder(HasTranslations):
    """
    An organisation collaborating in a Personal Exposure and Health research project
    """

    stakeholder: Optional[str] = Field(default=None)
    project_roles: Optional[list[ProjectRole]] = Field(default=None)
    contacts: Optional[list[Contact]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)


class StudyEntity(NamedThing):
    """
    Any entity carrying data or context relevant to a Personal Exposure and Health research project or study
    """

    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class Project(StudyEntity, HasTranslations, HasContextAliases):
    """
    A collaborative effort in the Personal Exposure and Health research domain
    """

    default_language: Optional[str] = Field(default=None)
    project_stakeholders: Optional[list[ProjectStakeholder]] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    study_id_list: Optional[list[str]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class StudyEntityLink(ConfiguredBaseModel):
    """
    A relational property that allows creating qualified links to study entities
    """

    linktype: Optional[LinkType] = Field(default=None)
    study_entity: Optional[str] = Field(default=None)


class Study(StudyEntity, HasTranslations, HasContextAliases):
    """
    A structured, goal-directed observational investigation designed to collect and analyze data on human subjects and their environments
    """

    default_language: Optional[str] = Field(default=None)
    study_stakeholders: Optional[list[StudyStakeholder]] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    observation_group_id_list: Optional[list[str]] = Field(default=None)
    study_entity_id_list: Optional[list[str]] = Field(default=None)
    project_id_list: Optional[list[str]] = Field(default=None)
    translations: Optional[list[Translation]] = Field(default=None)
    context_aliases: Optional[list[ContextAlias]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class StudyStakeholder(ConfiguredBaseModel):
    """
    An organisation collaborating in a Personal Exposure and Health research study
    """

    stakeholder: Optional[str] = Field(default=None)
    study_roles: Optional[list[StudyRole]] = Field(default=None)
    contacts: Optional[list[Contact]] = Field(default=None)


class ObservationGroup(StudyEntity):
    """
    A grouped collection of observations, intended and/or executed, as part of a Personal Exposure and Health research study
    """

    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    observation_id_list: Optional[list[str]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class StudyPopulation(StudyEntity):
    """
    A group of study entities that is itself also a study entity that observations can be recorded for
    """

    research_population_type: Optional[ResearchPopulationType] = Field(default=None)
    member_id_list: Optional[list[str]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class SampleCollection(StudyEntity):
    """
    A collection of samples that is itself also a study entity that observations can be recorded for
    """

    matrix: Optional[str] = Field(default=None)
    constraints: Optional[list[str]] = Field(default=None)
    sample_id_list: Optional[list[str]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class StudySubject(StudyEntity):
    """
    A study entity that is a main subject for the study
    """

    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class StudySubjectGroup(StudyEntity):
    """
    A group of study subjects that is itself also a study entity that observations can be recorded for
    """

    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[list[StudyEntityLink]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class Observation(NamedThing):
    """
    The registration of the intent to perform a set of observations as well as the resulting observed values
    """

    observation_type: Optional[ObservationType] = Field(default=None)
    observation_design: Optional[str] = Field(default=None)
    observation_result_id_list: Optional[list[str]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class DerivedObservation(Observation):
    """
    An observation in which all observed values are derived from a prior observation through analytical or statistical processing.
    """

    was_derived_from: Optional[str] = Field(default=None)
    observation_type: Optional[ObservationType] = Field(default=None)
    observation_design: Optional[str] = Field(default=None)
    observation_result_id_list: Optional[list[str]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class ObservationDesign(NamedThing):
    """
    The setup of the observation, listing the study entity type being observed (and -optionally- the entities), as well as the the properties being recorded
    """

    observation_result_type: Optional[ObservationResultType] = Field(default=None)
    observable_entity_type: Optional[ObservableEntityType] = Field(default=None)
    observable_entity_id_list: Optional[list[str]] = Field(default=None)
    observable_property_specifications: Optional[
        list[ObservablePropertySpecification]
    ] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class ObservablePropertySpecification(ConfiguredBaseModel):
    """
    For an observable property being recorded, lists its categorisation and processing rules
    """

    observable_property: Optional[str] = Field(default=None)
    specification_category: Optional[ObservablePropertySpecificationCategory] = Field(
        default=None
    )
    calculation_design: Optional[CalculationDesign] = Field(default=None)
    validation_designs: Optional[list[ValidationDesign]] = Field(default=None)


class ObservationResult(NamedThing):
    """
    The result of an observational effort in Personal Exposure and Health research
    """

    observation_result_type: Optional[ObservationResultType] = Field(default=None)
    observation_start_date: Optional[date] = Field(default=None)
    observation_end_date: Optional[date] = Field(default=None)
    observed_values: Optional[list[ObservedValue]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class ObservedValue(ConfiguredBaseModel):
    """
    A single observational result value registering a specific property for a specific entity at a specific moment
    """

    observable_entity: Optional[str] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)
    raw_value: Optional[str] = Field(default=None)
    raw_unit: Optional[str] = Field(default=None)
    imputed_value: Optional[str] = Field(default=None)
    imputed_unit: Optional[str] = Field(default=None)
    normalised_value: Optional[str] = Field(default=None)
    normalised_unit: Optional[str] = Field(default=None)
    value: Optional[str] = Field(
        default=None,
        description="""String representation of a measured or configured value, to be parsed according to the corresponding value type""",
    )
    unit: Optional[str] = Field(default=None)
    value_as_string: Optional[str] = Field(default=None)
    quality_data: Optional[list[QualityData]] = Field(default=None)
    provenance_data: Optional[list[ProvenanceData]] = Field(default=None)


class QualityData(ConfiguredBaseModel):
    """
    Quality metadata, adding context to an Observed Value
    """

    quality_context_key: Optional[str] = Field(default=None)
    quality_value: Optional[str] = Field(default=None)


class ProvenanceData(ConfiguredBaseModel):
    """
    Provenance metadata, adding context to an Observed Value
    """

    provenance_context_key: Optional[str] = Field(default=None)
    provenance_value: Optional[str] = Field(default=None)


class DataLayout(NamedThing):
    """
    Layout, allowing the definition of templating sections for combining layout and data elements
    """

    sections: Optional[list[DataLayoutSection]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class DataLayoutSection(NamedThing):
    """
    Definition for an individual layout or data section, as part of a full layout. Each section contains the information on a single observation.
    """

    section_type: Optional[DataLayoutSectionType] = Field(default=None)
    observable_entity_type: Optional[ObservableEntityType] = Field(default=None)
    elements: Optional[list[DataLayoutElement]] = Field(default=None)
    validation_designs: Optional[list[ValidationDesign]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class DataLayoutElement(ConfiguredBaseModel):
    """
    Definition for an individual layout or data element, as part of a layout section
    """

    label: Optional[str] = Field(default=None)
    element_type: Optional[DataLayoutElementType] = Field(default=None)
    element_style: Optional[DataLayoutElementStyle] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)
    is_observable_entity_key: Optional[bool] = Field(default=None)
    foreign_key_link: Optional[DataLayoutElementLink] = Field(default=None)


class DataLayoutElementLink(ConfiguredBaseModel):
    """
    Configuration that refers to an element in a layout section
    """

    section: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)


class DataImportConfig(NamedThing):
    """
    Configuration for incoming data, defining the expected DataLayout and the Observation(s) the data will be added to
    """

    layout: Optional[str] = Field(default=None)
    section_mapping: Optional[DataImportSectionMapping] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class DataImportSectionMapping(ConfiguredBaseModel):
    """
    Configuration for mapping structured data from a known layout to one or more study observations
    """

    section_mapping_links: Optional[list[DataImportSectionMappingLink]] = Field(
        default=None
    )


class DataImportSectionMappingLink(ConfiguredBaseModel):
    """
    Configuration that links a data layout section to one or more observations
    """

    section: Optional[str] = Field(default=None)
    observation_id_list: Optional[list[str]] = Field(default=None)


class DataRequest(NamedThing):
    """
    Registration of a request for data by a data user
    """

    contacts: Optional[list[Contact]] = Field(default=None)
    request_properties: Optional[str] = Field(default=None)
    data_stakeholders: Optional[list[str]] = Field(default=None)
    research_objectives: Optional[list[str]] = Field(default=None)
    processing_actions: Optional[list[str]] = Field(default=None)
    processing_steps: Optional[list[str]] = Field(default=None)
    remark_on_content: Optional[str] = Field(default=None)
    remark_on_methodology: Optional[str] = Field(default=None)
    observed_entity_properties: Optional[list[ObservedEntityProperty]] = Field(
        default=None
    )
    observation_design_id_list: Optional[list[str]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class ObservedEntityProperty(ConfiguredBaseModel):
    """
    Conceptual definition of the observation of a certain property for a certain entity in a study
    """

    observable_entity: Optional[str] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)


class DataStakeholder(NamedThing):
    """
    An organisation participating in a data process in Personal Exposure and Health research
    """

    stakeholder: Optional[str] = Field(default=None)
    data_roles: Optional[list[DataRole]] = Field(default=None)
    contacts: Optional[list[Contact]] = Field(default=None)
    processing_description: Optional[str] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class ResearchObjective(NamedThing):
    """
    A research objective communicated in the request and used to evaluate if the request is valid and appropriate
    """

    objective_type: Optional[ObjectiveType] = Field(default=None)
    authors: Optional[list[str]] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class ProcessingAction(NamedThing):
    """
    One action in the data request and processing flow
    """

    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class ProcessingStep(NamedThing):
    """
    One step in the data request and processing flow
    """

    start_date: Optional[date] = Field(default=None)
    delivery_date: Optional[date] = Field(default=None)
    id: str = Field(
        default=...,
        description="""Machine readable, unique identifier; ideally a URI/GUPRI (Globally Unique, Persistent, Resolvable Identifier).""",
    )
    short_name: Optional[str] = Field(
        default=None,
        description="""Shortened name or code, preferrably unique within the context the entity is (typically) used in.""",
    )
    name: Optional[str] = Field(
        default=None, description="""Common human readable name"""
    )
    ui_label: Optional[str] = Field(
        default=None,
        description="""Human readable label, to be used in user interactions through forms or documents.""",
    )
    description: Optional[str] = Field(
        default=None,
        description="""Long form description or definition for the entity.""",
    )
    remark: Optional[str] = Field(
        default=None,
        description="""Additional comment, note or remark providing context on the use of an entity or the interpretation of its properties.""",
    )
    exact_matches: Optional[list[str]] = Field(default=None)


class DataExtract(ConfiguredBaseModel):
    """
    A set of Observed Values, combined into a data extract
    """

    observed_values: Optional[list[ObservedValue]] = Field(default=None)


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
EntityList.model_rebuild()
NamedThing.model_rebuild()
HasValidationStatus.model_rebuild()
ValidationHistoryRecord.model_rebuild()
HasAliases.model_rebuild()
HasContextAliases.model_rebuild()
ContextAlias.model_rebuild()
HasTranslations.model_rebuild()
Grouping.model_rebuild()
Translation.model_rebuild()
BioChemEntity.model_rebuild()
BioChemEntitySubClass.model_rebuild()
Matrix.model_rebuild()
MatrixSubClass.model_rebuild()
Indicator.model_rebuild()
IndicatorSubClass.model_rebuild()
QUDTUnit.model_rebuild()
QUDTQuantityKind.model_rebuild()
PhysicalEntity.model_rebuild()
PhysicalEntityLink.model_rebuild()
Sample.model_rebuild()
Person.model_rebuild()
Geolocation.model_rebuild()
Environment.model_rebuild()
HomeEnvironment.model_rebuild()
WorkEnvironment.model_rebuild()
ObservableProperty.model_rebuild()
ObservablePropertyValueOption.model_rebuild()
ObservablePropertyMetadataElement.model_rebuild()
ObservablePropertyMetadataField.model_rebuild()
CalculationDesign.model_rebuild()
CalculationImplementation.model_rebuild()
CalculationKeywordArgument.model_rebuild()
CalculationResult.model_rebuild()
ValidationDesign.model_rebuild()
ValidationExpression.model_rebuild()
ContextualFieldReference.model_rebuild()
Contact.model_rebuild()
Stakeholder.model_rebuild()
ProjectStakeholder.model_rebuild()
StudyEntity.model_rebuild()
Project.model_rebuild()
StudyEntityLink.model_rebuild()
Study.model_rebuild()
StudyStakeholder.model_rebuild()
ObservationGroup.model_rebuild()
StudyPopulation.model_rebuild()
SampleCollection.model_rebuild()
StudySubject.model_rebuild()
StudySubjectGroup.model_rebuild()
Observation.model_rebuild()
DerivedObservation.model_rebuild()
ObservationDesign.model_rebuild()
ObservablePropertySpecification.model_rebuild()
ObservationResult.model_rebuild()
ObservedValue.model_rebuild()
QualityData.model_rebuild()
ProvenanceData.model_rebuild()
DataLayout.model_rebuild()
DataLayoutSection.model_rebuild()
DataLayoutElement.model_rebuild()
DataLayoutElementLink.model_rebuild()
DataImportConfig.model_rebuild()
DataImportSectionMapping.model_rebuild()
DataImportSectionMappingLink.model_rebuild()
DataRequest.model_rebuild()
ObservedEntityProperty.model_rebuild()
DataStakeholder.model_rebuild()
ResearchObjective.model_rebuild()
ProcessingAction.model_rebuild()
ProcessingStep.model_rebuild()
DataExtract.model_rebuild()
