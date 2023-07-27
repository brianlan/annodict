from dataclasses import dataclass, field

@dataclass
class AnnoItem:
    """Attribute Item
    """
    name: str
    name_zh: str
    example_img_paths: list[str] = field(default_factory=list)


@dataclass
class AnnoAttr:
    """Attribute
    """
    name: str
    name_zh: str
    attr_type: str
    items: list[AnnoItem] = field(default_factory=list)


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
    name_zh: str
    category: str
    movable: bool
    attributes: list[AnnoAttr] = field(default_factory=list)
    example_img_paths: list[str] = field(default_factory=list)


@dataclass
class AnnoScene:
    """Scene
    """
    name: str
    desc: str
    classes: list[AnnoClass] = field(default_factory=list)
