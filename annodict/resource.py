from dataclasses import dataclass, field
from pathlib import Path

from jinja2 import Template
import requests
import pandas as pd


@dataclass
class AnnoItem:
    """Attribute Item"""

    name: str
    name_zh: str
    example_img_paths: list[str] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict):
        """Create AnnoItem from dict"""
        return AnnoItem(
            name=d["name"],
            name_zh=d["name_zh"],
            example_img_paths=d.get("example_img_paths", []),
        )


@dataclass
class AnnoAttr:
    """Attribute"""

    name: str
    name_zh: str
    attr_type: str
    items: list[AnnoItem] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict):
        """Create AnnoAttr from dict"""
        return AnnoAttr(
            name=d["name"],
            name_zh=d["name_zh"],
            attr_type=d["attr_type"],
            items=[AnnoItem.from_dict(i) for i in d["items"]],
        )


@dataclass
class AnnoClass:
    """Class"""

    name: str
    name_zh: str
    category: str
    movable: bool
    attributes: list[AnnoAttr] = field(default_factory=list)
    example_img_paths: list[str] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict):
        """Create AnnoClass from dict"""
        return AnnoClass(
            name=d["name"],
            name_zh=d["name_zh"],
            category=d["category"],
            movable=d["movable"],
            attributes=[AnnoAttr.from_dict(a) for a in d["attributes"]],
            example_img_paths=d.get("example_img_paths", []),
        )

    @staticmethod
    def from_objectid(objid: str, api_server: str):
        """use requests.get to get the object from restful API:
        GET /annoclass/<objid>?embedded={"attributes":1}
        """
        resp = requests.get(
            f'{api_server}/annoclass/{objid}?embedded={{"attributes":1}}'
        )
        if resp.status_code != 200:
            raise ValueError(f"Failed to get annoclass: {objid}")
        return AnnoClass.from_dict(resp.json())


@dataclass
class AnnoScene:
    """Scene"""

    name: str
    desc: str
    classes: list[AnnoClass] = field(default_factory=list)

    @staticmethod
    def from_objectid(objid: str, api_server: str):
        """use requests.get to get the object from restful API:
        GET /annoscene/<objid>
        """
        resp = requests.get(f"{api_server}/annoscene/{objid}")
        if resp.status_code != 200:
            raise ValueError(f"Failed to get annoscene: {objid}")
        return AnnoScene.from_dict(resp.json(), api_server=api_server)

    @staticmethod
    def from_dict(d: dict, api_server: str = None):
        """Create AnnoScene from dict"""
        return AnnoScene(
            name=d["name"],
            desc=d.get("desc", ""),
            classes=[
                AnnoClass.from_dict(c)
                if isinstance(c, dict)
                else AnnoClass.from_objectid(c, api_server)
                for c in d["classes"]
            ],
        )

    def export_html(self) -> str:
        """Export as html string"""
        template = Template(Path("templates/scene.html").read_text())
        return template.render(
            annoscene=self,
        )

    def export_csv(self) -> pd.DataFrame:
        """Export as csv"""
        pass
