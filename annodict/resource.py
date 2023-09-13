from dataclasses import dataclass, field, asdict
from pathlib import Path

from jinja2 import Template
import requests
import pandas as pd
import numpy as np


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
    time_varying: bool
    attributes: list[AnnoAttr] = field(default_factory=list)
    example_img_paths: list[str] = field(default_factory=list)

    @staticmethod
    def from_dict(d: dict):
        """Create AnnoClass from dict"""
        return AnnoClass(
            name=d["name"],
            name_zh=d["name_zh"],
            category=d["category"],
            time_varying=d["time_varying"],
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

    # TODO: needs to be modified due to the refactoring of annoitem.
    def export_html(self, path: Path) -> str:
        """Export as html string"""
        template = Template(Path("templates/scene.html").read_text())
        html = template.render(annoscene=self)
        with open(path, "w") as f:
            f.write(html)

    # TODO: needs to be modified due to the refactoring of annoitem.
    def export_csv(self, path: Path) -> pd.DataFrame:
        """Export as csv
        -----------------
        check the number of attributes for each class,
        obtain the Cartesian product of the items of each attribute
        """
        out = []
        for cls in self.classes:
            if len(cls.attributes) == 0:
                out.append(
                    pd.DataFrame(
                        {
                            "标注场景": [self.name,],
                            "简介": [self.desc,],
                            "所属": [cls.category,],
                            "大类名称": [cls.name_zh,],
                            "小类名称": [cls.name_zh],
                            "随时间可变": [cls.time_varying,],
                        }
                    )
                )
            elif len(cls.attributes) == 1:
                attr = cls.attributes[0]
                _tmp = pd.DataFrame(
                        {
                            "标注场景": self.name,
                            "简介": self.desc,
                            "所属": cls.category,
                            "大类名称": cls.name_zh,
                            "随时间可变": cls.time_varying,
                            "items": attr.items,
                        }
                    ).explode("items")
                _tmp.loc[:, "小类名称"] = _tmp["items"].map(lambda x: f"{attr.name_zh}({x.name_zh})" if attr.attr_type == 'bool' else x.name_zh)
                _tmp.drop(columns=['items'], inplace=True)
                out.append(_tmp)
            else:
                merged = pd.DataFrame.from_dict([asdict(item) for item in cls.attributes[0].items])
                if cls.attributes[0].attr_type == 'bool':
                    cur.loc[:, "name_zh"] = cls.attributes[0].name_zh + '(' + cur.name_zh + ')'
                for i in range(1, len(cls.attributes)):
                    cur = pd.DataFrame.from_dict([asdict(item) for item in cls.attributes[i].items])
                    if cls.attributes[i].attr_type == 'bool':
                        cur.loc[:, "name_zh"] = cls.attributes[i].name_zh + '(' + cur.name_zh + ')'
                    merged = pd.merge(merged[['name_zh']], cur[['name_zh']], how='cross')
                    merged['name_zh'] = merged['name_zh_x'] + '-' + merged['name_zh_y']
                    merged.drop(columns=['name_zh_x', 'name_zh_y'], inplace=True)
                merged.loc[:, "标注场景"] = self.name
                merged.loc[:, "简介"] = self.desc
                merged.loc[:, "所属"] = cls.category
                merged.loc[:, "大类名称"] = cls.name_zh
                merged.loc[:, "小类名称"] = merged.name_zh
                merged.loc[:, "随时间可变"] = cls.time_varying
                merged.drop(columns=['name_zh'], inplace=True)
                out.append(merged)
        pd.concat(out, ignore_index=True).to_csv(path, encoding='utf_8_sig', index=False)
