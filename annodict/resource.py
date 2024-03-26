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
    _id: str = None

    @staticmethod
    def from_dict(d: dict):
        """Create AnnoItem from dict"""
        return AnnoItem(
            _id=d["_id"],
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
    _id: str = None

    @staticmethod
    def from_dict(d: dict, embedded: bool = False):
        """Create AnnoAttr from dict"""
        annoattr = AnnoAttr(
            _id=d["_id"],
            name=d["name"],
            name_zh=d["name_zh"],
            attr_type=d["attr_type"],
            items=[AnnoItem.from_dict(i) if embedded else i for i in d["items"]],
        )
        return annoattr
    
    @staticmethod
    def from_name(name: str, api_server: str, embedded: bool = False):
        query_str = f'{api_server}/annoattr/?where={{"name":"{name}"}}'
        if embedded:
            query_str += "&embedded={\"items\":1}"
        resp = requests.get(query_str)
        if resp.status_code != 200:
            raise ValueError(f"Failed to get annoattr with name: {name}")
        j = resp.json()
        assert j["_meta"]["total"] == 1, f"There should only be 1 record with attr name: {name}"
        return AnnoAttr.from_dict(j["_items"][0], embedded=embedded)


@dataclass
class AnnoClass:
    """Class"""

    name: str
    name_zh: str
    category: str
    time_varying: bool
    attributes: list[AnnoAttr] = field(default_factory=list)
    example_img_paths: list[str] = field(default_factory=list)
    _id: str = None

    @staticmethod
    def from_dict(d: dict, embedded: bool = False):
        """Create AnnoClass from dict"""
        annoclass = AnnoClass(
            _id=d["_id"],
            name=d["name"],
            name_zh=d["name_zh"],
            category=d["category"],
            time_varying=d["time_varying"],
            attributes=[AnnoAttr.from_dict(a) if embedded else a for a in d["attributes"]],
            example_img_paths=d.get("example_img_paths", []),
        )
        return annoclass

    @staticmethod
    def from_objectid(objid: str, api_server: str, embedded: bool = False):
        """use requests.get to get the object from restful API:
        GET /annoclass/<objid>?embedded={"attributes":1}
        """
        query_str = f'{api_server}/annoclass/{objid}'
        if embedded:
            query_str += "&embedded={\"attributes\":1}"
        resp = requests.get(query_str)
        if resp.status_code != 200:
            raise ValueError(f"Failed to get annoclass: {objid}")
        return AnnoClass.from_dict(resp.json(), embedded=embedded)
    
    @staticmethod
    def from_name(name: str, api_server: str):
        query_str = f'{api_server}/annoclass/?where={{"name":"{name}"}}'
        resp = requests.get(query_str)
        if resp.status_code != 200:
            raise ValueError(f"Failed to get annoclass with name: {name}")
        j = resp.json()
        assert j["_meta"]["total"] == 1, f"There should only be 1 record with class name: {name}"
        return AnnoClass.from_dict(j["_items"][0])


@dataclass
class AnnoScene:
    """Scene"""

    name: str
    desc: str
    classes: list[AnnoClass] = field(default_factory=list)

    @staticmethod
    def from_objectid(objid: str, api_server: str, embedded: bool = False):
        """use requests.get to get the object from restful API:
        GET /annoscene/<objid>
        """
        resp = requests.get(f"{api_server}/annoscene/{objid}")
        if resp.status_code != 200:
            raise ValueError(f"Failed to get annoscene: {objid}")
        return AnnoScene.from_dict(resp.json(), api_server=api_server, embedded=embedded)

    @staticmethod
    def from_dict(d: dict, api_server: str = None, embedded: bool = False):
        """Create AnnoScene from dict"""
        return AnnoScene(
            name=d["name"],
            desc=d.get("desc", ""),
            classes=[
                AnnoClass.from_dict(c, embedded=embedded)
                if isinstance(c, dict)
                else AnnoClass.from_objectid(c, api_server)
                for c in d["classes"]
            ],
        )

    # TODO: needs to be modified due to the refactoring of annoitem.
    def export_html(self, path: Path, template_path: str = "templates/scene.html") -> str:
        """Export as html string"""
        template = Template(Path(template_path).read_text())
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
