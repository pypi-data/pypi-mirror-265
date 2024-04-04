from dataclasses import dataclass
from functools import lru_cache
from typing import List, Optional

from . import traverse
from .enums import DimensionType, MemberType
from .models import Annotations


@dataclass(eq=False, frozen=True, order=False)
class PublicSchema:
    name: str
    locales: List[str]
    default_locale: str
    annotations: Annotations
    cubes: List["PublicCube"]

    @classmethod
    def from_entity(
        cls,
        entity: traverse.SchemaTraverser,
        roles: List[str] = [],
        locale: Optional[str] = None,
    ):
        """Generates a dataclass-schema object describing this entity."""
        default_locale = entity.schema.default_locale
        locale = default_locale if locale is None else locale
        return cls(
            name=entity.schema.name,
            locales=sorted(entity.get_locale_available()),
            default_locale=default_locale,
            cubes=[
                PublicCube.from_entity(item, locale)
                for item in entity.cube_map.values()
                if item.visible and item.is_authorized(roles)
            ],
            annotations=dict(entity.schema.annotations),
        )


@dataclass(eq=False, frozen=True, order=False)
class PublicCube:
    name: str
    caption: str
    annotations: Annotations
    dimensions: List["PublicDimension"]
    measures: List["PublicMeasure"]

    @classmethod
    @lru_cache(maxsize=256)
    def from_entity(cls, entity: traverse.CubeTraverser, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            dimensions=[
                PublicDimension.from_entity(item, locale) for item in entity.dimensions
            ],
            measures=[
                PublicMeasure.from_entity(item, locale) for item in entity.measures
            ],
            annotations=dict(entity.annotations),
        )


@dataclass(eq=False, frozen=True, order=False)
class PublicMeasure:
    name: str
    caption: str
    aggregator: str
    annotations: Annotations
    attached: List["PublicMeasure"]

    @classmethod
    def from_entity(cls, entity: traverse.AnyMeasure, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            aggregator=str(entity.aggregator),
            annotations=dict(entity.annotations),
            attached=[
                cls.from_entity(item, locale) for item in entity.submeasures.values()
            ],
        )


@dataclass(eq=False, frozen=True, order=False)
class PublicDimension:
    name: str
    caption: str
    type: DimensionType
    annotations: Annotations
    hierarchies: List["PublicHierarchy"]
    default_hierarchy: str

    @classmethod
    def from_entity(cls, entity: traverse.DimensionTraverser, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            type=entity.dim_type,
            annotations=dict(entity.annotations),
            hierarchies=[
                PublicHierarchy.from_entity(item, locale) for item in entity.hierarchies
            ],
            default_hierarchy=entity._entity.default_hierarchy,
        )


@dataclass(eq=False, frozen=True, order=False)
class PublicHierarchy:
    name: str
    caption: str
    annotations: Annotations
    levels: List["PublicLevel"]

    @classmethod
    def from_entity(cls, entity: traverse.HierarchyTraverser, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            annotations=dict(entity.annotations),
            levels=[PublicLevel.from_entity(item, locale) for item in entity.levels],
        )


@dataclass(eq=False, frozen=True, order=False)
class PublicLevel:
    name: str
    caption: str
    depth: int
    annotations: Annotations
    properties: List["PublicProperty"]

    @classmethod
    def from_entity(cls, entity: traverse.LevelTraverser, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            depth=entity.depth,
            annotations=dict(entity.annotations),
            properties=[
                PublicProperty.from_entity(item, locale) for item in entity.properties
            ],
        )


@dataclass(eq=False, frozen=True, order=False)
class PublicProperty:
    name: str
    caption: str
    type: MemberType
    annotations: Annotations

    @classmethod
    def from_entity(cls, entity: traverse.PropertyTraverser, locale: str):
        """Generates a dataclass-schema object describing this entity."""
        return cls(
            name=entity.name,
            caption=entity.get_caption(locale),
            type=entity.key_type,
            annotations=dict(entity.annotations),
        )
