from dataclasses import dataclass, field

@dataclass
class AnnoAttr:
    """Attribute
    """
    name: str
    attr_type: str
    values: list[str]
    descs: list[str]


@dataclass
class AnnoAffi:
    """Affiliation
    """
    name: str
    values: list[str]
    descs: list[str]


@dataclass
class AnnoClass:
    """Class
    """
    name: str
    category: str
    desc: str
    movable: bool
    attributes: list[AnnoAttr] = field(default_factory=list)
    parts: list[AnnoAffi] = field(default_factory=list)


@dataclass
class AnnoScene:
    """Scene
    """
    name: str
    desc: str
    classes: list[AnnoClass] = field(default_factory=list)
