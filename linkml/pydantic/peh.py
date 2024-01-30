from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any, Union
from decimal import Decimal
from pydantic import BaseModel as BaseModel, ConfigDict,  Field, field_validator
import re
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


metamodel_version = "None"
version = "None"

class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment=True,
        validate_default=True,
        extra = 'forbid',
        arbitrary_types_allowed=True,
        use_enum_values = True)


class ValidationStatus(str, Enum):
    
    
    unvalidated = "unvalidated"
    
    in_progress = "in_progress"
    
    validated = "validated"
    
    

class IndicatorType(str, Enum):
    
    
    effectmarker = "effectmarker"
    
    exposuremarker = "exposuremarker"
    
    geomarker = "geomarker"
    
    observation = "observation"
    
    

class BioChemEntityLinkType(str, Enum):
    
    
    exact_match = "exact_match"
    
    close_match = "close_match"
    
    broader = "broader"
    
    part_of = "part_of"
    
    group_contains = "group_contains"
    
    

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
    
    
    person = "person"
    
    persongroup = "persongroup"
    
    environment = "environment"
    
    location = "location"
    
    study = "study"
    
    dataset = "dataset"
    
    sample = "sample"
    
    

class ObservationType(str, Enum):
    
    
    sampling = "sampling"
    
    questionnaire = "questionnaire"
    
    geospatial = "geospatial"
    
    metadata = "metadata"
    
    

class ObjectiveType(str, Enum):
    
    
    research_objective = "research_objective"
    
    project_result = "project_result"
    
    publication = "publication"
    
    

class LinkType(str, Enum):
    
    
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
    
    

class StudyRole(str, Enum):
    
    
    funding_partner = "funding_partner"
    
    principal_investigator = "principal_investigator"
    
    data_controller = "data_controller"
    
    data_processor = "data_processor"
    
    data_user = "data_user"
    
    

class DataRole(str, Enum):
    
    
    main_stakeholder = "main_stakeholder"
    
    supplying_data_controller = "supplying_data_controller"
    
    receiving_data_controller = "receiving_data_controller"
    
    external_data_controller = "external_data_controller"
    
    

class QudtUnit(str):
    
    
    dummy = "dummy"
    

class QudtQuantityKind(str, Enum):
    
    
    MassConcentration = "MassConcentration"
    
    Period = "Period"
    
    

class EntityList(ConfiguredBaseModel):
    
    matrices: Optional[List[Matrix]] = Field(default_factory=list)
    metadata_fields: Optional[List[ObservablePropertyMetadataField]] = Field(default_factory=list)
    biochementities: Optional[List[BioChemEntity]] = Field(default_factory=list)
    biochemgroupings: Optional[List[BioChemGrouping]] = Field(default_factory=list)
    indicators: Optional[List[Indicator]] = Field(default_factory=list)
    units: Optional[List[Unit]] = Field(default_factory=list)
    observable_property_groups: Optional[List[ObservablePropertyGroup]] = Field(default_factory=list)
    observable_properties: Optional[List[ObservableProperty]] = Field(default_factory=list)
    stakeholders: Optional[List[Stakeholder]] = Field(default_factory=list)
    projects: Optional[List[Project]] = Field(default_factory=list)
    studies: Optional[List[Study]] = Field(default_factory=list)
    timepoints: Optional[List[Timepoint]] = Field(default_factory=list)
    
        

class NamedThing(ConfiguredBaseModel):
    """
    A generic grouping for any identifiable entity
    """
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class HasValidationStatus(ConfiguredBaseModel):
    
    current_validation_status: Optional[ValidationStatus] = Field(None)
    validation_history: Optional[List[ValidationHistoryRecord]] = Field(default_factory=list)
    
        

class ValidationHistoryRecord(ConfiguredBaseModel):
    
    validation_datetime: Optional[datetime ] = Field(None)
    validation_status: Optional[ValidationStatus] = Field(None)
    validation_actor: Optional[str] = Field(None)
    validation_remark: Optional[str] = Field(None)
    
        

class HasAliases(ConfiguredBaseModel):
    
    aliases: Optional[List[str]] = Field(default_factory=list)
    
        

class HasContextAliases(ConfiguredBaseModel):
    
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    
        

class ContextAlias(ConfiguredBaseModel):
    
    context: Optional[str] = Field(None)
    alias: Optional[str] = Field(None)
    
        

class HasTranslations(ConfiguredBaseModel):
    
    translations: Optional[List[Translation]] = Field(default_factory=list)
    
        

class Translation(ConfiguredBaseModel):
    
    property_name: Optional[str] = Field(None)
    language: Optional[str] = Field(None)
    translated_value: Optional[str] = Field(None)
    
        

class Unit(HasTranslations, HasContextAliases, NamedThing):
    
    same_unit_as: Optional[QudtUnit] = Field(None)
    quantity_kind: Optional[QudtQuantityKind] = Field(None)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    translations: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class BioChemGrouping(HasTranslations, HasContextAliases, NamedThing):
    
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    translations: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class BioChemEntity(HasTranslations, HasContextAliases, HasAliases, HasValidationStatus, NamedThing):
    """
    A biological, chemical or biochemical entity that is relevant to the Personal Exposure and Health domain
    """
    grouping: Optional[str] = Field(None)
    biochemidentifiers: Optional[List[BioChemIdentifier]] = Field(default_factory=list)
    aliases: Optional[List[str]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    translations: Optional[List[Translation]] = Field(default_factory=list)
    current_validation_status: Optional[ValidationStatus] = Field(None)
    validation_history: Optional[List[ValidationHistoryRecord]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class BioChemIdentifier(HasValidationStatus):
    
    identifier_schema: Optional[str] = Field(None)
    identifier_code: Optional[str] = Field(None)
    current_validation_status: Optional[ValidationStatus] = Field(None)
    validation_history: Optional[List[ValidationHistoryRecord]] = Field(default_factory=list)
    
        

class BioChemIdentifierSchema(NamedThing):
    
    web_uri: Optional[str] = Field(None)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class Matrix(HasTranslations, HasContextAliases, NamedThing):
    
    sort_order: Optional[Decimal] = Field(None)
    aggregation_target: Optional[bool] = Field(None)
    parent_matrix: Optional[str] = Field(None)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    translations: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class Indicator(NamedThing):
    """
    A measurable indicator that is relevant to the Personal Exposure and Health domain
    """
    indicator_type: Optional[IndicatorType] = Field(None)
    quantity_kind: Optional[QudtQuantityKind] = Field(None)
    matrix: Optional[str] = Field(None)
    constraints: Optional[List[str]] = Field(default_factory=list)
    relevant_observable_entity_types: Optional[List[ObservableEntityType]] = Field(default_factory=list)
    biochementity_links: Optional[List[BioChemEntityLink]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class BioChemEntityLink(ConfiguredBaseModel):
    
    biochementity_linktype: Optional[BioChemEntityLinkType] = Field(None)
    biochementity: Optional[str] = Field(None)
    
        

class ObservablePropertyGroup(HasTranslations, NamedThing):
    
    sort_order: Optional[Decimal] = Field(None)
    is_abstract: Optional[bool] = Field(None)
    parent_groups: Optional[List[str]] = Field(default_factory=list)
    translations: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class ObservableProperty(HasTranslations, NamedThing):
    
    value_type: Optional[str] = Field(None)
    categorical: Optional[bool] = Field(None)
    multivalued: Optional[bool] = Field(None)
    value_options: Optional[List[ObservablePropertyValueOption]] = Field(default_factory=list)
    value_metadata: Optional[List[ObservablePropertyMetadataElement]] = Field(default_factory=list)
    quantity_kind: Optional[QudtQuantityKind] = Field(None)
    default_unit: Optional[str] = Field(None)
    default_significantdecimals: Optional[int] = Field(None)
    default_immutable: Optional[bool] = Field(None)
    groups: Optional[List[str]] = Field(default_factory=list)
    relevant_observable_entity_types: Optional[List[ObservableEntityType]] = Field(default_factory=list)
    relevant_observation_types: Optional[List[ObservationType]] = Field(default_factory=list)
    indicator: Optional[str] = Field(None)
    calculation_design: Optional[CalculationDesign] = Field(None)
    validation_design: Optional[ValidationDesign] = Field(None)
    translations: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class ObservablePropertyValueOption(HasContextAliases):
    
    key: Optional[str] = Field(None)
    value: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    
        

class ObservablePropertyMetadataElement(ConfiguredBaseModel):
    
    field: Optional[str] = Field(None)
    value: Optional[str] = Field(None)
    
        

class ObservablePropertyMetadataField(NamedThing):
    
    value_type: Optional[str] = Field(None)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class CalculationDesign(ConfiguredBaseModel):
    
    unit: Optional[str] = Field(None)
    formula: Optional[str] = Field(None)
    
        

class ValidationDesign(ConfiguredBaseModel):
    
    conditional: Optional[str] = Field(None)
    
        

class Contact(HasContextAliases):
    
    name: Optional[str] = Field(None)
    orcid: Optional[str] = Field(None)
    contact_roles: Optional[List[ContactRole]] = Field(default_factory=list)
    contact_email: Optional[str] = Field(None)
    contact_phone: Optional[str] = Field(None)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    
        

class Stakeholder(HasTranslations, NamedThing):
    
    rorid: Optional[str] = Field(None)
    geographic_scope: Optional[str] = Field(None)
    translations: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class ProjectStakeholder(HasTranslations):
    
    stakeholder: Optional[str] = Field(None)
    project_roles: Optional[List[ProjectRole]] = Field(default_factory=list)
    contacts: Optional[List[Contact]] = Field(default_factory=list)
    translations: Optional[List[Translation]] = Field(default_factory=list)
    
        

class StudyEntity(HasContextAliases, NamedThing):
    
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class Project(StudyEntity, HasTranslations, HasContextAliases):
    
    default_language: Optional[str] = Field(None)
    project_stakeholders: Optional[List[ProjectStakeholder]] = Field(default_factory=list)
    start_date: Optional[date] = Field(None)
    end_date: Optional[date] = Field(None)
    study_id_list: Optional[List[str]] = Field(default_factory=list)
    translations: Optional[List[Translation]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class StudyEntityLink(ConfiguredBaseModel):
    
    linktype: Optional[LinkType] = Field(None)
    study_entity: Optional[str] = Field(None)
    
        

class Study(StudyEntity, HasTranslations):
    
    default_language: Optional[str] = Field(None)
    study_stakeholders: Optional[List[StudyStakeholder]] = Field(default_factory=list)
    start_date: Optional[date] = Field(None)
    end_date: Optional[date] = Field(None)
    timepoint_id_list: Optional[List[str]] = Field(default_factory=list)
    study_entities: Optional[List[str]] = Field(default_factory=list)
    project_id_list: Optional[List[str]] = Field(default_factory=list)
    translations: Optional[List[Translation]] = Field(default_factory=list)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class StudyStakeholder(ConfiguredBaseModel):
    
    stakeholder: Optional[str] = Field(None)
    study_roles: Optional[List[StudyRole]] = Field(default_factory=list)
    contacts: Optional[List[Contact]] = Field(default_factory=list)
    
        

class Timepoint(StudyEntity):
    
    sort_order: Optional[Decimal] = Field(None)
    start_date: Optional[date] = Field(None)
    end_date: Optional[date] = Field(None)
    observations: Optional[List[Observation]] = Field(default_factory=list)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class StudyPopulation(StudyEntity):
    
    research_population_type: Optional[ResearchPopulationType] = Field(None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class SampleCollection(StudyEntity):
    
    matrix: Optional[str] = Field(None)
    constraints: Optional[List[str]] = Field(default_factory=list)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class Sample(StudyEntity):
    
    matrix: Optional[str] = Field(None)
    constraints: Optional[List[str]] = Field(default_factory=list)
    sampled_in_project: Optional[str] = Field(None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class StudySubject(StudyEntity):
    
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class Person(StudyEntity):
    
    recruited_in_project: Optional[str] = Field(None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class PersonGroup(StudyEntity):
    
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class Geolocation(StudyEntity):
    
    location: Optional[str] = Field(None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class Environment(StudyEntity):
    
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    context_aliases: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class Observation(NamedThing):
    
    observation_type: Optional[ObservationType] = Field(None)
    observation_design: Optional[ObservationDesign] = Field(None)
    observation_result: Optional[ObservationResult] = Field(None)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class MetadataObservation(Observation):
    
    observation_type: Optional[ObservationType] = Field(None)
    observation_design: Optional[ObservationDesign] = Field(None)
    observation_result: Optional[ObservationResult] = Field(None)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class QuestionnaireObservation(Observation):
    
    observation_type: Optional[ObservationType] = Field(None)
    observation_design: Optional[ObservationDesign] = Field(None)
    observation_result: Optional[ObservationResult] = Field(None)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class SamplingObservation(Observation):
    
    observation_type: Optional[ObservationType] = Field(None)
    observation_design: Optional[ObservationDesign] = Field(None)
    observation_result: Optional[ObservationResult] = Field(None)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class GeospatialObservation(Observation):
    
    observation_type: Optional[ObservationType] = Field(None)
    observation_design: Optional[ObservationDesign] = Field(None)
    observation_result: Optional[ObservationResult] = Field(None)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class ObservationDesign(ConfiguredBaseModel):
    
    observation_sets: Optional[List[ObservationSet]] = Field(default_factory=list)
    
        

class MetadataDesign(ObservationDesign):
    
    observation_sets: Optional[List[ObservationSet]] = Field(default_factory=list)
    
        

class QuestionnaireDesign(ObservationDesign):
    
    observation_sets: Optional[List[ObservationSet]] = Field(default_factory=list)
    
        

class SamplingDesign(ObservationDesign):
    
    observation_sets: Optional[List[ObservationSet]] = Field(default_factory=list)
    
        

class GeospatialDesign(ObservationDesign):
    
    observation_sets: Optional[List[ObservationSet]] = Field(default_factory=list)
    
        

class ObservationSet(ConfiguredBaseModel):
    
    observable_entity_type: Optional[ObservableEntityType] = Field(None)
    observable_entity_id_list: Optional[List[str]] = Field(default_factory=list)
    observable_property_id_list: Optional[List[str]] = Field(default_factory=list)
    
        

class ObservationResult(ConfiguredBaseModel):
    
    observed_values: Optional[List[ObservedValue]] = Field(default_factory=list)
    
        

class MetadataResult(ObservationResult):
    
    observed_values: Optional[List[ObservedValue]] = Field(default_factory=list)
    
        

class QuestionnaireResult(ObservationResult):
    
    observed_values: Optional[List[ObservedValue]] = Field(default_factory=list)
    
        

class SamplingResult(ObservationResult):
    
    observed_values: Optional[List[ObservedValue]] = Field(default_factory=list)
    
        

class GeospatialResult(ObservationResult):
    
    observed_values: Optional[List[ObservedValue]] = Field(default_factory=list)
    
        

class ObservedValue(ConfiguredBaseModel):
    
    observable_entity: Optional[str] = Field(None)
    observable_property: Optional[str] = Field(None)
    value: Optional[str] = Field(None)
    unit: Optional[str] = Field(None)
    quality_or_confidence_info: Optional[str] = Field(None)
    provenance_info: Optional[str] = Field(None)
    
        

class DataRequest(NamedThing):
    
    contacts: Optional[List[Contact]] = Field(default_factory=list)
    request_properties: Optional[str] = Field(None)
    data_stakeholders: Optional[List[str]] = Field(default_factory=list)
    research_objectives: Optional[List[str]] = Field(default_factory=list)
    processing_actions: Optional[List[str]] = Field(default_factory=list)
    processing_steps: Optional[List[str]] = Field(default_factory=list)
    remark_on_content: Optional[str] = Field(None)
    remark_on_methodology: Optional[str] = Field(None)
    observed_entity_properties: Optional[List[ObservedEntityProperty]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class ObservedEntityProperty(ConfiguredBaseModel):
    
    observable_entity: Optional[str] = Field(None)
    observable_property: Optional[str] = Field(None)
    
        

class DataStakeholder(NamedThing):
    
    stakeholder: Optional[str] = Field(None)
    data_roles: Optional[List[DataRole]] = Field(default_factory=list)
    contacts: Optional[List[Contact]] = Field(default_factory=list)
    processing_description: Optional[str] = Field(None)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class ResearchObjective(NamedThing):
    
    objective_type: Optional[ObjectiveType] = Field(None)
    authors: Optional[List[str]] = Field(default_factory=list)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class ProcessingAction(NamedThing):
    
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class ProcessingStep(NamedThing):
    
    start_date: Optional[date] = Field(None)
    delivery_date: Optional[date] = Field(None)
    id: str = Field(...)
    unique_name: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    remark: Optional[str] = Field(None)
    
        

class DataExtract(ConfiguredBaseModel):
    
    observed_values: Optional[List[ObservedValue]] = Field(default_factory=list)
    
        


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
Translation.model_rebuild()
Unit.model_rebuild()
BioChemGrouping.model_rebuild()
BioChemEntity.model_rebuild()
BioChemIdentifier.model_rebuild()
BioChemIdentifierSchema.model_rebuild()
Matrix.model_rebuild()
Indicator.model_rebuild()
BioChemEntityLink.model_rebuild()
ObservablePropertyGroup.model_rebuild()
ObservableProperty.model_rebuild()
ObservablePropertyValueOption.model_rebuild()
ObservablePropertyMetadataElement.model_rebuild()
ObservablePropertyMetadataField.model_rebuild()
CalculationDesign.model_rebuild()
ValidationDesign.model_rebuild()
Contact.model_rebuild()
Stakeholder.model_rebuild()
ProjectStakeholder.model_rebuild()
StudyEntity.model_rebuild()
Project.model_rebuild()
StudyEntityLink.model_rebuild()
Study.model_rebuild()
StudyStakeholder.model_rebuild()
Timepoint.model_rebuild()
StudyPopulation.model_rebuild()
SampleCollection.model_rebuild()
Sample.model_rebuild()
StudySubject.model_rebuild()
Person.model_rebuild()
PersonGroup.model_rebuild()
Geolocation.model_rebuild()
Environment.model_rebuild()
Observation.model_rebuild()
MetadataObservation.model_rebuild()
QuestionnaireObservation.model_rebuild()
SamplingObservation.model_rebuild()
GeospatialObservation.model_rebuild()
ObservationDesign.model_rebuild()
MetadataDesign.model_rebuild()
QuestionnaireDesign.model_rebuild()
SamplingDesign.model_rebuild()
GeospatialDesign.model_rebuild()
ObservationSet.model_rebuild()
ObservationResult.model_rebuild()
MetadataResult.model_rebuild()
QuestionnaireResult.model_rebuild()
SamplingResult.model_rebuild()
GeospatialResult.model_rebuild()
ObservedValue.model_rebuild()
DataRequest.model_rebuild()
ObservedEntityProperty.model_rebuild()
DataStakeholder.model_rebuild()
ResearchObjective.model_rebuild()
ProcessingAction.model_rebuild()
ProcessingStep.model_rebuild()
DataExtract.model_rebuild()

