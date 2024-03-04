# Auto generated from peh.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-02-26T15:49:09
# Schema: PEH-Model
#
# id: https://w3id.org/peh/peh-model
# description: Entity and relation ontology and datamodel for Personal Exposure and Health data
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import Boolean, Date, Datetime, Decimal, Integer, String
from linkml_runtime.utils.metamodelcore import Bool, Decimal, XSDDate, XSDDateTime

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
IOP = CurieNamespace('iop', 'http://example.org/UNKNOWN/iop/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
PEH = CurieNamespace('peh', 'https://w3id.org/peh/peh-model')
PROV = CurieNamespace('prov', 'http://www.w3.org/ns/prov#')
QUDT = CurieNamespace('qudt', 'http://qudt.org/2.1/schema/qudt')
QUDTQK = CurieNamespace('qudtqk', 'http://qudt.org/2.1/vocab/quantitykind')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = PEH


# Types

# Class references
class NamedThingId(extended_str):
    pass


class GroupingId(NamedThingId):
    pass


class UnitId(NamedThingId):
    pass


class BioChemEntityId(NamedThingId):
    pass


class BioChemIdentifierSchemaId(NamedThingId):
    pass


class MatrixId(NamedThingId):
    pass


class IndicatorId(NamedThingId):
    pass


class ObservablePropertyId(NamedThingId):
    pass


class ObservablePropertyMetadataFieldId(NamedThingId):
    pass


class StakeholderId(NamedThingId):
    pass


class StudyEntityId(NamedThingId):
    pass


class ProjectId(StudyEntityId):
    pass


class StudyId(StudyEntityId):
    pass


class TimepointId(StudyEntityId):
    pass


class StudyPopulationId(StudyEntityId):
    pass


class SampleCollectionId(StudyEntityId):
    pass


class SampleId(StudyEntityId):
    pass


class StudySubjectId(StudyEntityId):
    pass


class PersonId(StudyEntityId):
    pass


class PersonGroupId(StudyEntityId):
    pass


class GeolocationId(StudyEntityId):
    pass


class EnvironmentId(StudyEntityId):
    pass


class ObservationId(NamedThingId):
    pass


class MetadataObservationId(ObservationId):
    pass


class QuestionnaireObservationId(ObservationId):
    pass


class SamplingObservationId(ObservationId):
    pass


class GeospatialObservationId(ObservationId):
    pass


class DataRequestId(NamedThingId):
    pass


class DataStakeholderId(NamedThingId):
    pass


class ResearchObjectiveId(NamedThingId):
    pass


class ProcessingActionId(NamedThingId):
    pass


class ProcessingStepId(NamedThingId):
    pass


@dataclass
class EntityList(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["EntityList"]
    class_class_curie: ClassVar[str] = "peh:EntityList"
    class_name: ClassVar[str] = "EntityList"
    class_model_uri: ClassVar[URIRef] = PEH.EntityList

    matrices: Optional[Union[Dict[Union[str, MatrixId], Union[dict, "Matrix"]], List[Union[dict, "Matrix"]]]] = empty_dict()
    metadata_fields: Optional[Union[Dict[Union[str, ObservablePropertyMetadataFieldId], Union[dict, "ObservablePropertyMetadataField"]], List[Union[dict, "ObservablePropertyMetadataField"]]]] = empty_dict()
    biochementities: Optional[Union[Dict[Union[str, BioChemEntityId], Union[dict, "BioChemEntity"]], List[Union[dict, "BioChemEntity"]]]] = empty_dict()
    groupings: Optional[Union[Dict[Union[str, GroupingId], Union[dict, "Grouping"]], List[Union[dict, "Grouping"]]]] = empty_dict()
    indicators: Optional[Union[Dict[Union[str, IndicatorId], Union[dict, "Indicator"]], List[Union[dict, "Indicator"]]]] = empty_dict()
    units: Optional[Union[Dict[Union[str, UnitId], Union[dict, "Unit"]], List[Union[dict, "Unit"]]]] = empty_dict()
    observable_properties: Optional[Union[Dict[Union[str, ObservablePropertyId], Union[dict, "ObservableProperty"]], List[Union[dict, "ObservableProperty"]]]] = empty_dict()
    stakeholders: Optional[Union[Dict[Union[str, StakeholderId], Union[dict, "Stakeholder"]], List[Union[dict, "Stakeholder"]]]] = empty_dict()
    projects: Optional[Union[Dict[Union[str, ProjectId], Union[dict, "Project"]], List[Union[dict, "Project"]]]] = empty_dict()
    studies: Optional[Union[Dict[Union[str, StudyId], Union[dict, "Study"]], List[Union[dict, "Study"]]]] = empty_dict()
    timepoints: Optional[Union[Dict[Union[str, TimepointId], Union[dict, "Timepoint"]], List[Union[dict, "Timepoint"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="matrices", slot_type=Matrix, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="metadata_fields", slot_type=ObservablePropertyMetadataField, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="biochementities", slot_type=BioChemEntity, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="groupings", slot_type=Grouping, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="indicators", slot_type=Indicator, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="units", slot_type=Unit, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="observable_properties", slot_type=ObservableProperty, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="stakeholders", slot_type=Stakeholder, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="projects", slot_type=Project, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="studies", slot_type=Study, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="timepoints", slot_type=Timepoint, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class NamedThing(YAMLRoot):
    """
    A generic grouping for any identifiable entity
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["NamedThing"]
    class_class_curie: ClassVar[str] = "peh:NamedThing"
    class_name: ClassVar[str] = "NamedThing"
    class_model_uri: ClassVar[URIRef] = PEH.NamedThing

    id: Union[str, NamedThingId] = None
    unique_name: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    label: Optional[str] = None
    remark: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, NamedThingId):
            self.id = NamedThingId(self.id)

        if self.unique_name is not None and not isinstance(self.unique_name, str):
            self.unique_name = str(self.unique_name)

        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.remark is not None and not isinstance(self.remark, str):
            self.remark = str(self.remark)

        super().__post_init__(**kwargs)


@dataclass
class Grouping(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Grouping"]
    class_class_curie: ClassVar[str] = "peh:Grouping"
    class_name: ClassVar[str] = "Grouping"
    class_model_uri: ClassVar[URIRef] = PEH.Grouping

    id: Union[str, GroupingId] = None
    sort_order: Optional[Decimal] = None
    abstract: Optional[Union[bool, Bool]] = None
    parent_grouping_id_list: Optional[Union[Union[str, GroupingId], List[Union[str, GroupingId]]]] = empty_list()
    context_aliases: Optional[Union[Union[dict, "ContextAlias"], List[Union[dict, "ContextAlias"]]]] = empty_list()
    translations: Optional[Union[Union[dict, "Translation"], List[Union[dict, "Translation"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GroupingId):
            self.id = GroupingId(self.id)

        if self.sort_order is not None and not isinstance(self.sort_order, Decimal):
            self.sort_order = Decimal(self.sort_order)

        if self.abstract is not None and not isinstance(self.abstract, Bool):
            self.abstract = Bool(self.abstract)

        if not isinstance(self.parent_grouping_id_list, list):
            self.parent_grouping_id_list = [self.parent_grouping_id_list] if self.parent_grouping_id_list is not None else []
        self.parent_grouping_id_list = [v if isinstance(v, GroupingId) else GroupingId(v) for v in self.parent_grouping_id_list]

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass
class HasValidationStatus(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["HasValidationStatus"]
    class_class_curie: ClassVar[str] = "peh:HasValidationStatus"
    class_name: ClassVar[str] = "HasValidationStatus"
    class_model_uri: ClassVar[URIRef] = PEH.HasValidationStatus

    current_validation_status: Optional[Union[str, "ValidationStatus"]] = None
    validation_history: Optional[Union[Union[dict, "ValidationHistoryRecord"], List[Union[dict, "ValidationHistoryRecord"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.current_validation_status is not None and not isinstance(self.current_validation_status, ValidationStatus):
            self.current_validation_status = ValidationStatus(self.current_validation_status)

        if not isinstance(self.validation_history, list):
            self.validation_history = [self.validation_history] if self.validation_history is not None else []
        self.validation_history = [v if isinstance(v, ValidationHistoryRecord) else ValidationHistoryRecord(**as_dict(v)) for v in self.validation_history]

        super().__post_init__(**kwargs)


@dataclass
class ValidationHistoryRecord(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ValidationHistoryRecord"]
    class_class_curie: ClassVar[str] = "peh:ValidationHistoryRecord"
    class_name: ClassVar[str] = "ValidationHistoryRecord"
    class_model_uri: ClassVar[URIRef] = PEH.ValidationHistoryRecord

    validation_datetime: Optional[Union[str, XSDDateTime]] = None
    validation_status: Optional[Union[str, "ValidationStatus"]] = None
    validation_actor: Optional[str] = None
    validation_institute: Optional[str] = None
    validation_remark: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.validation_datetime is not None and not isinstance(self.validation_datetime, XSDDateTime):
            self.validation_datetime = XSDDateTime(self.validation_datetime)

        if self.validation_status is not None and not isinstance(self.validation_status, ValidationStatus):
            self.validation_status = ValidationStatus(self.validation_status)

        if self.validation_actor is not None and not isinstance(self.validation_actor, str):
            self.validation_actor = str(self.validation_actor)

        if self.validation_institute is not None and not isinstance(self.validation_institute, str):
            self.validation_institute = str(self.validation_institute)

        if self.validation_remark is not None and not isinstance(self.validation_remark, str):
            self.validation_remark = str(self.validation_remark)

        super().__post_init__(**kwargs)


@dataclass
class HasAliases(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["HasAliases"]
    class_class_curie: ClassVar[str] = "peh:HasAliases"
    class_name: ClassVar[str] = "HasAliases"
    class_model_uri: ClassVar[URIRef] = PEH.HasAliases

    aliases: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        super().__post_init__(**kwargs)


@dataclass
class HasContextAliases(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["HasContextAliases"]
    class_class_curie: ClassVar[str] = "peh:HasContextAliases"
    class_name: ClassVar[str] = "HasContextAliases"
    class_model_uri: ClassVar[URIRef] = PEH.HasContextAliases

    context_aliases: Optional[Union[Union[dict, "ContextAlias"], List[Union[dict, "ContextAlias"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass
class ContextAlias(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ContextAlias"]
    class_class_curie: ClassVar[str] = "peh:ContextAlias"
    class_name: ClassVar[str] = "ContextAlias"
    class_model_uri: ClassVar[URIRef] = PEH.ContextAlias

    context: Optional[Union[str, NamedThingId]] = None
    alias: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.context is not None and not isinstance(self.context, NamedThingId):
            self.context = NamedThingId(self.context)

        if self.alias is not None and not isinstance(self.alias, str):
            self.alias = str(self.alias)

        super().__post_init__(**kwargs)


@dataclass
class HasTranslations(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["HasTranslations"]
    class_class_curie: ClassVar[str] = "peh:HasTranslations"
    class_name: ClassVar[str] = "HasTranslations"
    class_model_uri: ClassVar[URIRef] = PEH.HasTranslations

    translations: Optional[Union[Union[dict, "Translation"], List[Union[dict, "Translation"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass
class Translation(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Translation"]
    class_class_curie: ClassVar[str] = "peh:Translation"
    class_name: ClassVar[str] = "Translation"
    class_model_uri: ClassVar[URIRef] = PEH.Translation

    property_name: Optional[str] = None
    language: Optional[str] = None
    translated_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.property_name is not None and not isinstance(self.property_name, str):
            self.property_name = str(self.property_name)

        if self.language is not None and not isinstance(self.language, str):
            self.language = str(self.language)

        if self.translated_value is not None and not isinstance(self.translated_value, str):
            self.translated_value = str(self.translated_value)

        super().__post_init__(**kwargs)


@dataclass
class Unit(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Unit"]
    class_class_curie: ClassVar[str] = "peh:Unit"
    class_name: ClassVar[str] = "Unit"
    class_model_uri: ClassVar[URIRef] = PEH.Unit

    id: Union[str, UnitId] = None
    same_unit_as: Optional[Union[str, "QudtUnit"]] = None
    quantity_kind: Optional[Union[str, "QudtQuantityKind"]] = None
    context_aliases: Optional[Union[Union[dict, ContextAlias], List[Union[dict, ContextAlias]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], List[Union[dict, Translation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, UnitId):
            self.id = UnitId(self.id)

        if self.quantity_kind is not None and not isinstance(self.quantity_kind, QudtQuantityKind):
            self.quantity_kind = QudtQuantityKind(self.quantity_kind)

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass
class BioChemEntity(NamedThing):
    """
    A biological, chemical or biochemical entity that is relevant to the Personal Exposure and Health domain
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCHEMA["BioChemEntity"]
    class_class_curie: ClassVar[str] = "schema:BioChemEntity"
    class_name: ClassVar[str] = "BioChemEntity"
    class_model_uri: ClassVar[URIRef] = PEH.BioChemEntity

    id: Union[str, BioChemEntityId] = None
    grouping: Optional[Union[str, GroupingId]] = None
    biochemidentifiers: Optional[Union[Union[dict, "BioChemIdentifier"], List[Union[dict, "BioChemIdentifier"]]]] = empty_list()
    biochementity_links: Optional[Union[Union[dict, "BioChemEntityLink"], List[Union[dict, "BioChemEntityLink"]]]] = empty_list()
    aliases: Optional[Union[str, List[str]]] = empty_list()
    context_aliases: Optional[Union[Union[dict, ContextAlias], List[Union[dict, ContextAlias]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], List[Union[dict, Translation]]]] = empty_list()
    current_validation_status: Optional[Union[str, "ValidationStatus"]] = None
    validation_history: Optional[Union[Union[dict, ValidationHistoryRecord], List[Union[dict, ValidationHistoryRecord]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BioChemEntityId):
            self.id = BioChemEntityId(self.id)

        if self.grouping is not None and not isinstance(self.grouping, GroupingId):
            self.grouping = GroupingId(self.grouping)

        if not isinstance(self.biochemidentifiers, list):
            self.biochemidentifiers = [self.biochemidentifiers] if self.biochemidentifiers is not None else []
        self.biochemidentifiers = [v if isinstance(v, BioChemIdentifier) else BioChemIdentifier(**as_dict(v)) for v in self.biochemidentifiers]

        if not isinstance(self.biochementity_links, list):
            self.biochementity_links = [self.biochementity_links] if self.biochementity_links is not None else []
        self.biochementity_links = [v if isinstance(v, BioChemEntityLink) else BioChemEntityLink(**as_dict(v)) for v in self.biochementity_links]

        if not isinstance(self.aliases, list):
            self.aliases = [self.aliases] if self.aliases is not None else []
        self.aliases = [v if isinstance(v, str) else str(v) for v in self.aliases]

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        if self.current_validation_status is not None and not isinstance(self.current_validation_status, ValidationStatus):
            self.current_validation_status = ValidationStatus(self.current_validation_status)

        if not isinstance(self.validation_history, list):
            self.validation_history = [self.validation_history] if self.validation_history is not None else []
        self.validation_history = [v if isinstance(v, ValidationHistoryRecord) else ValidationHistoryRecord(**as_dict(v)) for v in self.validation_history]

        super().__post_init__(**kwargs)


@dataclass
class BioChemIdentifier(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["BioChemIdentifier"]
    class_class_curie: ClassVar[str] = "peh:BioChemIdentifier"
    class_name: ClassVar[str] = "BioChemIdentifier"
    class_model_uri: ClassVar[URIRef] = PEH.BioChemIdentifier

    identifier_schema: Optional[Union[str, BioChemIdentifierSchemaId]] = None
    identifier_code: Optional[str] = None
    current_validation_status: Optional[Union[str, "ValidationStatus"]] = None
    validation_history: Optional[Union[Union[dict, ValidationHistoryRecord], List[Union[dict, ValidationHistoryRecord]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.identifier_schema is not None and not isinstance(self.identifier_schema, BioChemIdentifierSchemaId):
            self.identifier_schema = BioChemIdentifierSchemaId(self.identifier_schema)

        if self.identifier_code is not None and not isinstance(self.identifier_code, str):
            self.identifier_code = str(self.identifier_code)

        if self.current_validation_status is not None and not isinstance(self.current_validation_status, ValidationStatus):
            self.current_validation_status = ValidationStatus(self.current_validation_status)

        if not isinstance(self.validation_history, list):
            self.validation_history = [self.validation_history] if self.validation_history is not None else []
        self.validation_history = [v if isinstance(v, ValidationHistoryRecord) else ValidationHistoryRecord(**as_dict(v)) for v in self.validation_history]

        super().__post_init__(**kwargs)


@dataclass
class BioChemIdentifierSchema(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["BioChemIdentifierSchema"]
    class_class_curie: ClassVar[str] = "peh:BioChemIdentifierSchema"
    class_name: ClassVar[str] = "BioChemIdentifierSchema"
    class_model_uri: ClassVar[URIRef] = PEH.BioChemIdentifierSchema

    id: Union[str, BioChemIdentifierSchemaId] = None
    web_uri: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, BioChemIdentifierSchemaId):
            self.id = BioChemIdentifierSchemaId(self.id)

        if self.web_uri is not None and not isinstance(self.web_uri, str):
            self.web_uri = str(self.web_uri)

        super().__post_init__(**kwargs)


@dataclass
class Matrix(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Matrix"]
    class_class_curie: ClassVar[str] = "peh:Matrix"
    class_name: ClassVar[str] = "Matrix"
    class_model_uri: ClassVar[URIRef] = PEH.Matrix

    id: Union[str, MatrixId] = None
    sort_order: Optional[Decimal] = None
    aggregation_target: Optional[Union[bool, Bool]] = None
    parent_matrix: Optional[Union[str, MatrixId]] = None
    context_aliases: Optional[Union[Union[dict, ContextAlias], List[Union[dict, ContextAlias]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], List[Union[dict, Translation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MatrixId):
            self.id = MatrixId(self.id)

        if self.sort_order is not None and not isinstance(self.sort_order, Decimal):
            self.sort_order = Decimal(self.sort_order)

        if self.aggregation_target is not None and not isinstance(self.aggregation_target, Bool):
            self.aggregation_target = Bool(self.aggregation_target)

        if self.parent_matrix is not None and not isinstance(self.parent_matrix, MatrixId):
            self.parent_matrix = MatrixId(self.parent_matrix)

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass
class Indicator(NamedThing):
    """
    A measurable indicator that is relevant to the Personal Exposure and Health domain
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Indicator"]
    class_class_curie: ClassVar[str] = "peh:Indicator"
    class_name: ClassVar[str] = "Indicator"
    class_model_uri: ClassVar[URIRef] = PEH.Indicator

    id: Union[str, IndicatorId] = None
    indicator_type: Optional[Union[str, "IndicatorType"]] = None
    quantity_kind: Optional[Union[str, "QudtQuantityKind"]] = None
    matrix: Optional[Union[str, MatrixId]] = None
    constraints: Optional[Union[str, List[str]]] = empty_list()
    relevant_observable_entity_types: Optional[Union[Union[str, "ObservableEntityType"], List[Union[str, "ObservableEntityType"]]]] = empty_list()
    biochementity_links: Optional[Union[Union[dict, "BioChemEntityLink"], List[Union[dict, "BioChemEntityLink"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, IndicatorId):
            self.id = IndicatorId(self.id)

        if self.indicator_type is not None and not isinstance(self.indicator_type, IndicatorType):
            self.indicator_type = IndicatorType(self.indicator_type)

        if self.quantity_kind is not None and not isinstance(self.quantity_kind, QudtQuantityKind):
            self.quantity_kind = QudtQuantityKind(self.quantity_kind)

        if self.matrix is not None and not isinstance(self.matrix, MatrixId):
            self.matrix = MatrixId(self.matrix)

        if not isinstance(self.constraints, list):
            self.constraints = [self.constraints] if self.constraints is not None else []
        self.constraints = [v if isinstance(v, str) else str(v) for v in self.constraints]

        if not isinstance(self.relevant_observable_entity_types, list):
            self.relevant_observable_entity_types = [self.relevant_observable_entity_types] if self.relevant_observable_entity_types is not None else []
        self.relevant_observable_entity_types = [v if isinstance(v, ObservableEntityType) else ObservableEntityType(v) for v in self.relevant_observable_entity_types]

        if not isinstance(self.biochementity_links, list):
            self.biochementity_links = [self.biochementity_links] if self.biochementity_links is not None else []
        self.biochementity_links = [v if isinstance(v, BioChemEntityLink) else BioChemEntityLink(**as_dict(v)) for v in self.biochementity_links]

        super().__post_init__(**kwargs)


@dataclass
class BioChemEntityLink(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["BioChemEntityLink"]
    class_class_curie: ClassVar[str] = "peh:BioChemEntityLink"
    class_name: ClassVar[str] = "BioChemEntityLink"
    class_model_uri: ClassVar[URIRef] = PEH.BioChemEntityLink

    biochementity_linktype: Optional[Union[str, "BioChemEntityLinkType"]] = None
    biochementity: Optional[Union[str, BioChemEntityId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.biochementity_linktype is not None and not isinstance(self.biochementity_linktype, BioChemEntityLinkType):
            self.biochementity_linktype = BioChemEntityLinkType(self.biochementity_linktype)

        if self.biochementity is not None and not isinstance(self.biochementity, BioChemEntityId):
            self.biochementity = BioChemEntityId(self.biochementity)

        super().__post_init__(**kwargs)


@dataclass
class ObservableProperty(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ObservableProperty"]
    class_class_curie: ClassVar[str] = "peh:ObservableProperty"
    class_name: ClassVar[str] = "ObservableProperty"
    class_model_uri: ClassVar[URIRef] = PEH.ObservableProperty

    id: Union[str, ObservablePropertyId] = None
    value_type: Optional[str] = None
    categorical: Optional[Union[bool, Bool]] = None
    multivalued: Optional[Union[bool, Bool]] = None
    required: Optional[Union[bool, Bool]] = None
    value_options: Optional[Union[Union[dict, "ObservablePropertyValueOption"], List[Union[dict, "ObservablePropertyValueOption"]]]] = empty_list()
    value_metadata: Optional[Union[Union[dict, "ObservablePropertyMetadataElement"], List[Union[dict, "ObservablePropertyMetadataElement"]]]] = empty_list()
    quantity_kind: Optional[Union[str, "QudtQuantityKind"]] = None
    default_unit: Optional[str] = None
    default_significantdecimals: Optional[int] = None
    default_immutable: Optional[Union[bool, Bool]] = None
    grouping_id_list: Optional[Union[Union[str, GroupingId], List[Union[str, GroupingId]]]] = empty_list()
    relevant_observable_entity_types: Optional[Union[Union[str, "ObservableEntityType"], List[Union[str, "ObservableEntityType"]]]] = empty_list()
    relevant_observation_types: Optional[Union[Union[str, "ObservationType"], List[Union[str, "ObservationType"]]]] = empty_list()
    indicator: Optional[Union[str, IndicatorId]] = None
    calculation_design: Optional[Union[dict, "CalculationDesign"]] = None
    validation_design: Optional[Union[dict, "ValidationDesign"]] = None
    translations: Optional[Union[Union[dict, Translation], List[Union[dict, Translation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ObservablePropertyId):
            self.id = ObservablePropertyId(self.id)

        if self.value_type is not None and not isinstance(self.value_type, str):
            self.value_type = str(self.value_type)

        if self.categorical is not None and not isinstance(self.categorical, Bool):
            self.categorical = Bool(self.categorical)

        if self.multivalued is not None and not isinstance(self.multivalued, Bool):
            self.multivalued = Bool(self.multivalued)

        if self.required is not None and not isinstance(self.required, Bool):
            self.required = Bool(self.required)

        if not isinstance(self.value_options, list):
            self.value_options = [self.value_options] if self.value_options is not None else []
        self.value_options = [v if isinstance(v, ObservablePropertyValueOption) else ObservablePropertyValueOption(**as_dict(v)) for v in self.value_options]

        if not isinstance(self.value_metadata, list):
            self.value_metadata = [self.value_metadata] if self.value_metadata is not None else []
        self.value_metadata = [v if isinstance(v, ObservablePropertyMetadataElement) else ObservablePropertyMetadataElement(**as_dict(v)) for v in self.value_metadata]

        if self.quantity_kind is not None and not isinstance(self.quantity_kind, QudtQuantityKind):
            self.quantity_kind = QudtQuantityKind(self.quantity_kind)

        if self.default_unit is not None and not isinstance(self.default_unit, str):
            self.default_unit = str(self.default_unit)

        if self.default_significantdecimals is not None and not isinstance(self.default_significantdecimals, int):
            self.default_significantdecimals = int(self.default_significantdecimals)

        if self.default_immutable is not None and not isinstance(self.default_immutable, Bool):
            self.default_immutable = Bool(self.default_immutable)

        if not isinstance(self.grouping_id_list, list):
            self.grouping_id_list = [self.grouping_id_list] if self.grouping_id_list is not None else []
        self.grouping_id_list = [v if isinstance(v, GroupingId) else GroupingId(v) for v in self.grouping_id_list]

        if not isinstance(self.relevant_observable_entity_types, list):
            self.relevant_observable_entity_types = [self.relevant_observable_entity_types] if self.relevant_observable_entity_types is not None else []
        self.relevant_observable_entity_types = [v if isinstance(v, ObservableEntityType) else ObservableEntityType(v) for v in self.relevant_observable_entity_types]

        if not isinstance(self.relevant_observation_types, list):
            self.relevant_observation_types = [self.relevant_observation_types] if self.relevant_observation_types is not None else []
        self.relevant_observation_types = [v if isinstance(v, ObservationType) else ObservationType(v) for v in self.relevant_observation_types]

        if self.indicator is not None and not isinstance(self.indicator, IndicatorId):
            self.indicator = IndicatorId(self.indicator)

        if self.calculation_design is not None and not isinstance(self.calculation_design, CalculationDesign):
            self.calculation_design = CalculationDesign(**as_dict(self.calculation_design))

        if self.validation_design is not None and not isinstance(self.validation_design, ValidationDesign):
            self.validation_design = ValidationDesign(**as_dict(self.validation_design))

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass
class ObservablePropertyValueOption(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ObservablePropertyValueOption"]
    class_class_curie: ClassVar[str] = "peh:ObservablePropertyValueOption"
    class_name: ClassVar[str] = "ObservablePropertyValueOption"
    class_model_uri: ClassVar[URIRef] = PEH.ObservablePropertyValueOption

    key: Optional[str] = None
    value: Optional[str] = None
    label: Optional[str] = None
    context_aliases: Optional[Union[Union[dict, ContextAlias], List[Union[dict, ContextAlias]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.key is not None and not isinstance(self.key, str):
            self.key = str(self.key)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass
class ObservablePropertyMetadataElement(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ObservablePropertyMetadataElement"]
    class_class_curie: ClassVar[str] = "peh:ObservablePropertyMetadataElement"
    class_name: ClassVar[str] = "ObservablePropertyMetadataElement"
    class_model_uri: ClassVar[URIRef] = PEH.ObservablePropertyMetadataElement

    field: Optional[Union[str, ObservablePropertyMetadataFieldId]] = None
    value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.field is not None and not isinstance(self.field, ObservablePropertyMetadataFieldId):
            self.field = ObservablePropertyMetadataFieldId(self.field)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        super().__post_init__(**kwargs)


@dataclass
class ObservablePropertyMetadataField(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ObservablePropertyMetadataField"]
    class_class_curie: ClassVar[str] = "peh:ObservablePropertyMetadataField"
    class_name: ClassVar[str] = "ObservablePropertyMetadataField"
    class_model_uri: ClassVar[URIRef] = PEH.ObservablePropertyMetadataField

    id: Union[str, ObservablePropertyMetadataFieldId] = None
    value_type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ObservablePropertyMetadataFieldId):
            self.id = ObservablePropertyMetadataFieldId(self.id)

        if self.value_type is not None and not isinstance(self.value_type, str):
            self.value_type = str(self.value_type)

        super().__post_init__(**kwargs)


@dataclass
class CalculationDesign(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["CalculationDesign"]
    class_class_curie: ClassVar[str] = "peh:CalculationDesign"
    class_name: ClassVar[str] = "CalculationDesign"
    class_model_uri: ClassVar[URIRef] = PEH.CalculationDesign

    unit: Optional[Union[str, UnitId]] = None
    formula: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.unit is not None and not isinstance(self.unit, UnitId):
            self.unit = UnitId(self.unit)

        if self.formula is not None and not isinstance(self.formula, str):
            self.formula = str(self.formula)

        super().__post_init__(**kwargs)


@dataclass
class ValidationDesign(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ValidationDesign"]
    class_class_curie: ClassVar[str] = "peh:ValidationDesign"
    class_name: ClassVar[str] = "ValidationDesign"
    class_model_uri: ClassVar[URIRef] = PEH.ValidationDesign

    conditional: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.conditional is not None and not isinstance(self.conditional, str):
            self.conditional = str(self.conditional)

        super().__post_init__(**kwargs)


@dataclass
class Contact(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Contact"]
    class_class_curie: ClassVar[str] = "peh:Contact"
    class_name: ClassVar[str] = "Contact"
    class_model_uri: ClassVar[URIRef] = PEH.Contact

    name: Optional[str] = None
    orcid: Optional[str] = None
    contact_roles: Optional[Union[Union[str, "ContactRole"], List[Union[str, "ContactRole"]]]] = empty_list()
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    context_aliases: Optional[Union[Union[dict, ContextAlias], List[Union[dict, ContextAlias]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.name is not None and not isinstance(self.name, str):
            self.name = str(self.name)

        if self.orcid is not None and not isinstance(self.orcid, str):
            self.orcid = str(self.orcid)

        if not isinstance(self.contact_roles, list):
            self.contact_roles = [self.contact_roles] if self.contact_roles is not None else []
        self.contact_roles = [v if isinstance(v, ContactRole) else ContactRole(v) for v in self.contact_roles]

        if self.contact_email is not None and not isinstance(self.contact_email, str):
            self.contact_email = str(self.contact_email)

        if self.contact_phone is not None and not isinstance(self.contact_phone, str):
            self.contact_phone = str(self.contact_phone)

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass
class Stakeholder(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Stakeholder"]
    class_class_curie: ClassVar[str] = "peh:Stakeholder"
    class_name: ClassVar[str] = "Stakeholder"
    class_model_uri: ClassVar[URIRef] = PEH.Stakeholder

    id: Union[str, StakeholderId] = None
    rorid: Optional[str] = None
    geographic_scope: Optional[str] = None
    translations: Optional[Union[Union[dict, Translation], List[Union[dict, Translation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StakeholderId):
            self.id = StakeholderId(self.id)

        if self.rorid is not None and not isinstance(self.rorid, str):
            self.rorid = str(self.rorid)

        if self.geographic_scope is not None and not isinstance(self.geographic_scope, str):
            self.geographic_scope = str(self.geographic_scope)

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass
class ProjectStakeholder(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ProjectStakeholder"]
    class_class_curie: ClassVar[str] = "peh:ProjectStakeholder"
    class_name: ClassVar[str] = "ProjectStakeholder"
    class_model_uri: ClassVar[URIRef] = PEH.ProjectStakeholder

    stakeholder: Optional[Union[str, StakeholderId]] = None
    project_roles: Optional[Union[Union[str, "ProjectRole"], List[Union[str, "ProjectRole"]]]] = empty_list()
    contacts: Optional[Union[Union[dict, Contact], List[Union[dict, Contact]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], List[Union[dict, Translation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.stakeholder is not None and not isinstance(self.stakeholder, StakeholderId):
            self.stakeholder = StakeholderId(self.stakeholder)

        if not isinstance(self.project_roles, list):
            self.project_roles = [self.project_roles] if self.project_roles is not None else []
        self.project_roles = [v if isinstance(v, ProjectRole) else ProjectRole(v) for v in self.project_roles]

        if not isinstance(self.contacts, list):
            self.contacts = [self.contacts] if self.contacts is not None else []
        self.contacts = [v if isinstance(v, Contact) else Contact(**as_dict(v)) for v in self.contacts]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass
class StudyEntity(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["StudyEntity"]
    class_class_curie: ClassVar[str] = "peh:StudyEntity"
    class_name: ClassVar[str] = "StudyEntity"
    class_model_uri: ClassVar[URIRef] = PEH.StudyEntity

    id: Union[str, StudyEntityId] = None
    study_entity_links: Optional[Union[Union[dict, "StudyEntityLink"], List[Union[dict, "StudyEntityLink"]]]] = empty_list()
    context_aliases: Optional[Union[Union[dict, ContextAlias], List[Union[dict, ContextAlias]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.study_entity_links, list):
            self.study_entity_links = [self.study_entity_links] if self.study_entity_links is not None else []
        self.study_entity_links = [v if isinstance(v, StudyEntityLink) else StudyEntityLink(**as_dict(v)) for v in self.study_entity_links]

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        super().__post_init__(**kwargs)


@dataclass
class Project(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Project"]
    class_class_curie: ClassVar[str] = "peh:Project"
    class_name: ClassVar[str] = "Project"
    class_model_uri: ClassVar[URIRef] = PEH.Project

    id: Union[str, ProjectId] = None
    context_aliases: Optional[Union[Union[dict, ContextAlias], List[Union[dict, ContextAlias]]]] = empty_list()
    default_language: Optional[str] = None
    project_stakeholders: Optional[Union[Union[dict, "ProjectStakeholder"], List[Union[dict, "ProjectStakeholder"]]]] = empty_list()
    start_date: Optional[Union[str, XSDDate]] = None
    end_date: Optional[Union[str, XSDDate]] = None
    study_id_list: Optional[Union[Union[str, StudyId], List[Union[str, StudyId]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], List[Union[dict, Translation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProjectId):
            self.id = ProjectId(self.id)

        if not isinstance(self.context_aliases, list):
            self.context_aliases = [self.context_aliases] if self.context_aliases is not None else []
        self.context_aliases = [v if isinstance(v, ContextAlias) else ContextAlias(**as_dict(v)) for v in self.context_aliases]

        if self.default_language is not None and not isinstance(self.default_language, str):
            self.default_language = str(self.default_language)

        if not isinstance(self.project_stakeholders, list):
            self.project_stakeholders = [self.project_stakeholders] if self.project_stakeholders is not None else []
        self.project_stakeholders = [v if isinstance(v, ProjectStakeholder) else ProjectStakeholder(**as_dict(v)) for v in self.project_stakeholders]

        if self.start_date is not None and not isinstance(self.start_date, XSDDate):
            self.start_date = XSDDate(self.start_date)

        if self.end_date is not None and not isinstance(self.end_date, XSDDate):
            self.end_date = XSDDate(self.end_date)

        if not isinstance(self.study_id_list, list):
            self.study_id_list = [self.study_id_list] if self.study_id_list is not None else []
        self.study_id_list = [v if isinstance(v, StudyId) else StudyId(v) for v in self.study_id_list]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass
class StudyEntityLink(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["StudyEntityLink"]
    class_class_curie: ClassVar[str] = "peh:StudyEntityLink"
    class_name: ClassVar[str] = "StudyEntityLink"
    class_model_uri: ClassVar[URIRef] = PEH.StudyEntityLink

    linktype: Optional[Union[str, "LinkType"]] = None
    study_entity: Optional[Union[str, StudyEntityId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.linktype is not None and not isinstance(self.linktype, LinkType):
            self.linktype = LinkType(self.linktype)

        if self.study_entity is not None and not isinstance(self.study_entity, StudyEntityId):
            self.study_entity = StudyEntityId(self.study_entity)

        super().__post_init__(**kwargs)


@dataclass
class Study(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Study"]
    class_class_curie: ClassVar[str] = "peh:Study"
    class_name: ClassVar[str] = "Study"
    class_model_uri: ClassVar[URIRef] = PEH.Study

    id: Union[str, StudyId] = None
    default_language: Optional[str] = None
    study_stakeholders: Optional[Union[Union[dict, "StudyStakeholder"], List[Union[dict, "StudyStakeholder"]]]] = empty_list()
    start_date: Optional[Union[str, XSDDate]] = None
    end_date: Optional[Union[str, XSDDate]] = None
    timepoint_id_list: Optional[Union[Union[str, TimepointId], List[Union[str, TimepointId]]]] = empty_list()
    study_entities: Optional[Union[Union[str, StudyEntityId], List[Union[str, StudyEntityId]]]] = empty_list()
    project_id_list: Optional[Union[Union[str, ProjectId], List[Union[str, ProjectId]]]] = empty_list()
    translations: Optional[Union[Union[dict, Translation], List[Union[dict, Translation]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StudyId):
            self.id = StudyId(self.id)

        if self.default_language is not None and not isinstance(self.default_language, str):
            self.default_language = str(self.default_language)

        if not isinstance(self.study_stakeholders, list):
            self.study_stakeholders = [self.study_stakeholders] if self.study_stakeholders is not None else []
        self.study_stakeholders = [v if isinstance(v, StudyStakeholder) else StudyStakeholder(**as_dict(v)) for v in self.study_stakeholders]

        if self.start_date is not None and not isinstance(self.start_date, XSDDate):
            self.start_date = XSDDate(self.start_date)

        if self.end_date is not None and not isinstance(self.end_date, XSDDate):
            self.end_date = XSDDate(self.end_date)

        if not isinstance(self.timepoint_id_list, list):
            self.timepoint_id_list = [self.timepoint_id_list] if self.timepoint_id_list is not None else []
        self.timepoint_id_list = [v if isinstance(v, TimepointId) else TimepointId(v) for v in self.timepoint_id_list]

        if not isinstance(self.study_entities, list):
            self.study_entities = [self.study_entities] if self.study_entities is not None else []
        self.study_entities = [v if isinstance(v, StudyEntityId) else StudyEntityId(v) for v in self.study_entities]

        if not isinstance(self.project_id_list, list):
            self.project_id_list = [self.project_id_list] if self.project_id_list is not None else []
        self.project_id_list = [v if isinstance(v, ProjectId) else ProjectId(v) for v in self.project_id_list]

        if not isinstance(self.translations, list):
            self.translations = [self.translations] if self.translations is not None else []
        self.translations = [v if isinstance(v, Translation) else Translation(**as_dict(v)) for v in self.translations]

        super().__post_init__(**kwargs)


@dataclass
class StudyStakeholder(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["StudyStakeholder"]
    class_class_curie: ClassVar[str] = "peh:StudyStakeholder"
    class_name: ClassVar[str] = "StudyStakeholder"
    class_model_uri: ClassVar[URIRef] = PEH.StudyStakeholder

    stakeholder: Optional[Union[str, StakeholderId]] = None
    study_roles: Optional[Union[Union[str, "StudyRole"], List[Union[str, "StudyRole"]]]] = empty_list()
    contacts: Optional[Union[Union[dict, Contact], List[Union[dict, Contact]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.stakeholder is not None and not isinstance(self.stakeholder, StakeholderId):
            self.stakeholder = StakeholderId(self.stakeholder)

        if not isinstance(self.study_roles, list):
            self.study_roles = [self.study_roles] if self.study_roles is not None else []
        self.study_roles = [v if isinstance(v, StudyRole) else StudyRole(v) for v in self.study_roles]

        if not isinstance(self.contacts, list):
            self.contacts = [self.contacts] if self.contacts is not None else []
        self.contacts = [v if isinstance(v, Contact) else Contact(**as_dict(v)) for v in self.contacts]

        super().__post_init__(**kwargs)


@dataclass
class Timepoint(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Timepoint"]
    class_class_curie: ClassVar[str] = "peh:Timepoint"
    class_name: ClassVar[str] = "Timepoint"
    class_model_uri: ClassVar[URIRef] = PEH.Timepoint

    id: Union[str, TimepointId] = None
    sort_order: Optional[Decimal] = None
    start_date: Optional[Union[str, XSDDate]] = None
    end_date: Optional[Union[str, XSDDate]] = None
    observations: Optional[Union[Dict[Union[str, ObservationId], Union[dict, "Observation"]], List[Union[dict, "Observation"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TimepointId):
            self.id = TimepointId(self.id)

        if self.sort_order is not None and not isinstance(self.sort_order, Decimal):
            self.sort_order = Decimal(self.sort_order)

        if self.start_date is not None and not isinstance(self.start_date, XSDDate):
            self.start_date = XSDDate(self.start_date)

        if self.end_date is not None and not isinstance(self.end_date, XSDDate):
            self.end_date = XSDDate(self.end_date)

        self._normalize_inlined_as_list(slot_name="observations", slot_type=Observation, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class StudyPopulation(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["StudyPopulation"]
    class_class_curie: ClassVar[str] = "peh:StudyPopulation"
    class_name: ClassVar[str] = "StudyPopulation"
    class_model_uri: ClassVar[URIRef] = PEH.StudyPopulation

    id: Union[str, StudyPopulationId] = None
    research_population_type: Optional[Union[str, "ResearchPopulationType"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StudyPopulationId):
            self.id = StudyPopulationId(self.id)

        if self.research_population_type is not None and not isinstance(self.research_population_type, ResearchPopulationType):
            self.research_population_type = ResearchPopulationType(self.research_population_type)

        super().__post_init__(**kwargs)


@dataclass
class SampleCollection(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["SampleCollection"]
    class_class_curie: ClassVar[str] = "peh:SampleCollection"
    class_name: ClassVar[str] = "SampleCollection"
    class_model_uri: ClassVar[URIRef] = PEH.SampleCollection

    id: Union[str, SampleCollectionId] = None
    matrix: Optional[Union[str, MatrixId]] = None
    constraints: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SampleCollectionId):
            self.id = SampleCollectionId(self.id)

        if self.matrix is not None and not isinstance(self.matrix, MatrixId):
            self.matrix = MatrixId(self.matrix)

        if not isinstance(self.constraints, list):
            self.constraints = [self.constraints] if self.constraints is not None else []
        self.constraints = [v if isinstance(v, str) else str(v) for v in self.constraints]

        super().__post_init__(**kwargs)


@dataclass
class Sample(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Sample"]
    class_class_curie: ClassVar[str] = "peh:Sample"
    class_name: ClassVar[str] = "Sample"
    class_model_uri: ClassVar[URIRef] = PEH.Sample

    id: Union[str, SampleId] = None
    matrix: Optional[Union[str, MatrixId]] = None
    constraints: Optional[Union[str, List[str]]] = empty_list()
    sampled_in_project: Optional[Union[str, ProjectId]] = None
    physical_label: Optional[str] = None
    collection_date: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SampleId):
            self.id = SampleId(self.id)

        if self.matrix is not None and not isinstance(self.matrix, MatrixId):
            self.matrix = MatrixId(self.matrix)

        if not isinstance(self.constraints, list):
            self.constraints = [self.constraints] if self.constraints is not None else []
        self.constraints = [v if isinstance(v, str) else str(v) for v in self.constraints]

        if self.sampled_in_project is not None and not isinstance(self.sampled_in_project, ProjectId):
            self.sampled_in_project = ProjectId(self.sampled_in_project)

        if self.physical_label is not None and not isinstance(self.physical_label, str):
            self.physical_label = str(self.physical_label)

        if self.collection_date is not None and not isinstance(self.collection_date, XSDDate):
            self.collection_date = XSDDate(self.collection_date)

        super().__post_init__(**kwargs)


@dataclass
class StudySubject(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["StudySubject"]
    class_class_curie: ClassVar[str] = "peh:StudySubject"
    class_name: ClassVar[str] = "StudySubject"
    class_model_uri: ClassVar[URIRef] = PEH.StudySubject

    id: Union[str, StudySubjectId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, StudySubjectId):
            self.id = StudySubjectId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Person(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Person"]
    class_class_curie: ClassVar[str] = "peh:Person"
    class_name: ClassVar[str] = "Person"
    class_model_uri: ClassVar[URIRef] = PEH.Person

    id: Union[str, PersonId] = None
    recruited_in_project: Optional[Union[str, ProjectId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonId):
            self.id = PersonId(self.id)

        if self.recruited_in_project is not None and not isinstance(self.recruited_in_project, ProjectId):
            self.recruited_in_project = ProjectId(self.recruited_in_project)

        super().__post_init__(**kwargs)


@dataclass
class PersonGroup(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["PersonGroup"]
    class_class_curie: ClassVar[str] = "peh:PersonGroup"
    class_name: ClassVar[str] = "PersonGroup"
    class_model_uri: ClassVar[URIRef] = PEH.PersonGroup

    id: Union[str, PersonGroupId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PersonGroupId):
            self.id = PersonGroupId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Geolocation(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Geolocation"]
    class_class_curie: ClassVar[str] = "peh:Geolocation"
    class_name: ClassVar[str] = "Geolocation"
    class_model_uri: ClassVar[URIRef] = PEH.Geolocation

    id: Union[str, GeolocationId] = None
    location: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeolocationId):
            self.id = GeolocationId(self.id)

        if self.location is not None and not isinstance(self.location, str):
            self.location = str(self.location)

        super().__post_init__(**kwargs)


@dataclass
class Environment(StudyEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Environment"]
    class_class_curie: ClassVar[str] = "peh:Environment"
    class_name: ClassVar[str] = "Environment"
    class_model_uri: ClassVar[URIRef] = PEH.Environment

    id: Union[str, EnvironmentId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EnvironmentId):
            self.id = EnvironmentId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class Observation(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["Observation"]
    class_class_curie: ClassVar[str] = "peh:Observation"
    class_name: ClassVar[str] = "Observation"
    class_model_uri: ClassVar[URIRef] = PEH.Observation

    id: Union[str, ObservationId] = None
    observation_type: Optional[Union[str, "ObservationType"]] = None
    observation_design: Optional[Union[dict, "ObservationDesign"]] = None
    observation_result: Optional[Union[dict, "ObservationResult"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.observation_type is not None and not isinstance(self.observation_type, ObservationType):
            self.observation_type = ObservationType(self.observation_type)

        if self.observation_design is not None and not isinstance(self.observation_design, ObservationDesign):
            self.observation_design = ObservationDesign(**as_dict(self.observation_design))

        if self.observation_result is not None and not isinstance(self.observation_result, ObservationResult):
            self.observation_result = ObservationResult(**as_dict(self.observation_result))

        super().__post_init__(**kwargs)


@dataclass
class MetadataObservation(Observation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["MetadataObservation"]
    class_class_curie: ClassVar[str] = "peh:MetadataObservation"
    class_name: ClassVar[str] = "MetadataObservation"
    class_model_uri: ClassVar[URIRef] = PEH.MetadataObservation

    id: Union[str, MetadataObservationId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MetadataObservationId):
            self.id = MetadataObservationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class QuestionnaireObservation(Observation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["QuestionnaireObservation"]
    class_class_curie: ClassVar[str] = "peh:QuestionnaireObservation"
    class_name: ClassVar[str] = "QuestionnaireObservation"
    class_model_uri: ClassVar[URIRef] = PEH.QuestionnaireObservation

    id: Union[str, QuestionnaireObservationId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, QuestionnaireObservationId):
            self.id = QuestionnaireObservationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class SamplingObservation(Observation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["SamplingObservation"]
    class_class_curie: ClassVar[str] = "peh:SamplingObservation"
    class_name: ClassVar[str] = "SamplingObservation"
    class_model_uri: ClassVar[URIRef] = PEH.SamplingObservation

    id: Union[str, SamplingObservationId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SamplingObservationId):
            self.id = SamplingObservationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class GeospatialObservation(Observation):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["GeospatialObservation"]
    class_class_curie: ClassVar[str] = "peh:GeospatialObservation"
    class_name: ClassVar[str] = "GeospatialObservation"
    class_model_uri: ClassVar[URIRef] = PEH.GeospatialObservation

    id: Union[str, GeospatialObservationId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, GeospatialObservationId):
            self.id = GeospatialObservationId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ObservationDesign(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ObservationDesign"]
    class_class_curie: ClassVar[str] = "peh:ObservationDesign"
    class_name: ClassVar[str] = "ObservationDesign"
    class_model_uri: ClassVar[URIRef] = PEH.ObservationDesign

    observable_entity_property_sets: Optional[Union[Union[dict, "ObservableEntityPropertySet"], List[Union[dict, "ObservableEntityPropertySet"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.observable_entity_property_sets, list):
            self.observable_entity_property_sets = [self.observable_entity_property_sets] if self.observable_entity_property_sets is not None else []
        self.observable_entity_property_sets = [v if isinstance(v, ObservableEntityPropertySet) else ObservableEntityPropertySet(**as_dict(v)) for v in self.observable_entity_property_sets]

        super().__post_init__(**kwargs)


class MetadataDesign(ObservationDesign):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["MetadataDesign"]
    class_class_curie: ClassVar[str] = "peh:MetadataDesign"
    class_name: ClassVar[str] = "MetadataDesign"
    class_model_uri: ClassVar[URIRef] = PEH.MetadataDesign


class QuestionnaireDesign(ObservationDesign):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["QuestionnaireDesign"]
    class_class_curie: ClassVar[str] = "peh:QuestionnaireDesign"
    class_name: ClassVar[str] = "QuestionnaireDesign"
    class_model_uri: ClassVar[URIRef] = PEH.QuestionnaireDesign


class SamplingDesign(ObservationDesign):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["SamplingDesign"]
    class_class_curie: ClassVar[str] = "peh:SamplingDesign"
    class_name: ClassVar[str] = "SamplingDesign"
    class_model_uri: ClassVar[URIRef] = PEH.SamplingDesign


class GeospatialDesign(ObservationDesign):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["GeospatialDesign"]
    class_class_curie: ClassVar[str] = "peh:GeospatialDesign"
    class_name: ClassVar[str] = "GeospatialDesign"
    class_model_uri: ClassVar[URIRef] = PEH.GeospatialDesign


@dataclass
class ObservableEntityPropertySet(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ObservableEntityPropertySet"]
    class_class_curie: ClassVar[str] = "peh:ObservableEntityPropertySet"
    class_name: ClassVar[str] = "ObservableEntityPropertySet"
    class_model_uri: ClassVar[URIRef] = PEH.ObservableEntityPropertySet

    observable_entity_type: Optional[Union[str, "ObservableEntityType"]] = None
    observable_entity_id_list: Optional[Union[Union[str, StudyEntityId], List[Union[str, StudyEntityId]]]] = empty_list()
    observable_property_id_list: Optional[Union[Union[str, ObservablePropertyId], List[Union[str, ObservablePropertyId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.observable_entity_type is not None and not isinstance(self.observable_entity_type, ObservableEntityType):
            self.observable_entity_type = ObservableEntityType(self.observable_entity_type)

        if not isinstance(self.observable_entity_id_list, list):
            self.observable_entity_id_list = [self.observable_entity_id_list] if self.observable_entity_id_list is not None else []
        self.observable_entity_id_list = [v if isinstance(v, StudyEntityId) else StudyEntityId(v) for v in self.observable_entity_id_list]

        if not isinstance(self.observable_property_id_list, list):
            self.observable_property_id_list = [self.observable_property_id_list] if self.observable_property_id_list is not None else []
        self.observable_property_id_list = [v if isinstance(v, ObservablePropertyId) else ObservablePropertyId(v) for v in self.observable_property_id_list]

        super().__post_init__(**kwargs)


@dataclass
class ObservationResult(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ObservationResult"]
    class_class_curie: ClassVar[str] = "peh:ObservationResult"
    class_name: ClassVar[str] = "ObservationResult"
    class_model_uri: ClassVar[URIRef] = PEH.ObservationResult

    observed_values: Optional[Union[Union[dict, "ObservedValue"], List[Union[dict, "ObservedValue"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.observed_values, list):
            self.observed_values = [self.observed_values] if self.observed_values is not None else []
        self.observed_values = [v if isinstance(v, ObservedValue) else ObservedValue(**as_dict(v)) for v in self.observed_values]

        super().__post_init__(**kwargs)


class MetadataResult(ObservationResult):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["MetadataResult"]
    class_class_curie: ClassVar[str] = "peh:MetadataResult"
    class_name: ClassVar[str] = "MetadataResult"
    class_model_uri: ClassVar[URIRef] = PEH.MetadataResult


class QuestionnaireResult(ObservationResult):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["QuestionnaireResult"]
    class_class_curie: ClassVar[str] = "peh:QuestionnaireResult"
    class_name: ClassVar[str] = "QuestionnaireResult"
    class_model_uri: ClassVar[URIRef] = PEH.QuestionnaireResult


class SamplingResult(ObservationResult):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["SamplingResult"]
    class_class_curie: ClassVar[str] = "peh:SamplingResult"
    class_name: ClassVar[str] = "SamplingResult"
    class_model_uri: ClassVar[URIRef] = PEH.SamplingResult


class GeospatialResult(ObservationResult):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["GeospatialResult"]
    class_class_curie: ClassVar[str] = "peh:GeospatialResult"
    class_name: ClassVar[str] = "GeospatialResult"
    class_model_uri: ClassVar[URIRef] = PEH.GeospatialResult


@dataclass
class ObservedValue(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ObservedValue"]
    class_class_curie: ClassVar[str] = "peh:ObservedValue"
    class_name: ClassVar[str] = "ObservedValue"
    class_model_uri: ClassVar[URIRef] = PEH.ObservedValue

    observable_entity: Optional[Union[str, StudyEntityId]] = None
    observable_property: Optional[Union[str, ObservablePropertyId]] = None
    value: Optional[str] = None
    unit: Optional[Union[str, UnitId]] = None
    quality_data: Optional[Union[Union[dict, "QualityData"], List[Union[dict, "QualityData"]]]] = empty_list()
    provenance_data: Optional[Union[Union[dict, "ProvenanceData"], List[Union[dict, "ProvenanceData"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.observable_entity is not None and not isinstance(self.observable_entity, StudyEntityId):
            self.observable_entity = StudyEntityId(self.observable_entity)

        if self.observable_property is not None and not isinstance(self.observable_property, ObservablePropertyId):
            self.observable_property = ObservablePropertyId(self.observable_property)

        if self.value is not None and not isinstance(self.value, str):
            self.value = str(self.value)

        if self.unit is not None and not isinstance(self.unit, UnitId):
            self.unit = UnitId(self.unit)

        if not isinstance(self.quality_data, list):
            self.quality_data = [self.quality_data] if self.quality_data is not None else []
        self.quality_data = [v if isinstance(v, QualityData) else QualityData(**as_dict(v)) for v in self.quality_data]

        if not isinstance(self.provenance_data, list):
            self.provenance_data = [self.provenance_data] if self.provenance_data is not None else []
        self.provenance_data = [v if isinstance(v, ProvenanceData) else ProvenanceData(**as_dict(v)) for v in self.provenance_data]

        super().__post_init__(**kwargs)


@dataclass
class QualityData(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["QualityData"]
    class_class_curie: ClassVar[str] = "peh:QualityData"
    class_name: ClassVar[str] = "QualityData"
    class_model_uri: ClassVar[URIRef] = PEH.QualityData

    quality_context_key: Optional[str] = None
    quality_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.quality_context_key is not None and not isinstance(self.quality_context_key, str):
            self.quality_context_key = str(self.quality_context_key)

        if self.quality_value is not None and not isinstance(self.quality_value, str):
            self.quality_value = str(self.quality_value)

        super().__post_init__(**kwargs)


@dataclass
class ProvenanceData(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ProvenanceData"]
    class_class_curie: ClassVar[str] = "peh:ProvenanceData"
    class_name: ClassVar[str] = "ProvenanceData"
    class_model_uri: ClassVar[URIRef] = PEH.ProvenanceData

    provenance_context_key: Optional[str] = None
    provenance_value: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.provenance_context_key is not None and not isinstance(self.provenance_context_key, str):
            self.provenance_context_key = str(self.provenance_context_key)

        if self.provenance_value is not None and not isinstance(self.provenance_value, str):
            self.provenance_value = str(self.provenance_value)

        super().__post_init__(**kwargs)


@dataclass
class DataRequest(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["DataRequest"]
    class_class_curie: ClassVar[str] = "peh:DataRequest"
    class_name: ClassVar[str] = "DataRequest"
    class_model_uri: ClassVar[URIRef] = PEH.DataRequest

    id: Union[str, DataRequestId] = None
    contacts: Optional[Union[Union[dict, Contact], List[Union[dict, Contact]]]] = empty_list()
    request_properties: Optional[str] = None
    data_stakeholders: Optional[Union[Union[str, DataStakeholderId], List[Union[str, DataStakeholderId]]]] = empty_list()
    research_objectives: Optional[Union[Union[str, ResearchObjectiveId], List[Union[str, ResearchObjectiveId]]]] = empty_list()
    processing_actions: Optional[Union[Union[str, ProcessingActionId], List[Union[str, ProcessingActionId]]]] = empty_list()
    processing_steps: Optional[Union[Union[str, ProcessingStepId], List[Union[str, ProcessingStepId]]]] = empty_list()
    remark_on_content: Optional[str] = None
    remark_on_methodology: Optional[str] = None
    observed_entity_properties: Optional[Union[Union[dict, "ObservedEntityProperty"], List[Union[dict, "ObservedEntityProperty"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataRequestId):
            self.id = DataRequestId(self.id)

        if not isinstance(self.contacts, list):
            self.contacts = [self.contacts] if self.contacts is not None else []
        self.contacts = [v if isinstance(v, Contact) else Contact(**as_dict(v)) for v in self.contacts]

        if self.request_properties is not None and not isinstance(self.request_properties, str):
            self.request_properties = str(self.request_properties)

        if not isinstance(self.data_stakeholders, list):
            self.data_stakeholders = [self.data_stakeholders] if self.data_stakeholders is not None else []
        self.data_stakeholders = [v if isinstance(v, DataStakeholderId) else DataStakeholderId(v) for v in self.data_stakeholders]

        if not isinstance(self.research_objectives, list):
            self.research_objectives = [self.research_objectives] if self.research_objectives is not None else []
        self.research_objectives = [v if isinstance(v, ResearchObjectiveId) else ResearchObjectiveId(v) for v in self.research_objectives]

        if not isinstance(self.processing_actions, list):
            self.processing_actions = [self.processing_actions] if self.processing_actions is not None else []
        self.processing_actions = [v if isinstance(v, ProcessingActionId) else ProcessingActionId(v) for v in self.processing_actions]

        if not isinstance(self.processing_steps, list):
            self.processing_steps = [self.processing_steps] if self.processing_steps is not None else []
        self.processing_steps = [v if isinstance(v, ProcessingStepId) else ProcessingStepId(v) for v in self.processing_steps]

        if self.remark_on_content is not None and not isinstance(self.remark_on_content, str):
            self.remark_on_content = str(self.remark_on_content)

        if self.remark_on_methodology is not None and not isinstance(self.remark_on_methodology, str):
            self.remark_on_methodology = str(self.remark_on_methodology)

        if not isinstance(self.observed_entity_properties, list):
            self.observed_entity_properties = [self.observed_entity_properties] if self.observed_entity_properties is not None else []
        self.observed_entity_properties = [v if isinstance(v, ObservedEntityProperty) else ObservedEntityProperty(**as_dict(v)) for v in self.observed_entity_properties]

        super().__post_init__(**kwargs)


@dataclass
class ObservedEntityProperty(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ObservedEntityProperty"]
    class_class_curie: ClassVar[str] = "peh:ObservedEntityProperty"
    class_name: ClassVar[str] = "ObservedEntityProperty"
    class_model_uri: ClassVar[URIRef] = PEH.ObservedEntityProperty

    observable_entity: Optional[Union[str, StudyEntityId]] = None
    observable_property: Optional[Union[str, ObservablePropertyId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self.observable_entity is not None and not isinstance(self.observable_entity, StudyEntityId):
            self.observable_entity = StudyEntityId(self.observable_entity)

        if self.observable_property is not None and not isinstance(self.observable_property, ObservablePropertyId):
            self.observable_property = ObservablePropertyId(self.observable_property)

        super().__post_init__(**kwargs)


@dataclass
class DataStakeholder(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["DataStakeholder"]
    class_class_curie: ClassVar[str] = "peh:DataStakeholder"
    class_name: ClassVar[str] = "DataStakeholder"
    class_model_uri: ClassVar[URIRef] = PEH.DataStakeholder

    id: Union[str, DataStakeholderId] = None
    stakeholder: Optional[Union[str, StakeholderId]] = None
    data_roles: Optional[Union[Union[str, "DataRole"], List[Union[str, "DataRole"]]]] = empty_list()
    contacts: Optional[Union[Union[dict, Contact], List[Union[dict, Contact]]]] = empty_list()
    processing_description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, DataStakeholderId):
            self.id = DataStakeholderId(self.id)

        if self.stakeholder is not None and not isinstance(self.stakeholder, StakeholderId):
            self.stakeholder = StakeholderId(self.stakeholder)

        if not isinstance(self.data_roles, list):
            self.data_roles = [self.data_roles] if self.data_roles is not None else []
        self.data_roles = [v if isinstance(v, DataRole) else DataRole(v) for v in self.data_roles]

        if not isinstance(self.contacts, list):
            self.contacts = [self.contacts] if self.contacts is not None else []
        self.contacts = [v if isinstance(v, Contact) else Contact(**as_dict(v)) for v in self.contacts]

        if self.processing_description is not None and not isinstance(self.processing_description, str):
            self.processing_description = str(self.processing_description)

        super().__post_init__(**kwargs)


@dataclass
class ResearchObjective(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ResearchObjective"]
    class_class_curie: ClassVar[str] = "peh:ResearchObjective"
    class_name: ClassVar[str] = "ResearchObjective"
    class_model_uri: ClassVar[URIRef] = PEH.ResearchObjective

    id: Union[str, ResearchObjectiveId] = None
    objective_type: Optional[Union[str, "ObjectiveType"]] = None
    authors: Optional[Union[str, List[str]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ResearchObjectiveId):
            self.id = ResearchObjectiveId(self.id)

        if self.objective_type is not None and not isinstance(self.objective_type, ObjectiveType):
            self.objective_type = ObjectiveType(self.objective_type)

        if not isinstance(self.authors, list):
            self.authors = [self.authors] if self.authors is not None else []
        self.authors = [v if isinstance(v, str) else str(v) for v in self.authors]

        super().__post_init__(**kwargs)


@dataclass
class ProcessingAction(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ProcessingAction"]
    class_class_curie: ClassVar[str] = "peh:ProcessingAction"
    class_name: ClassVar[str] = "ProcessingAction"
    class_model_uri: ClassVar[URIRef] = PEH.ProcessingAction

    id: Union[str, ProcessingActionId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcessingActionId):
            self.id = ProcessingActionId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class ProcessingStep(NamedThing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["ProcessingStep"]
    class_class_curie: ClassVar[str] = "peh:ProcessingStep"
    class_name: ClassVar[str] = "ProcessingStep"
    class_model_uri: ClassVar[URIRef] = PEH.ProcessingStep

    id: Union[str, ProcessingStepId] = None
    start_date: Optional[Union[str, XSDDate]] = None
    delivery_date: Optional[Union[str, XSDDate]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ProcessingStepId):
            self.id = ProcessingStepId(self.id)

        if self.start_date is not None and not isinstance(self.start_date, XSDDate):
            self.start_date = XSDDate(self.start_date)

        if self.delivery_date is not None and not isinstance(self.delivery_date, XSDDate):
            self.delivery_date = XSDDate(self.delivery_date)

        super().__post_init__(**kwargs)


@dataclass
class DataExtract(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = PEH["DataExtract"]
    class_class_curie: ClassVar[str] = "peh:DataExtract"
    class_name: ClassVar[str] = "DataExtract"
    class_model_uri: ClassVar[URIRef] = PEH.DataExtract

    observed_values: Optional[Union[Union[dict, ObservedValue], List[Union[dict, ObservedValue]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.observed_values, list):
            self.observed_values = [self.observed_values] if self.observed_values is not None else []
        self.observed_values = [v if isinstance(v, ObservedValue) else ObservedValue(**as_dict(v)) for v in self.observed_values]

        super().__post_init__(**kwargs)


# Enumerations
class ValidationStatus(EnumDefinitionImpl):

    unvalidated = PermissibleValue(text="unvalidated")
    in_progress = PermissibleValue(text="in_progress")
    validated = PermissibleValue(text="validated")

    _defn = EnumDefinition(
        name="ValidationStatus",
    )

class IndicatorType(EnumDefinitionImpl):

    effectmarker = PermissibleValue(text="effectmarker")
    exposuremarker = PermissibleValue(text="exposuremarker")
    geomarker = PermissibleValue(text="geomarker")
    observation = PermissibleValue(text="observation")

    _defn = EnumDefinition(
        name="IndicatorType",
    )

class BioChemEntityLinkType(EnumDefinitionImpl):

    exact_match = PermissibleValue(text="exact_match")
    close_match = PermissibleValue(text="close_match")
    broader = PermissibleValue(text="broader")
    part_of = PermissibleValue(text="part_of")
    group_contains = PermissibleValue(text="group_contains")
    has_parent_compound = PermissibleValue(text="has_parent_compound")
    branched_version_of = PermissibleValue(text="branched_version_of")

    _defn = EnumDefinition(
        name="BioChemEntityLinkType",
    )

class ResearchPopulationType(EnumDefinitionImpl):

    general_population = PermissibleValue(text="general_population")
    person = PermissibleValue(text="person")
    newborn = PermissibleValue(text="newborn")
    adolescent = PermissibleValue(text="adolescent")
    mother = PermissibleValue(text="mother")
    parent = PermissibleValue(text="parent")
    pregnant_person = PermissibleValue(text="pregnant_person")
    household = PermissibleValue(text="household")

    _defn = EnumDefinition(
        name="ResearchPopulationType",
    )

class ObservableEntityType(EnumDefinitionImpl):

    person = PermissibleValue(text="person")
    persongroup = PermissibleValue(text="persongroup")
    environment = PermissibleValue(text="environment")
    location = PermissibleValue(text="location")
    study = PermissibleValue(text="study")
    dataset = PermissibleValue(text="dataset")
    sample = PermissibleValue(text="sample")

    _defn = EnumDefinition(
        name="ObservableEntityType",
    )

class ObservationType(EnumDefinitionImpl):

    sampling = PermissibleValue(text="sampling")
    questionnaire = PermissibleValue(text="questionnaire")
    geospatial = PermissibleValue(text="geospatial")
    metadata = PermissibleValue(text="metadata")

    _defn = EnumDefinition(
        name="ObservationType",
    )

class ObjectiveType(EnumDefinitionImpl):

    research_objective = PermissibleValue(text="research_objective")
    project_result = PermissibleValue(text="project_result")
    publication = PermissibleValue(text="publication")

    _defn = EnumDefinition(
        name="ObjectiveType",
    )

class LinkType(EnumDefinitionImpl):

    is_about = PermissibleValue(text="is_about")
    is_same_as = PermissibleValue(text="is_same_as")
    is_part_of = PermissibleValue(text="is_part_of")
    is_located_at = PermissibleValue(text="is_located_at")

    _defn = EnumDefinition(
        name="LinkType",
    )

class ContactRole(EnumDefinitionImpl):

    administrative = PermissibleValue(text="administrative")
    data = PermissibleValue(text="data")
    general = PermissibleValue(text="general")
    lead = PermissibleValue(text="lead")
    legal = PermissibleValue(text="legal")
    technical = PermissibleValue(text="technical")

    _defn = EnumDefinition(
        name="ContactRole",
    )

class ProjectRole(EnumDefinitionImpl):

    member = PermissibleValue(text="member")
    partner = PermissibleValue(text="partner")
    funding_partner = PermissibleValue(text="funding_partner")
    principal_investigator = PermissibleValue(text="principal_investigator")
    data_governance = PermissibleValue(text="data_governance")
    data_controller = PermissibleValue(text="data_controller")
    data_processor = PermissibleValue(text="data_processor")
    data_user = PermissibleValue(text="data_user")

    _defn = EnumDefinition(
        name="ProjectRole",
    )

class StudyRole(EnumDefinitionImpl):

    funding_partner = PermissibleValue(text="funding_partner")
    principal_investigator = PermissibleValue(text="principal_investigator")
    data_controller = PermissibleValue(text="data_controller")
    data_processor = PermissibleValue(text="data_processor")
    data_user = PermissibleValue(text="data_user")

    _defn = EnumDefinition(
        name="StudyRole",
    )

class DataRole(EnumDefinitionImpl):

    main_stakeholder = PermissibleValue(text="main_stakeholder")
    supplying_data_controller = PermissibleValue(text="supplying_data_controller")
    receiving_data_controller = PermissibleValue(text="receiving_data_controller")
    external_data_controller = PermissibleValue(text="external_data_controller")

    _defn = EnumDefinition(
        name="DataRole",
    )

class QudtUnit(EnumDefinitionImpl):

    _defn = EnumDefinition(
        name="QudtUnit",
    )

class QudtQuantityKind(EnumDefinitionImpl):

    MassConcentration = PermissibleValue(
        text="MassConcentration",
        meaning=QUDTQK["MassConcentration"])
    Period = PermissibleValue(
        text="Period",
        meaning=QUDTQK["Period"])

    _defn = EnumDefinition(
        name="QudtQuantityKind",
    )

# Slots
class slots:
    pass

slots.id = Slot(uri=SCHEMA.identifier, name="id", curie=SCHEMA.curie('identifier'),
                   model_uri=PEH.id, domain=None, range=URIRef)

slots.unique_name = Slot(uri=PEH.unique_name, name="unique_name", curie=PEH.curie('unique_name'),
                   model_uri=PEH.unique_name, domain=None, range=Optional[str])

slots.name = Slot(uri=SCHEMA.name, name="name", curie=SCHEMA.curie('name'),
                   model_uri=PEH.name, domain=None, range=Optional[str])

slots.description = Slot(uri=SCHEMA.description, name="description", curie=SCHEMA.curie('description'),
                   model_uri=PEH.description, domain=None, range=Optional[str])

slots.label = Slot(uri=RDFS.label, name="label", curie=RDFS.curie('label'),
                   model_uri=PEH.label, domain=None, range=Optional[str])

slots.remark = Slot(uri=PEH.remark, name="remark", curie=PEH.curie('remark'),
                   model_uri=PEH.remark, domain=None, range=Optional[str])

slots.orcid = Slot(uri=PEH.orcid, name="orcid", curie=PEH.curie('orcid'),
                   model_uri=PEH.orcid, domain=None, range=Optional[str])

slots.rorid = Slot(uri=PEH.rorid, name="rorid", curie=PEH.curie('rorid'),
                   model_uri=PEH.rorid, domain=None, range=Optional[str])

slots.alias = Slot(uri=PEH.alias, name="alias", curie=PEH.curie('alias'),
                   model_uri=PEH.alias, domain=None, range=Optional[str])

slots.aliases = Slot(uri=PEH.aliases, name="aliases", curie=PEH.curie('aliases'),
                   model_uri=PEH.aliases, domain=None, range=Optional[Union[str, List[str]]])

slots.context_aliases = Slot(uri=PEH.context_aliases, name="context_aliases", curie=PEH.curie('context_aliases'),
                   model_uri=PEH.context_aliases, domain=None, range=Optional[Union[Union[dict, ContextAlias], List[Union[dict, ContextAlias]]]])

slots.context = Slot(uri=PEH.context, name="context", curie=PEH.curie('context'),
                   model_uri=PEH.context, domain=None, range=Optional[Union[str, NamedThingId]])

slots.translations = Slot(uri=PEH.translations, name="translations", curie=PEH.curie('translations'),
                   model_uri=PEH.translations, domain=None, range=Optional[Union[Union[dict, Translation], List[Union[dict, Translation]]]])

slots.property_name = Slot(uri=PEH.property_name, name="property_name", curie=PEH.curie('property_name'),
                   model_uri=PEH.property_name, domain=None, range=Optional[str])

slots.language = Slot(uri=PEH.language, name="language", curie=PEH.curie('language'),
                   model_uri=PEH.language, domain=None, range=Optional[str])

slots.translated_value = Slot(uri=PEH.translated_value, name="translated_value", curie=PEH.curie('translated_value'),
                   model_uri=PEH.translated_value, domain=None, range=Optional[str])

slots.validation_history = Slot(uri=PEH.validation_history, name="validation_history", curie=PEH.curie('validation_history'),
                   model_uri=PEH.validation_history, domain=None, range=Optional[Union[Union[dict, ValidationHistoryRecord], List[Union[dict, ValidationHistoryRecord]]]])

slots.units = Slot(uri=PEH.units, name="units", curie=PEH.curie('units'),
                   model_uri=PEH.units, domain=None, range=Optional[Union[Dict[Union[str, UnitId], Union[dict, Unit]], List[Union[dict, Unit]]]])

slots.same_unit_as = Slot(uri=PEH.same_unit_as, name="same_unit_as", curie=PEH.curie('same_unit_as'),
                   model_uri=PEH.same_unit_as, domain=None, range=Optional[Union[str, "QudtUnit"]])

slots.quantity_kind = Slot(uri=PEH.quantity_kind, name="quantity_kind", curie=PEH.curie('quantity_kind'),
                   model_uri=PEH.quantity_kind, domain=None, range=Optional[Union[str, "QudtQuantityKind"]])

slots.grouping = Slot(uri=PEH.grouping, name="grouping", curie=PEH.curie('grouping'),
                   model_uri=PEH.grouping, domain=None, range=Optional[Union[str, GroupingId]])

slots.groupings = Slot(uri=PEH.groupings, name="groupings", curie=PEH.curie('groupings'),
                   model_uri=PEH.groupings, domain=None, range=Optional[Union[Dict[Union[str, GroupingId], Union[dict, Grouping]], List[Union[dict, Grouping]]]])

slots.grouping_id_list = Slot(uri=PEH.grouping_id_list, name="grouping_id_list", curie=PEH.curie('grouping_id_list'),
                   model_uri=PEH.grouping_id_list, domain=None, range=Optional[Union[Union[str, GroupingId], List[Union[str, GroupingId]]]])

slots.parent_grouping_id_list = Slot(uri=PEH.parent_grouping_id_list, name="parent_grouping_id_list", curie=PEH.curie('parent_grouping_id_list'),
                   model_uri=PEH.parent_grouping_id_list, domain=None, range=Optional[Union[Union[str, GroupingId], List[Union[str, GroupingId]]]])

slots.biochemidentifiers = Slot(uri=PEH.biochemidentifiers, name="biochemidentifiers", curie=PEH.curie('biochemidentifiers'),
                   model_uri=PEH.biochemidentifiers, domain=None, range=Optional[Union[Union[dict, BioChemIdentifier], List[Union[dict, BioChemIdentifier]]]])

slots.biochementities = Slot(uri=PEH.biochementities, name="biochementities", curie=PEH.curie('biochementities'),
                   model_uri=PEH.biochementities, domain=None, range=Optional[Union[Dict[Union[str, BioChemEntityId], Union[dict, BioChemEntity]], List[Union[dict, BioChemEntity]]]])

slots.indicators = Slot(uri=PEH.indicators, name="indicators", curie=PEH.curie('indicators'),
                   model_uri=PEH.indicators, domain=None, range=Optional[Union[Dict[Union[str, IndicatorId], Union[dict, Indicator]], List[Union[dict, Indicator]]]])

slots.web_uri = Slot(uri=PEH.web_uri, name="web_uri", curie=PEH.curie('web_uri'),
                   model_uri=PEH.web_uri, domain=None, range=Optional[str])

slots.identifier_schema = Slot(uri=PEH.identifier_schema, name="identifier_schema", curie=PEH.curie('identifier_schema'),
                   model_uri=PEH.identifier_schema, domain=None, range=Optional[Union[str, BioChemIdentifierSchemaId]])

slots.identifier_code = Slot(uri=PEH.identifier_code, name="identifier_code", curie=PEH.curie('identifier_code'),
                   model_uri=PEH.identifier_code, domain=None, range=Optional[str])

slots.current_validation_status = Slot(uri=PEH.current_validation_status, name="current_validation_status", curie=PEH.curie('current_validation_status'),
                   model_uri=PEH.current_validation_status, domain=None, range=Optional[Union[str, "ValidationStatus"]])

slots.validation_datetime = Slot(uri=PEH.validation_datetime, name="validation_datetime", curie=PEH.curie('validation_datetime'),
                   model_uri=PEH.validation_datetime, domain=None, range=Optional[Union[str, XSDDateTime]])

slots.validation_status = Slot(uri=PEH.validation_status, name="validation_status", curie=PEH.curie('validation_status'),
                   model_uri=PEH.validation_status, domain=None, range=Optional[Union[str, "ValidationStatus"]])

slots.validation_actor = Slot(uri=PEH.validation_actor, name="validation_actor", curie=PEH.curie('validation_actor'),
                   model_uri=PEH.validation_actor, domain=None, range=Optional[str])

slots.validation_institute = Slot(uri=PEH.validation_institute, name="validation_institute", curie=PEH.curie('validation_institute'),
                   model_uri=PEH.validation_institute, domain=None, range=Optional[str])

slots.validation_remark = Slot(uri=PEH.validation_remark, name="validation_remark", curie=PEH.curie('validation_remark'),
                   model_uri=PEH.validation_remark, domain=None, range=Optional[str])

slots.sort_order = Slot(uri=PEH.sort_order, name="sort_order", curie=PEH.curie('sort_order'),
                   model_uri=PEH.sort_order, domain=None, range=Optional[Decimal])

slots.aggregation_target = Slot(uri=PEH.aggregation_target, name="aggregation_target", curie=PEH.curie('aggregation_target'),
                   model_uri=PEH.aggregation_target, domain=None, range=Optional[Union[bool, Bool]])

slots.parent_matrix = Slot(uri=PEH.parent_matrix, name="parent_matrix", curie=PEH.curie('parent_matrix'),
                   model_uri=PEH.parent_matrix, domain=None, range=Optional[Union[str, MatrixId]])

slots.indicator_type = Slot(uri=PEH.indicator_type, name="indicator_type", curie=PEH.curie('indicator_type'),
                   model_uri=PEH.indicator_type, domain=None, range=Optional[Union[str, "IndicatorType"]])

slots.matrices = Slot(uri=PEH.matrices, name="matrices", curie=PEH.curie('matrices'),
                   model_uri=PEH.matrices, domain=None, range=Optional[Union[Dict[Union[str, MatrixId], Union[dict, Matrix]], List[Union[dict, Matrix]]]])

slots.matrix = Slot(uri=PEH.matrix, name="matrix", curie=PEH.curie('matrix'),
                   model_uri=PEH.matrix, domain=None, range=Optional[Union[str, MatrixId]])

slots.constraints = Slot(uri=PEH.constraints, name="constraints", curie=PEH.curie('constraints'),
                   model_uri=PEH.constraints, domain=None, range=Optional[Union[str, List[str]]])

slots.relevant_observable_entity_types = Slot(uri=PEH.relevant_observable_entity_types, name="relevant_observable_entity_types", curie=PEH.curie('relevant_observable_entity_types'),
                   model_uri=PEH.relevant_observable_entity_types, domain=None, range=Optional[Union[Union[str, "ObservableEntityType"], List[Union[str, "ObservableEntityType"]]]])

slots.biochementity_links = Slot(uri=PEH.biochementity_links, name="biochementity_links", curie=PEH.curie('biochementity_links'),
                   model_uri=PEH.biochementity_links, domain=None, range=Optional[Union[Union[dict, BioChemEntityLink], List[Union[dict, BioChemEntityLink]]]])

slots.biochementity_linktype = Slot(uri=PEH.biochementity_linktype, name="biochementity_linktype", curie=PEH.curie('biochementity_linktype'),
                   model_uri=PEH.biochementity_linktype, domain=None, range=Optional[Union[str, "BioChemEntityLinkType"]])

slots.biochementity = Slot(uri=PEH.biochementity, name="biochementity", curie=PEH.curie('biochementity'),
                   model_uri=PEH.biochementity, domain=None, range=Optional[Union[str, BioChemEntityId]])

slots.categorical = Slot(uri=PEH.categorical, name="categorical", curie=PEH.curie('categorical'),
                   model_uri=PEH.categorical, domain=None, range=Optional[Union[bool, Bool]])

slots.multivalued = Slot(uri=PEH.multivalued, name="multivalued", curie=PEH.curie('multivalued'),
                   model_uri=PEH.multivalued, domain=None, range=Optional[Union[bool, Bool]])

slots.required = Slot(uri=PEH.required, name="required", curie=PEH.curie('required'),
                   model_uri=PEH.required, domain=None, range=Optional[Union[bool, Bool]])

slots.abstract = Slot(uri=PEH.abstract, name="abstract", curie=PEH.curie('abstract'),
                   model_uri=PEH.abstract, domain=None, range=Optional[Union[bool, Bool]])

slots.value_type = Slot(uri=PEH.value_type, name="value_type", curie=PEH.curie('value_type'),
                   model_uri=PEH.value_type, domain=None, range=Optional[str])

slots.value_metadata = Slot(uri=PEH.value_metadata, name="value_metadata", curie=PEH.curie('value_metadata'),
                   model_uri=PEH.value_metadata, domain=None, range=Optional[Union[Union[dict, ObservablePropertyMetadataElement], List[Union[dict, ObservablePropertyMetadataElement]]]])

slots.value_options = Slot(uri=PEH.value_options, name="value_options", curie=PEH.curie('value_options'),
                   model_uri=PEH.value_options, domain=None, range=Optional[Union[Union[dict, ObservablePropertyValueOption], List[Union[dict, ObservablePropertyValueOption]]]])

slots.default_immutable = Slot(uri=PEH.default_immutable, name="default_immutable", curie=PEH.curie('default_immutable'),
                   model_uri=PEH.default_immutable, domain=None, range=Optional[Union[bool, Bool]])

slots.default_significantdecimals = Slot(uri=PEH.default_significantdecimals, name="default_significantdecimals", curie=PEH.curie('default_significantdecimals'),
                   model_uri=PEH.default_significantdecimals, domain=None, range=Optional[int])

slots.default_unit = Slot(uri=PEH.default_unit, name="default_unit", curie=PEH.curie('default_unit'),
                   model_uri=PEH.default_unit, domain=None, range=Optional[str])

slots.relevant_observation_types = Slot(uri=PEH.relevant_observation_types, name="relevant_observation_types", curie=PEH.curie('relevant_observation_types'),
                   model_uri=PEH.relevant_observation_types, domain=None, range=Optional[Union[Union[str, "ObservationType"], List[Union[str, "ObservationType"]]]])

slots.indicator = Slot(uri=PEH.indicator, name="indicator", curie=PEH.curie('indicator'),
                   model_uri=PEH.indicator, domain=None, range=Optional[Union[str, IndicatorId]])

slots.calculation_design = Slot(uri=PEH.calculation_design, name="calculation_design", curie=PEH.curie('calculation_design'),
                   model_uri=PEH.calculation_design, domain=None, range=Optional[Union[dict, CalculationDesign]])

slots.validation_design = Slot(uri=PEH.validation_design, name="validation_design", curie=PEH.curie('validation_design'),
                   model_uri=PEH.validation_design, domain=None, range=Optional[Union[dict, ValidationDesign]])

slots.formula = Slot(uri=PEH.formula, name="formula", curie=PEH.curie('formula'),
                   model_uri=PEH.formula, domain=None, range=Optional[str])

slots.conditional = Slot(uri=PEH.conditional, name="conditional", curie=PEH.curie('conditional'),
                   model_uri=PEH.conditional, domain=None, range=Optional[str])

slots.field = Slot(uri=PEH.field, name="field", curie=PEH.curie('field'),
                   model_uri=PEH.field, domain=None, range=Optional[Union[str, ObservablePropertyMetadataFieldId]])

slots.key = Slot(uri=PEH.key, name="key", curie=PEH.curie('key'),
                   model_uri=PEH.key, domain=None, range=Optional[str])

slots.value = Slot(uri=PEH.value, name="value", curie=PEH.curie('value'),
                   model_uri=PEH.value, domain=None, range=Optional[str])

slots.metadata_fields = Slot(uri=PEH.metadata_fields, name="metadata_fields", curie=PEH.curie('metadata_fields'),
                   model_uri=PEH.metadata_fields, domain=None, range=Optional[Union[Dict[Union[str, ObservablePropertyMetadataFieldId], Union[dict, ObservablePropertyMetadataField]], List[Union[dict, ObservablePropertyMetadataField]]]])

slots.stakeholders = Slot(uri=PEH.stakeholders, name="stakeholders", curie=PEH.curie('stakeholders'),
                   model_uri=PEH.stakeholders, domain=None, range=Optional[Union[Dict[Union[str, StakeholderId], Union[dict, Stakeholder]], List[Union[dict, Stakeholder]]]])

slots.project_id_list = Slot(uri=PEH.project_id_list, name="project_id_list", curie=PEH.curie('project_id_list'),
                   model_uri=PEH.project_id_list, domain=None, range=Optional[Union[Union[str, ProjectId], List[Union[str, ProjectId]]]])

slots.projects = Slot(uri=PEH.projects, name="projects", curie=PEH.curie('projects'),
                   model_uri=PEH.projects, domain=None, range=Optional[Union[Dict[Union[str, ProjectId], Union[dict, Project]], List[Union[dict, Project]]]])

slots.geographic_scope = Slot(uri=PEH.geographic_scope, name="geographic_scope", curie=PEH.curie('geographic_scope'),
                   model_uri=PEH.geographic_scope, domain=None, range=Optional[str])

slots.project = Slot(uri=SCHEMA.ResearchProject, name="project", curie=SCHEMA.curie('ResearchProject'),
                   model_uri=PEH.project, domain=None, range=Optional[str])

slots.default_language = Slot(uri=PEH.default_language, name="default_language", curie=PEH.curie('default_language'),
                   model_uri=PEH.default_language, domain=None, range=Optional[str])

slots.stakeholder = Slot(uri=PEH.stakeholder, name="stakeholder", curie=PEH.curie('stakeholder'),
                   model_uri=PEH.stakeholder, domain=None, range=Optional[Union[str, StakeholderId]])

slots.project_stakeholders = Slot(uri=PEH.project_stakeholders, name="project_stakeholders", curie=PEH.curie('project_stakeholders'),
                   model_uri=PEH.project_stakeholders, domain=None, range=Optional[Union[Union[dict, ProjectStakeholder], List[Union[dict, ProjectStakeholder]]]])

slots.study_id_list = Slot(uri=PEH.study_id_list, name="study_id_list", curie=PEH.curie('study_id_list'),
                   model_uri=PEH.study_id_list, domain=None, range=Optional[Union[Union[str, StudyId], List[Union[str, StudyId]]]])

slots.studies = Slot(uri=PEH.studies, name="studies", curie=PEH.curie('studies'),
                   model_uri=PEH.studies, domain=None, range=Optional[Union[Dict[Union[str, StudyId], Union[dict, Study]], List[Union[dict, Study]]]])

slots.project_roles = Slot(uri=PEH.project_roles, name="project_roles", curie=PEH.curie('project_roles'),
                   model_uri=PEH.project_roles, domain=None, range=Optional[Union[Union[str, "ProjectRole"], List[Union[str, "ProjectRole"]]]])

slots.study_stakeholders = Slot(uri=PEH.study_stakeholders, name="study_stakeholders", curie=PEH.curie('study_stakeholders'),
                   model_uri=PEH.study_stakeholders, domain=None, range=Optional[Union[Union[dict, StudyStakeholder], List[Union[dict, StudyStakeholder]]]])

slots.research_population_type = Slot(uri=PEH.research_population_type, name="research_population_type", curie=PEH.curie('research_population_type'),
                   model_uri=PEH.research_population_type, domain=None, range=Optional[Union[str, "ResearchPopulationType"]])

slots.study_roles = Slot(uri=PEH.study_roles, name="study_roles", curie=PEH.curie('study_roles'),
                   model_uri=PEH.study_roles, domain=None, range=Optional[Union[Union[str, "StudyRole"], List[Union[str, "StudyRole"]]]])

slots.timepoint_id_list = Slot(uri=PEH.timepoint_id_list, name="timepoint_id_list", curie=PEH.curie('timepoint_id_list'),
                   model_uri=PEH.timepoint_id_list, domain=None, range=Optional[Union[Union[str, TimepointId], List[Union[str, TimepointId]]]])

slots.timepoints = Slot(uri=PEH.timepoints, name="timepoints", curie=PEH.curie('timepoints'),
                   model_uri=PEH.timepoints, domain=None, range=Optional[Union[Dict[Union[str, TimepointId], Union[dict, Timepoint]], List[Union[dict, Timepoint]]]])

slots.study_entities = Slot(uri=PEH.study_entities, name="study_entities", curie=PEH.curie('study_entities'),
                   model_uri=PEH.study_entities, domain=None, range=Optional[Union[Union[str, StudyEntityId], List[Union[str, StudyEntityId]]]])

slots.observations = Slot(uri=PEH.observations, name="observations", curie=PEH.curie('observations'),
                   model_uri=PEH.observations, domain=None, range=Optional[Union[Dict[Union[str, ObservationId], Union[dict, Observation]], List[Union[dict, Observation]]]])

slots.study_entity_links = Slot(uri=PEH.study_entity_links, name="study_entity_links", curie=PEH.curie('study_entity_links'),
                   model_uri=PEH.study_entity_links, domain=None, range=Optional[Union[Union[dict, StudyEntityLink], List[Union[dict, StudyEntityLink]]]])

slots.linktype = Slot(uri=PEH.linktype, name="linktype", curie=PEH.curie('linktype'),
                   model_uri=PEH.linktype, domain=None, range=Optional[Union[str, "LinkType"]])

slots.study_entity = Slot(uri=PEH.study_entity, name="study_entity", curie=PEH.curie('study_entity'),
                   model_uri=PEH.study_entity, domain=None, range=Optional[Union[str, StudyEntityId]])

slots.recruited_in_project = Slot(uri=PEH.recruited_in_project, name="recruited_in_project", curie=PEH.curie('recruited_in_project'),
                   model_uri=PEH.recruited_in_project, domain=None, range=Optional[Union[str, ProjectId]])

slots.sampled_in_project = Slot(uri=PEH.sampled_in_project, name="sampled_in_project", curie=PEH.curie('sampled_in_project'),
                   model_uri=PEH.sampled_in_project, domain=None, range=Optional[Union[str, ProjectId]])

slots.physical_label = Slot(uri=PEH.physical_label, name="physical_label", curie=PEH.curie('physical_label'),
                   model_uri=PEH.physical_label, domain=None, range=Optional[str])

slots.location = Slot(uri=PEH.location, name="location", curie=PEH.curie('location'),
                   model_uri=PEH.location, domain=None, range=Optional[str])

slots.observation_type = Slot(uri=PEH.observation_type, name="observation_type", curie=PEH.curie('observation_type'),
                   model_uri=PEH.observation_type, domain=None, range=Optional[Union[str, "ObservationType"]])

slots.observation_design = Slot(uri=PEH.observation_design, name="observation_design", curie=PEH.curie('observation_design'),
                   model_uri=PEH.observation_design, domain=None, range=Optional[Union[dict, ObservationDesign]])

slots.observable_entity_property_sets = Slot(uri=PEH.observable_entity_property_sets, name="observable_entity_property_sets", curie=PEH.curie('observable_entity_property_sets'),
                   model_uri=PEH.observable_entity_property_sets, domain=None, range=Optional[Union[Union[dict, ObservableEntityPropertySet], List[Union[dict, ObservableEntityPropertySet]]]])

slots.observation_result = Slot(uri=PEH.observation_result, name="observation_result", curie=PEH.curie('observation_result'),
                   model_uri=PEH.observation_result, domain=None, range=Optional[Union[dict, ObservationResult]])

slots.observable_entity_type = Slot(uri=PEH.observable_entity_type, name="observable_entity_type", curie=PEH.curie('observable_entity_type'),
                   model_uri=PEH.observable_entity_type, domain=None, range=Optional[Union[str, "ObservableEntityType"]])

slots.observable_entity_id_list = Slot(uri=PEH.observable_entity_id_list, name="observable_entity_id_list", curie=PEH.curie('observable_entity_id_list'),
                   model_uri=PEH.observable_entity_id_list, domain=None, range=Optional[Union[Union[str, StudyEntityId], List[Union[str, StudyEntityId]]]])

slots.observable_entities = Slot(uri=PEH.observable_entities, name="observable_entities", curie=PEH.curie('observable_entities'),
                   model_uri=PEH.observable_entities, domain=None, range=Optional[Union[Dict[Union[str, StudyEntityId], Union[dict, StudyEntity]], List[Union[dict, StudyEntity]]]])

slots.observable_entity = Slot(uri=PEH.observable_entity, name="observable_entity", curie=PEH.curie('observable_entity'),
                   model_uri=PEH.observable_entity, domain=None, range=Optional[Union[str, StudyEntityId]])

slots.observable_property_id_list = Slot(uri=PEH.observable_property_id_list, name="observable_property_id_list", curie=PEH.curie('observable_property_id_list'),
                   model_uri=PEH.observable_property_id_list, domain=None, range=Optional[Union[Union[str, ObservablePropertyId], List[Union[str, ObservablePropertyId]]]])

slots.observable_properties = Slot(uri=PEH.observable_properties, name="observable_properties", curie=PEH.curie('observable_properties'),
                   model_uri=PEH.observable_properties, domain=None, range=Optional[Union[Dict[Union[str, ObservablePropertyId], Union[dict, ObservableProperty]], List[Union[dict, ObservableProperty]]]])

slots.observable_property = Slot(uri=PEH.observable_property, name="observable_property", curie=PEH.curie('observable_property'),
                   model_uri=PEH.observable_property, domain=None, range=Optional[Union[str, ObservablePropertyId]])

slots.observed_values = Slot(uri=PEH.observed_values, name="observed_values", curie=PEH.curie('observed_values'),
                   model_uri=PEH.observed_values, domain=None, range=Optional[Union[Union[dict, ObservedValue], List[Union[dict, ObservedValue]]]])

slots.unit = Slot(uri=PEH.unit, name="unit", curie=PEH.curie('unit'),
                   model_uri=PEH.unit, domain=None, range=Optional[Union[str, UnitId]])

slots.quality_data = Slot(uri=PEH.quality_data, name="quality_data", curie=PEH.curie('quality_data'),
                   model_uri=PEH.quality_data, domain=None, range=Optional[Union[Union[dict, QualityData], List[Union[dict, QualityData]]]])

slots.quality_context_key = Slot(uri=PEH.quality_context_key, name="quality_context_key", curie=PEH.curie('quality_context_key'),
                   model_uri=PEH.quality_context_key, domain=None, range=Optional[str])

slots.quality_value = Slot(uri=PEH.quality_value, name="quality_value", curie=PEH.curie('quality_value'),
                   model_uri=PEH.quality_value, domain=None, range=Optional[str])

slots.provenance_data = Slot(uri=PEH.provenance_data, name="provenance_data", curie=PEH.curie('provenance_data'),
                   model_uri=PEH.provenance_data, domain=None, range=Optional[Union[Union[dict, ProvenanceData], List[Union[dict, ProvenanceData]]]])

slots.provenance_context_key = Slot(uri=PEH.provenance_context_key, name="provenance_context_key", curie=PEH.curie('provenance_context_key'),
                   model_uri=PEH.provenance_context_key, domain=None, range=Optional[str])

slots.provenance_value = Slot(uri=PEH.provenance_value, name="provenance_value", curie=PEH.curie('provenance_value'),
                   model_uri=PEH.provenance_value, domain=None, range=Optional[str])

slots.data_roles = Slot(uri=PEH.data_roles, name="data_roles", curie=PEH.curie('data_roles'),
                   model_uri=PEH.data_roles, domain=None, range=Optional[Union[Union[str, "DataRole"], List[Union[str, "DataRole"]]]])

slots.contacts = Slot(uri=PEH.contacts, name="contacts", curie=PEH.curie('contacts'),
                   model_uri=PEH.contacts, domain=None, range=Optional[Union[Union[dict, Contact], List[Union[dict, Contact]]]])

slots.contact_roles = Slot(uri=PEH.contact_roles, name="contact_roles", curie=PEH.curie('contact_roles'),
                   model_uri=PEH.contact_roles, domain=None, range=Optional[Union[Union[str, "ContactRole"], List[Union[str, "ContactRole"]]]])

slots.contact_email = Slot(uri=PEH.contact_email, name="contact_email", curie=PEH.curie('contact_email'),
                   model_uri=PEH.contact_email, domain=None, range=Optional[str])

slots.contact_phone = Slot(uri=PEH.contact_phone, name="contact_phone", curie=PEH.curie('contact_phone'),
                   model_uri=PEH.contact_phone, domain=None, range=Optional[str])

slots.request_properties = Slot(uri=PEH.request_properties, name="request_properties", curie=PEH.curie('request_properties'),
                   model_uri=PEH.request_properties, domain=None, range=Optional[str])

slots.data_stakeholders = Slot(uri=PEH.data_stakeholders, name="data_stakeholders", curie=PEH.curie('data_stakeholders'),
                   model_uri=PEH.data_stakeholders, domain=None, range=Optional[Union[Union[str, DataStakeholderId], List[Union[str, DataStakeholderId]]]])

slots.research_objectives = Slot(uri=PEH.research_objectives, name="research_objectives", curie=PEH.curie('research_objectives'),
                   model_uri=PEH.research_objectives, domain=None, range=Optional[Union[Union[str, ResearchObjectiveId], List[Union[str, ResearchObjectiveId]]]])

slots.processing_actions = Slot(uri=PEH.processing_actions, name="processing_actions", curie=PEH.curie('processing_actions'),
                   model_uri=PEH.processing_actions, domain=None, range=Optional[Union[Union[str, ProcessingActionId], List[Union[str, ProcessingActionId]]]])

slots.processing_steps = Slot(uri=PEH.processing_steps, name="processing_steps", curie=PEH.curie('processing_steps'),
                   model_uri=PEH.processing_steps, domain=None, range=Optional[Union[Union[str, ProcessingStepId], List[Union[str, ProcessingStepId]]]])

slots.remark_on_content = Slot(uri=PEH.remark_on_content, name="remark_on_content", curie=PEH.curie('remark_on_content'),
                   model_uri=PEH.remark_on_content, domain=None, range=Optional[str])

slots.remark_on_methodology = Slot(uri=PEH.remark_on_methodology, name="remark_on_methodology", curie=PEH.curie('remark_on_methodology'),
                   model_uri=PEH.remark_on_methodology, domain=None, range=Optional[str])

slots.observed_entity_properties = Slot(uri=PEH.observed_entity_properties, name="observed_entity_properties", curie=PEH.curie('observed_entity_properties'),
                   model_uri=PEH.observed_entity_properties, domain=None, range=Optional[Union[Union[dict, ObservedEntityProperty], List[Union[dict, ObservedEntityProperty]]]])

slots.processing_description = Slot(uri=PEH.processing_description, name="processing_description", curie=PEH.curie('processing_description'),
                   model_uri=PEH.processing_description, domain=None, range=Optional[str])

slots.objective_type = Slot(uri=PEH.objective_type, name="objective_type", curie=PEH.curie('objective_type'),
                   model_uri=PEH.objective_type, domain=None, range=Optional[Union[str, "ObjectiveType"]])

slots.authors = Slot(uri=PEH.authors, name="authors", curie=PEH.curie('authors'),
                   model_uri=PEH.authors, domain=None, range=Optional[Union[str, List[str]]])

slots.start_date = Slot(uri=PEH.start_date, name="start_date", curie=PEH.curie('start_date'),
                   model_uri=PEH.start_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.end_date = Slot(uri=PEH.end_date, name="end_date", curie=PEH.curie('end_date'),
                   model_uri=PEH.end_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.delivery_date = Slot(uri=PEH.delivery_date, name="delivery_date", curie=PEH.curie('delivery_date'),
                   model_uri=PEH.delivery_date, domain=None, range=Optional[Union[str, XSDDate]])

slots.collection_date = Slot(uri=PEH.collection_date, name="collection_date", curie=PEH.curie('collection_date'),
                   model_uri=PEH.collection_date, domain=None, range=Optional[Union[str, XSDDate]])
