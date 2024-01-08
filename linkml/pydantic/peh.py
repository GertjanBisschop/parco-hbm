from __future__ import annotations
from datetime import datetime, date
from enum import Enum
from typing import List, Dict, Optional, Any, Union
from decimal import Decimal
from pydantic import BaseModel as BaseModel, ConfigDict, Field
import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


metamodel_version = "None"
version = "None"

class WeakRefShimBaseModel(BaseModel):
   __slots__ = '__weakref__'

class ConfiguredBaseModel(WeakRefShimBaseModel,
                validate_assignment = True,
                validate_all = True,
                underscore_attrs_are_private = True,
                extra = 'forbid',
                arbitrary_types_allowed = True,
                use_enum_values = True):
    pass


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
    
    

class ProjectRole(str, Enum):
    
    
    subsidising_party = "subsidising_party"
    
    principal_investigator = "principal_investigator"
    
    data_controller = "data_controller"
    
    data_processor = "data_processor"
    
    data_user = "data_user"
    
    

class StudyRole(str, Enum):
    
    
    subsidising_party = "subsidising_party"
    
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
    
    matrices_as_list: Optional[List[Matrix]] = Field(default_factory=list)
    metadata_fields_as_list: Optional[List[ObservablePropertyMetadataField]] = Field(default_factory=list)
    biochementities_as_list: Optional[List[BioChemEntity]] = Field(default_factory=list)
    biochemgroupings_as_list: Optional[List[BioChemGrouping]] = Field(default_factory=list)
    indicators_as_list: Optional[List[Indicator]] = Field(default_factory=list)
    units_as_list: Optional[List[Unit]] = Field(default_factory=list)
    observablepropertygroups_as_list: Optional[List[ObservablePropertyGroup]] = Field(default_factory=list)
    observableproperties_as_list: Optional[List[ObservableProperty]] = Field(default_factory=list)
    stakeholders_as_list: Optional[List[Stakeholder]] = Field(default_factory=list)
    projects_as_list: Optional[List[Project]] = Field(default_factory=list)
    studies_as_list: Optional[List[Study]] = Field(default_factory=list)
    timepoints_as_list: Optional[List[Timepoint]] = Field(default_factory=list)
    

class NamedThing(ConfiguredBaseModel):
    """
    A generic grouping for any identifiable entity
    """
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class HasValidationStatus(ConfiguredBaseModel):
    
    current_validation_status: Optional[ValidationStatus] = Field(None)
    validation_history: Optional[List[ValidationHistoryRecord]] = Field(default_factory=list)
    

class ValidationHistoryRecord(ConfiguredBaseModel):
    
    validation_datetime: Optional[datetime ] = Field(None)
    validation_status: Optional[ValidationStatus] = Field(None)
    validation_actor: Optional[str] = Field(None)
    validation_remark: Optional[str] = Field(None)
    

class HasAliases(ConfiguredBaseModel):
    
    aliases_as_list: Optional[List[str]] = Field(default_factory=list)
    

class HasContextAliases(ConfiguredBaseModel):
    
    context_aliases_as_list: Optional[List[ContextAlias]] = Field(default_factory=list)
    

class ContextAlias(ConfiguredBaseModel):
    
    context: Optional[str] = Field(None)
    alias: Optional[str] = Field(None)
    

class HasTranslations(ConfiguredBaseModel):
    
    translations_as_list: Optional[List[Translation]] = Field(default_factory=list)
    

class Translation(ConfiguredBaseModel):
    
    property_name: Optional[str] = Field(None)
    language: Optional[str] = Field(None)
    translated_value: Optional[str] = Field(None)
    

class Unit(HasTranslations, HasContextAliases, NamedThing):
    
    same_unit_as: Optional[QudtUnit] = Field(None)
    quantity_kind: Optional[QudtQuantityKind] = Field(None)
    context_aliases_as_list: Optional[List[ContextAlias]] = Field(default_factory=list)
    translations_as_list: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class BioChemGrouping(HasTranslations, HasContextAliases, NamedThing):
    
    context_aliases_as_list: Optional[List[ContextAlias]] = Field(default_factory=list)
    translations_as_list: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class BioChemEntity(HasTranslations, HasContextAliases, HasAliases, HasValidationStatus, NamedThing):
    """
    A biological, chemical or biochemical entity that is relevant to the Personal Exposure and Health domain
    """
    grouping: Optional[str] = Field(None)
    biochemidentifiers_as_list: Optional[List[BioChemIdentifier]] = Field(default_factory=list)
    aliases_as_list: Optional[List[str]] = Field(default_factory=list)
    context_aliases_as_list: Optional[List[ContextAlias]] = Field(default_factory=list)
    translations_as_list: Optional[List[Translation]] = Field(default_factory=list)
    current_validation_status: Optional[ValidationStatus] = Field(None)
    validation_history: Optional[List[ValidationHistoryRecord]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class BioChemIdentifier(HasValidationStatus):
    
    identifier_schema: Optional[str] = Field(None)
    identifier_code: Optional[str] = Field(None)
    current_validation_status: Optional[ValidationStatus] = Field(None)
    validation_history: Optional[List[ValidationHistoryRecord]] = Field(default_factory=list)
    

class BioChemIdentifierSchema(NamedThing):
    
    web_uri: Optional[str] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class Matrix(HasContextAliases, NamedThing):
    
    sort_order: Optional[Decimal] = Field(None)
    aggregation_target: Optional[bool] = Field(None)
    parent_matrix: Optional[str] = Field(None)
    context_aliases_as_list: Optional[List[ContextAlias]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class Indicator(NamedThing):
    """
    A measurable indicator that is relevant to the Personal Exposure and Health domain
    """
    indicator_type: Optional[IndicatorType] = Field(None)
    quantity_kind: Optional[QudtQuantityKind] = Field(None)
    matrix: Optional[str] = Field(None)
    constraints: Optional[List[str]] = Field(default_factory=list)
    relevant_observable_entity_types: Optional[List[ObservableEntityType]] = Field(default_factory=list)
    biochementity_links_as_list: Optional[List[BioChemEntityLink]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class BioChemEntityLink(ConfiguredBaseModel):
    
    biochementity_linktype: Optional[BioChemEntityLinkType] = Field(None)
    biochementity: Optional[str] = Field(None)
    

class ObservablePropertyGroup(HasTranslations, NamedThing):
    
    sort_order: Optional[Decimal] = Field(None)
    is_abstract: Optional[bool] = Field(None)
    parent_groups: Optional[List[str]] = Field(default_factory=list)
    translations_as_list: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class ObservableProperty(HasTranslations, NamedThing):
    
    value_type: Optional[str] = Field(None)
    categorical: Optional[bool] = Field(None)
    multivalued: Optional[bool] = Field(None)
    value_options_as_list: Optional[List[ObservablePropertyValueOption]] = Field(default_factory=list)
    value_metadata_as_list: Optional[List[ObservablePropertyMetadataElement]] = Field(default_factory=list)
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
    translations_as_list: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class ObservablePropertyValueOption(HasContextAliases):
    
    key: Optional[str] = Field(None)
    value: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    context_aliases_as_list: Optional[List[ContextAlias]] = Field(default_factory=list)
    

class ObservablePropertyMetadataElement(ConfiguredBaseModel):
    
    field: Optional[str] = Field(None)
    value: Optional[str] = Field(None)
    

class ObservablePropertyMetadataField(NamedThing):
    
    value_type: Optional[str] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class CalculationDesign(ConfiguredBaseModel):
    
    unit: Optional[str] = Field(None)
    formula: Optional[str] = Field(None)
    

class ValidationDesign(ConfiguredBaseModel):
    
    conditional: Optional[str] = Field(None)
    

class Stakeholder(HasTranslations, NamedThing):
    
    geographic_scope: Optional[str] = Field(None)
    translations_as_list: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class Project(HasTranslations, NamedThing):
    
    project_stakeholders_as_list: Optional[List[ProjectStakeholder]] = Field(default_factory=list)
    studies: Optional[List[str]] = Field(default_factory=list)
    translations_as_list: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class ProjectStakeholder(HasTranslations):
    
    stakeholder: Optional[str] = Field(None)
    project_roles: Optional[List[ProjectRole]] = Field(default_factory=list)
    translations_as_list: Optional[List[Translation]] = Field(default_factory=list)
    

class Study(HasTranslations, NamedThing):
    
    study_stakeholders_as_list: Optional[List[StudyStakeholder]] = Field(default_factory=list)
    timepoints: Optional[List[str]] = Field(default_factory=list)
    study_entities: Optional[List[str]] = Field(default_factory=list)
    projects: Optional[List[str]] = Field(default_factory=list)
    translations_as_list: Optional[List[Translation]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class StudyStakeholder(ConfiguredBaseModel):
    
    stakeholder: Optional[str] = Field(None)
    study_roles: Optional[List[StudyRole]] = Field(default_factory=list)
    

class Timepoint(NamedThing):
    
    observations_as_list: Optional[List[Observation]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class StudyEntity(NamedThing):
    
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class StudyEntityLink(ConfiguredBaseModel):
    
    linktype: Optional[LinkType] = Field(None)
    study_entity: Optional[str] = Field(None)
    

class Sample(StudyEntity):
    
    matrix: Optional[str] = Field(None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class StudySubject(StudyEntity):
    
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class Person(StudyEntity):
    
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class PersonGroup(StudyEntity):
    
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class Geolocation(StudyEntity):
    
    location: Optional[str] = Field(None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class Environment(StudyEntity):
    
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class Observation(NamedThing):
    
    observation_type: Optional[ObservationType] = Field(None)
    observation_design: Optional[ObservationDesign] = Field(None)
    observation_result: Optional[ObservationResult] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class MetadataObservation(Observation):
    
    observation_type: Optional[ObservationType] = Field(None)
    observation_design: Optional[ObservationDesign] = Field(None)
    observation_result: Optional[ObservationResult] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class QuestionnaireObservation(Observation):
    
    observation_type: Optional[ObservationType] = Field(None)
    observation_design: Optional[ObservationDesign] = Field(None)
    observation_result: Optional[ObservationResult] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class SamplingObservation(Observation):
    
    observation_type: Optional[ObservationType] = Field(None)
    observation_design: Optional[ObservationDesign] = Field(None)
    observation_result: Optional[ObservationResult] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class GeospatialObservation(Observation):
    
    observation_type: Optional[ObservationType] = Field(None)
    observation_design: Optional[ObservationDesign] = Field(None)
    observation_result: Optional[ObservationResult] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class ObservationDesign(ConfiguredBaseModel):
    
    observation_entities: Optional[List[str]] = Field(default_factory=list)
    observation_properties: Optional[List[str]] = Field(default_factory=list)
    

class ObservationEntity(NamedThing):
    
    study_entity: Optional[str] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class ObservationProperty(NamedThing):
    
    observable_property: Optional[str] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class ObservationResult(ConfiguredBaseModel):
    
    observed_values: Optional[List[ObservedValue]] = Field(default_factory=list)
    

class ObservedValue(ConfiguredBaseModel):
    
    observed_entity: Optional[str] = Field(None)
    observable_property: Optional[str] = Field(None)
    value: Optional[str] = Field(None)
    unit: Optional[str] = Field(None)
    quality_or_confidence_info: Optional[str] = Field(None)
    provenance_info: Optional[str] = Field(None)
    

class DataRequest(NamedThing):
    
    contact_name: Optional[str] = Field(None)
    contact_email: Optional[str] = Field(None)
    contact_phone: Optional[str] = Field(None)
    request_properties: Optional[str] = Field(None)
    data_stakeholders: Optional[List[str]] = Field(default_factory=list)
    research_objectives: Optional[List[str]] = Field(default_factory=list)
    processing_actions: Optional[List[str]] = Field(default_factory=list)
    processing_steps: Optional[List[str]] = Field(default_factory=list)
    remarks_on_content: Optional[List[str]] = Field(default_factory=list)
    remarks_on_methodology: Optional[List[str]] = Field(default_factory=list)
    observed_entity_properties: Optional[List[ObservedEntityProperty]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class ObservedEntityProperty(ConfiguredBaseModel):
    
    observed_entity: Optional[str] = Field(None)
    observable_property: Optional[str] = Field(None)
    

class DataStakeholder(NamedThing):
    
    stakeholder: Optional[str] = Field(None)
    data_roles: Optional[List[DataRole]] = Field(default_factory=list)
    processing_description: Optional[str] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class ResearchObjective(NamedThing):
    
    objective_type: Optional[ObjectiveType] = Field(None)
    authors: Optional[List[str]] = Field(default_factory=list)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class ProcessingAction(NamedThing):
    
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class ProcessingStep(NamedThing):
    
    start_date: Optional[str] = Field(None)
    delivery_date: Optional[str] = Field(None)
    id: str = Field(...)
    shortname: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    label: Optional[str] = Field(None)
    

class DataExtract(ConfiguredBaseModel):
    
    observed_values: Optional[List[ObservedValue]] = Field(default_factory=list)
    


# Update forward refs
# see https://pydantic-docs.helpmanual.io/usage/postponed_annotations/
EntityList.update_forward_refs()
NamedThing.update_forward_refs()
HasValidationStatus.update_forward_refs()
ValidationHistoryRecord.update_forward_refs()
HasAliases.update_forward_refs()
HasContextAliases.update_forward_refs()
ContextAlias.update_forward_refs()
HasTranslations.update_forward_refs()
Translation.update_forward_refs()
Unit.update_forward_refs()
BioChemGrouping.update_forward_refs()
BioChemEntity.update_forward_refs()
BioChemIdentifier.update_forward_refs()
BioChemIdentifierSchema.update_forward_refs()
Matrix.update_forward_refs()
Indicator.update_forward_refs()
BioChemEntityLink.update_forward_refs()
ObservablePropertyGroup.update_forward_refs()
ObservableProperty.update_forward_refs()
ObservablePropertyValueOption.update_forward_refs()
ObservablePropertyMetadataElement.update_forward_refs()
ObservablePropertyMetadataField.update_forward_refs()
CalculationDesign.update_forward_refs()
ValidationDesign.update_forward_refs()
Stakeholder.update_forward_refs()
Project.update_forward_refs()
ProjectStakeholder.update_forward_refs()
Study.update_forward_refs()
StudyStakeholder.update_forward_refs()
Timepoint.update_forward_refs()
StudyEntity.update_forward_refs()
StudyEntityLink.update_forward_refs()
Sample.update_forward_refs()
StudySubject.update_forward_refs()
Person.update_forward_refs()
PersonGroup.update_forward_refs()
Geolocation.update_forward_refs()
Environment.update_forward_refs()
Observation.update_forward_refs()
MetadataObservation.update_forward_refs()
QuestionnaireObservation.update_forward_refs()
SamplingObservation.update_forward_refs()
GeospatialObservation.update_forward_refs()
ObservationDesign.update_forward_refs()
ObservationEntity.update_forward_refs()
ObservationProperty.update_forward_refs()
ObservationResult.update_forward_refs()
ObservedValue.update_forward_refs()
DataRequest.update_forward_refs()
ObservedEntityProperty.update_forward_refs()
DataStakeholder.update_forward_refs()
ResearchObjective.update_forward_refs()
ProcessingAction.update_forward_refs()
ProcessingStep.update_forward_refs()
DataExtract.update_forward_refs()

