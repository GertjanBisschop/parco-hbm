from __future__ import annotations 

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal 
from enum import Enum 
from typing import (
    Any,
    ClassVar,
    Dict,
    List,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    field_validator
)


metamodel_version = "None"
version = "0.0.1a"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )
    pass




class LinkMLMeta(RootModel):
    root: Dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
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
    and = "and"
    or = "or"


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


class BioChemEntityLinkType(str, Enum):
    exact_match = "exact_match"
    close_match = "close_match"
    broader = "broader"
    part_of = "part_of"
    group_contains = "group_contains"
    has_parent_compound = "has_parent_compound"
    branched_version_of = "branched_version_of"


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


class QudtUnit(str, Enum):
    PERCENT = "PERCENT"
    KiloGM_PER_M3 = "KiloGM-PER-M3"
    DAY = "DAY"
    NanoGM = "NanoGM"
    GM = "GM"
    MilliGM_PER_KiloGM = "MilliGM-PER-KiloGM"
    MilliMOL_PER_MOL = "MilliMOL-PER-MOL"
    MicroGM_PER_MilliL = "MicroGM-PER-MilliL"
    MO = "MO"
    UNITLESS = "UNITLESS"
    NanoMOL_PER_L = "NanoMOL-PER-L"
    MIN = "MIN"
    NanoGM_PER_M3 = "NanoGM-PER-M3"
    GM_PER_DeciL = "GM-PER-DeciL"
    GM_PER_L = "GM-PER-L"
    MilliL = "MilliL"
    HR = "HR"
    PicoGM = "PicoGM"
    FemtoMOL_PER_KiloGM = "FemtoMOL-PER-KiloGM"
    NUM = "NUM"
    NanoGM_PER_MilliL = "NanoGM-PER-MilliL"
    MicroGM_PER_KiloGM = "MicroGM-PER-KiloGM"
    KiloGM = "KiloGM"
    NanoGM_PER_L = "NanoGM-PER-L"
    MicroMOL_PER_L = "MicroMOL-PER-L"
    CentiM = "CentiM"
    MicroGM_PER_GM = "MicroGM-PER-GM"
    WK = "WK"
    NanoGM_PER_DeciL = "NanoGM-PER-DeciL"
    MilliGM_PER_L = "MilliGM-PER-L"
    PicoGM_PER_GM = "PicoGM-PER-GM"
    L = "L"
    NanoGM_PER_M2 = "NanoGM-PER-M2"
    IU_PER_L = "IU-PER-L"
    NUM_PER_MilliL = "NUM-PER-MilliL"
    GM_PER_MOL = "GM-PER-MOL"
    PER_WK = "PER-WK"
    PicoGM_PER_MilliL = "PicoGM-PER-MilliL"
    YR = "YR"
    PER_DAY = "PER-DAY"
    PicoGM_PER_MilliGM = "PicoGM-PER-MilliGM"
    MicroGM_PER_L = "MicroGM-PER-L"
    KiloGM_PER_M2 = "KiloGM-PER-M2"
    MilliGM_PER_DeciL = "MilliGM-PER-DeciL"


class QudtQuantityKind(str, Enum):
    AmountOfSubstanceConcentration = "AmountOfSubstanceConcentration"
    AmountOfSubstancePerMass = "AmountOfSubstancePerMass"
    Count = "Count"
    Dimensionless = "Dimensionless"
    DimensionlessRatio = "DimensionlessRatio"
    Time = "Time"
    Frequency = "Frequency"
    Length = "Length"
    Mass = "Mass"
    MassPerArea = "MassPerArea"
    MassConcentration = "MassConcentration"
    MassRatio = "MassRatio"
    MolarMass = "MolarMass"
    MolarRatio = "MolarRatio"
    NumberDensity = "NumberDensity"
    Volume = "Volume"



class EntityList(ConfiguredBaseModel):
    matrices: Optional[List[Matrix]] = Field(default=None)
    metadata_fields: Optional[List[ObservablePropertyMetadataField]] = Field(default=None)
    biochementities: Optional[List[BioChemEntity]] = Field(default=None)
    groupings: Optional[List[Grouping]] = Field(default=None)
    indicators: Optional[List[Indicator]] = Field(default=None)
    units: Optional[List[Unit]] = Field(default=None)
    observable_properties: Optional[List[ObservableProperty]] = Field(default=None)
    stakeholders: Optional[List[Stakeholder]] = Field(default=None)
    projects: Optional[List[Project]] = Field(default=None)
    studies: Optional[List[Study]] = Field(default=None)
    study_entities: Optional[List[StudyEntity]] = Field(default=None)
    physical_entities: Optional[List[PhysicalEntity]] = Field(default=None)
    observation_groups: Optional[List[ObservationGroup]] = Field(default=None)
    observations: Optional[List[Observation]] = Field(default=None)
    observation_results: Optional[List[ObservationResult]] = Field(default=None)
    observed_values: Optional[List[ObservedValue]] = Field(default=None)
    layouts: Optional[List[DataLayout]] = Field(default=None)
    data_requests: Optional[List[DataRequest]] = Field(default=None)


class NamedThing(ConfiguredBaseModel):
    """
    A generic grouping for any identifiable entity
    """
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class HasValidationStatus(ConfiguredBaseModel):
    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[List[ValidationHistoryRecord]] = Field(default=None)


class ValidationHistoryRecord(ConfiguredBaseModel):
    validation_datetime: Optional[datetime ] = Field(default=None)
    validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_actor: Optional[str] = Field(default=None)
    validation_institute: Optional[str] = Field(default=None)
    validation_remark: Optional[str] = Field(default=None)


class HasAliases(ConfiguredBaseModel):
    aliases: Optional[List[str]] = Field(default=None)


class HasContextAliases(ConfiguredBaseModel):
    context_aliases: Optional[List[ContextAlias]] = Field(default=None)


class ContextAlias(ConfiguredBaseModel):
    property_name: Optional[str] = Field(default=None)
    context: Optional[str] = Field(default=None)
    alias: Optional[str] = Field(default=None)


class HasTranslations(ConfiguredBaseModel):
    translations: Optional[List[Translation]] = Field(default=None)


class Grouping(HasTranslations, HasContextAliases, NamedThing):
    sort_order: Optional[Decimal] = Field(default=None)
    abstract: Optional[bool] = Field(default=None)
    parent_grouping_id_list: Optional[List[str]] = Field(default=None)
    context_aliases: Optional[List[ContextAlias]] = Field(default=None)
    translations: Optional[List[Translation]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Translation(ConfiguredBaseModel):
    property_name: Optional[str] = Field(default=None)
    language: Optional[str] = Field(default=None)
    translated_value: Optional[str] = Field(default=None)


class Unit(HasTranslations, HasContextAliases, HasValidationStatus, NamedThing):
    same_unit_as: Optional[QudtUnit] = Field(default=None)
    quantity_kind: Optional[QudtQuantityKind] = Field(default=None)
    context_aliases: Optional[List[ContextAlias]] = Field(default=None)
    translations: Optional[List[Translation]] = Field(default=None)
    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[List[ValidationHistoryRecord]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class BioChemEntity(HasTranslations, HasContextAliases, HasAliases, HasValidationStatus, NamedThing):
    """
    A biological, chemical or biochemical entity that is relevant to the Personal Exposure and Health domain
    """
    grouping_id_list: Optional[List[str]] = Field(default=None)
    molweight_grampermol: Optional[Decimal] = Field(default=None)
    biochemidentifiers: Optional[List[BioChemIdentifier]] = Field(default=None)
    biochementity_links: Optional[List[BioChemEntityLink]] = Field(default=None)
    aliases: Optional[List[str]] = Field(default=None)
    context_aliases: Optional[List[ContextAlias]] = Field(default=None)
    translations: Optional[List[Translation]] = Field(default=None)
    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[List[ValidationHistoryRecord]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class BioChemIdentifier(HasValidationStatus):
    identifier_schema: Optional[str] = Field(default=None)
    identifier_code: Optional[str] = Field(default=None)
    current_validation_status: Optional[ValidationStatus] = Field(default=None)
    validation_history: Optional[List[ValidationHistoryRecord]] = Field(default=None)


class BioChemIdentifierSchema(NamedThing):
    web_uri: Optional[str] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Matrix(HasTranslations, HasContextAliases, NamedThing):
    sort_order: Optional[Decimal] = Field(default=None)
    aggregation_target: Optional[bool] = Field(default=None)
    parent_matrix: Optional[str] = Field(default=None)
    secondary_parent_matrix_id_list: Optional[List[str]] = Field(default=None)
    context_aliases: Optional[List[ContextAlias]] = Field(default=None)
    translations: Optional[List[Translation]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Indicator(NamedThing):
    """
    A measurable indicator that is relevant to the Personal Exposure and Health domain
    """
    indicator_type: Optional[IndicatorType] = Field(default=None)
    varname: Optional[str] = Field(default=None)
    property: Optional[str] = Field(default=None)
    quantity_kind: Optional[QudtQuantityKind] = Field(default=None)
    matrix: Optional[str] = Field(default=None)
    constraints: Optional[List[str]] = Field(default=None)
    grouping_id_list: Optional[List[str]] = Field(default=None)
    relevant_observable_entity_types: Optional[List[ObservableEntityType]] = Field(default=None)
    biochementity_links: Optional[List[BioChemEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class BioChemEntityLink(ConfiguredBaseModel):
    biochementity_linktype: Optional[BioChemEntityLinkType] = Field(default=None)
    biochementity: Optional[str] = Field(default=None)


class PhysicalEntity(NamedThing):
    physical_entity_links: Optional[List[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class PhysicalEntityLink(ConfiguredBaseModel):
    linktype: Optional[LinkType] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)


class Sample(PhysicalEntity):
    matrix: Optional[str] = Field(default=None)
    constraints: Optional[List[str]] = Field(default=None)
    sampled_in_project: Optional[str] = Field(default=None)
    physical_label: Optional[str] = Field(default=None)
    collection_date: Optional[date] = Field(default=None)
    physical_entity_links: Optional[List[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Person(PhysicalEntity):
    recruited_in_project: Optional[str] = Field(default=None)
    physical_entity_links: Optional[List[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Geolocation(PhysicalEntity):
    location: Optional[str] = Field(default=None)
    physical_entity_links: Optional[List[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Environment(PhysicalEntity):
    physical_entity_links: Optional[List[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class HomeEnvironment(Environment):
    physical_entity_links: Optional[List[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class WorkEnvironment(Environment):
    physical_entity_links: Optional[List[PhysicalEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ObservableProperty(HasTranslations, NamedThing):
    value_type: Optional[str] = Field(default=None)
    categorical: Optional[bool] = Field(default=None)
    multivalued: Optional[bool] = Field(default=None)
    value_options: Optional[List[ObservablePropertyValueOption]] = Field(default=None)
    value_metadata: Optional[List[ObservablePropertyMetadataElement]] = Field(default=None)
    quantity_kind: Optional[QudtQuantityKind] = Field(default=None)
    default_unit: Optional[str] = Field(default=None)
    default_unit_label: Optional[str] = Field(default=None)
    default_required: Optional[bool] = Field(default=None)
    default_zeroallowed: Optional[bool] = Field(default=None)
    default_significantdecimals: Optional[int] = Field(default=None)
    default_immutable: Optional[bool] = Field(default=None)
    grouping_id_list: Optional[List[str]] = Field(default=None)
    default_observation_result_type: Optional[ObservationResultType] = Field(default=None)
    relevant_observable_entity_types: Optional[List[ObservableEntityType]] = Field(default=None)
    relevant_observation_types: Optional[List[ObservationType]] = Field(default=None)
    indicator: Optional[str] = Field(default=None)
    varname: Optional[str] = Field(default=None)
    calculation_designs: Optional[List[CalculationDesign]] = Field(default=None)
    validation_designs: Optional[List[ValidationDesign]] = Field(default=None)
    translations: Optional[List[Translation]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ObservablePropertyValueOption(HasContextAliases):
    key: Optional[str] = Field(default=None)
    value: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    context_aliases: Optional[List[ContextAlias]] = Field(default=None)


class ObservablePropertyMetadataElement(ConfiguredBaseModel):
    field: Optional[str] = Field(default=None)
    value: Optional[str] = Field(default=None)


class ObservablePropertyMetadataField(NamedThing):
    value_type: Optional[str] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class CalculationDesign(ConfiguredBaseModel):
    calculation_name: Optional[str] = Field(default=None)
    calculation_implementation_as_json: Optional[str] = Field(default=None)
    calculation_implementation: Optional[CalculationImplementation] = Field(default=None)
    conditional: Optional[str] = Field(default=None)


class CalculationImplementation(ConfiguredBaseModel):
    function_name: Optional[str] = Field(default=None)
    function_args: Optional[List[CalculationArgument]] = Field(default=None)
    function_kwargs: Optional[List[CalculationKeywordArgument]] = Field(default=None)
    function_results: Optional[List[CalculationResult]] = Field(default=None)


class CalculationArgument(ConfiguredBaseModel):
    source_path: Optional[str] = Field(default=None)
    varname: Optional[str] = Field(default=None)
    process_state: Optional[str] = Field(default=None)
    imputation_state: Optional[str] = Field(default=None)
    value_type: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)


class CalculationKeywordArgument(ConfiguredBaseModel):
    mapping_name: Optional[str] = Field(default=None)
    source_path: Optional[str] = Field(default=None)
    varname: Optional[str] = Field(default=None)
    process_state: Optional[str] = Field(default=None)
    imputation_state: Optional[str] = Field(default=None)
    value_type: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)


class CalculationResult(ConfiguredBaseModel):
    mapping_name: Optional[str] = Field(default=None)
    value_type: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    round_decimals: Optional[int] = Field(default=None)
    scale_factor: Optional[Decimal] = Field(default=None)
    destination_path: Optional[str] = Field(default=None)


class ValidationDesign(ConfiguredBaseModel):
    validation_name: Optional[str] = Field(default=None)
    validation_condition_expression: Optional[ValidationExpression] = Field(default=None)
    validation_result_expression: Optional[ValidationExpression] = Field(default=None)
    validation_error_level: Optional[ValidationErrorLevel] = Field(default=None)
    validation_error_message_template: Optional[str] = Field(default=None)
    conditional: Optional[str] = Field(default=None)


class ValidationExpression(ConfiguredBaseModel):
    validation_subject_source_paths: Optional[List[str]] = Field(default=None)
    validation_command: Optional[ValidationCommand] = Field(default=None)
    validation_arg_values: Optional[List[str]] = Field(default=None)
    validation_arg_source_paths: Optional[List[str]] = Field(default=None)
    validation_arg_expressions: Optional[List[ValidationExpression]] = Field(default=None)


class Contact(HasContextAliases):
    name: Optional[str] = Field(default=None)
    orcid: Optional[str] = Field(default=None)
    contact_roles: Optional[List[ContactRole]] = Field(default=None)
    contact_email: Optional[str] = Field(default=None)
    contact_phone: Optional[str] = Field(default=None)
    context_aliases: Optional[List[ContextAlias]] = Field(default=None)


class Stakeholder(HasTranslations, NamedThing):
    rorid: Optional[str] = Field(default=None)
    geographic_scope: Optional[str] = Field(default=None)
    translations: Optional[List[Translation]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ProjectStakeholder(HasTranslations):
    stakeholder: Optional[str] = Field(default=None)
    project_roles: Optional[List[ProjectRole]] = Field(default=None)
    contacts: Optional[List[Contact]] = Field(default=None)
    translations: Optional[List[Translation]] = Field(default=None)


class StudyEntity(NamedThing):
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Project(StudyEntity, HasTranslations, HasContextAliases):
    default_language: Optional[str] = Field(default=None)
    project_stakeholders: Optional[List[ProjectStakeholder]] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    study_id_list: Optional[List[str]] = Field(default=None)
    translations: Optional[List[Translation]] = Field(default=None)
    context_aliases: Optional[List[ContextAlias]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class StudyEntityLink(ConfiguredBaseModel):
    linktype: Optional[LinkType] = Field(default=None)
    study_entity: Optional[str] = Field(default=None)


class Study(StudyEntity, HasTranslations, HasContextAliases):
    default_language: Optional[str] = Field(default=None)
    study_stakeholders: Optional[List[StudyStakeholder]] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    observation_group_id_list: Optional[List[str]] = Field(default=None)
    study_entity_id_list: Optional[List[str]] = Field(default=None)
    project_id_list: Optional[List[str]] = Field(default=None)
    translations: Optional[List[Translation]] = Field(default=None)
    context_aliases: Optional[List[ContextAlias]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class StudyStakeholder(ConfiguredBaseModel):
    stakeholder: Optional[str] = Field(default=None)
    study_roles: Optional[List[StudyRole]] = Field(default=None)
    contacts: Optional[List[Contact]] = Field(default=None)


class ObservationGroup(StudyEntity):
    sort_order: Optional[Decimal] = Field(default=None)
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    observation_id_list: Optional[List[str]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class StudyPopulation(StudyEntity):
    research_population_type: Optional[ResearchPopulationType] = Field(default=None)
    member_id_list: Optional[List[str]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class SampleCollection(StudyEntity):
    matrix: Optional[str] = Field(default=None)
    constraints: Optional[List[str]] = Field(default=None)
    sample_id_list: Optional[List[str]] = Field(default=None)
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class StudySubject(StudyEntity):
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class StudySubjectGroup(StudyEntity):
    physical_entity: Optional[str] = Field(default=None)
    study_entity_links: Optional[List[StudyEntityLink]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class Observation(NamedThing):
    observation_type: Optional[ObservationType] = Field(default=None)
    observation_design: Optional[ObservationDesign] = Field(default=None)
    observation_result_id_list: Optional[List[str]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ObservationDesign(ConfiguredBaseModel):
    observable_entity_property_sets: Optional[List[ObservableEntityPropertySet]] = Field(default=None)


class ObservableEntityPropertySet(ConfiguredBaseModel):
    observation_result_type: Optional[ObservationResultType] = Field(default=None)
    observable_entity_type: Optional[ObservableEntityType] = Field(default=None)
    observable_entity_id_list: Optional[List[str]] = Field(default=None)
    identifying_observable_property_id_list: Optional[List[str]] = Field(default=None)
    required_observable_property_id_list: Optional[List[str]] = Field(default=None)
    optional_observable_property_id_list: Optional[List[str]] = Field(default=None)


class ObservationResult(NamedThing):
    observation_result_type: Optional[ObservationResultType] = Field(default=None)
    observation_start_date: Optional[date] = Field(default=None)
    observation_end_date: Optional[date] = Field(default=None)
    observed_values: Optional[List[ObservedValue]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ObservedValue(ConfiguredBaseModel):
    observable_entity: Optional[str] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)
    default_unit: Optional[str] = Field(default=None)
    raw_value: Optional[str] = Field(default=None)
    raw_unit: Optional[str] = Field(default=None)
    imputed_value: Optional[str] = Field(default=None)
    imputed_unit: Optional[str] = Field(default=None)
    normalised_value: Optional[str] = Field(default=None)
    normalised_unit: Optional[str] = Field(default=None)
    value: Optional[str] = Field(default=None)
    unit: Optional[str] = Field(default=None)
    value_as_string: Optional[str] = Field(default=None)
    quality_data: Optional[List[QualityData]] = Field(default=None)
    provenance_data: Optional[List[ProvenanceData]] = Field(default=None)


class QualityData(ConfiguredBaseModel):
    quality_context_key: Optional[str] = Field(default=None)
    quality_value: Optional[str] = Field(default=None)


class ProvenanceData(ConfiguredBaseModel):
    provenance_context_key: Optional[str] = Field(default=None)
    provenance_value: Optional[str] = Field(default=None)


class DataLayout(NamedThing):
    sections: Optional[List[DataLayoutSection]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class DataLayoutSection(NamedThing):
    section_type: Optional[DataLayoutSectionType] = Field(default=None)
    observable_entity_types: Optional[List[ObservableEntityType]] = Field(default=None)
    observable_entity_grouping_id_list: Optional[List[str]] = Field(default=None)
    elements: Optional[List[DataLayoutElement]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class DataLayoutElement(ConfiguredBaseModel):
    label: Optional[str] = Field(default=None)
    element_type: Optional[DataLayoutElementType] = Field(default=None)
    element_style: Optional[DataLayoutElementStyle] = Field(default=None)
    varname: Optional[str] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)
    is_observable_entity_key: Optional[bool] = Field(default=None)
    is_foreign_key: Optional[bool] = Field(default=None)


class DataRequest(NamedThing):
    contacts: Optional[List[Contact]] = Field(default=None)
    request_properties: Optional[str] = Field(default=None)
    data_stakeholders: Optional[List[str]] = Field(default=None)
    research_objectives: Optional[List[str]] = Field(default=None)
    processing_actions: Optional[List[str]] = Field(default=None)
    processing_steps: Optional[List[str]] = Field(default=None)
    remark_on_content: Optional[str] = Field(default=None)
    remark_on_methodology: Optional[str] = Field(default=None)
    observed_entity_properties: Optional[List[ObservedEntityProperty]] = Field(default=None)
    observable_entity_property_sets: Optional[List[ObservableEntityPropertySet]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ObservedEntityProperty(ConfiguredBaseModel):
    observable_entity: Optional[str] = Field(default=None)
    observable_property: Optional[str] = Field(default=None)


class DataStakeholder(NamedThing):
    stakeholder: Optional[str] = Field(default=None)
    data_roles: Optional[List[DataRole]] = Field(default=None)
    contacts: Optional[List[Contact]] = Field(default=None)
    processing_description: Optional[str] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ResearchObjective(NamedThing):
    objective_type: Optional[ObjectiveType] = Field(default=None)
    authors: Optional[List[str]] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ProcessingAction(NamedThing):
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class ProcessingStep(NamedThing):
    start_date: Optional[date] = Field(default=None)
    delivery_date: Optional[date] = Field(default=None)
    id: str = Field(default=...)
    unique_name: Optional[str] = Field(default=None)
    name: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    label: Optional[str] = Field(default=None)
    remark: Optional[str] = Field(default=None)


class DataExtract(ConfiguredBaseModel):
    observed_values: Optional[List[ObservedValue]] = Field(default=None)


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
Unit.model_rebuild()
BioChemEntity.model_rebuild()
BioChemIdentifier.model_rebuild()
BioChemIdentifierSchema.model_rebuild()
Matrix.model_rebuild()
Indicator.model_rebuild()
BioChemEntityLink.model_rebuild()
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
CalculationArgument.model_rebuild()
CalculationKeywordArgument.model_rebuild()
CalculationResult.model_rebuild()
ValidationDesign.model_rebuild()
ValidationExpression.model_rebuild()
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
ObservationDesign.model_rebuild()
ObservableEntityPropertySet.model_rebuild()
ObservationResult.model_rebuild()
ObservedValue.model_rebuild()
QualityData.model_rebuild()
ProvenanceData.model_rebuild()
DataLayout.model_rebuild()
DataLayoutSection.model_rebuild()
DataLayoutElement.model_rebuild()
DataRequest.model_rebuild()
ObservedEntityProperty.model_rebuild()
DataStakeholder.model_rebuild()
ResearchObjective.model_rebuild()
ProcessingAction.model_rebuild()
ProcessingStep.model_rebuild()
DataExtract.model_rebuild()

