import argparse
from pathlib import Path
from typing import List, Dict

import requests
from loguru import logger

from annodict.resource import AnnoClass, AnnoAttr


def main(args):
    # read scene json
    src_scene_json = read_scene_json(args.json_path)
    dst_scene_json = {
        "name": src_scene_json["name"],
        "desc": src_scene_json["desc"],
        "classes": prepare_classes_or_tags(src_scene_json["classes"], args.endpoint_url),
        "tags": prepare_classes_or_tags(src_scene_json["tags"], args.endpoint_url),
    }
    a = 100


def prepare_classes_or_tags(classes_or_tags: List[Dict], endpoint_url: str) -> List[Dict]:
    full_info = []
    # iterate over all classes of scene json
    for cls_or_tag in classes_or_tags:
        # fetch class info though REST API
        obj = AnnoClass.from_name(cls_or_tag["name"], endpoint_url)
        
        if "attributes" in cls_or_tag:
            obj.attributes = prepare_attributes(cls_or_tag["attributes"], endpoint_url)
        else:
            obj.attributes = []

        full_info.append(obj.as_dict())

    return full_info


def prepare_attributes(attributes: List[Dict], endpoint_url: str) -> List[Dict]:
    full_info = []
    for attr in attributes:
        # fetch attribute info though REST API
        obj = AnnoAttr.from_name(attr["name"], endpoint_url, embedded=True)
        obj.items = [i for i in obj.items if i["name"] in attr.get("items", [])]
        full_info.append(obj.as_dict())
    return full_info


def read_scene_json(path: Path):
    with open(path, "r") as f:
        return f.read()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-path", type=Path, required=True)
    parser.add_argument("--endpoint-url", default="http://localhost:5100")
    main(parser.parse_args())
