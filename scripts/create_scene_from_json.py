import argparse
import json
from pathlib import Path
from typing import List, Dict
from dataclasses import asdict

import requests
from loguru import logger

from annodict.resource import AnnoClass, AnnoAttr
from annodict.restful import post_docs


def main(args):
    # read scene json
    src_scene_json = read_scene_json(args.json_path)
    dst_scene_json = {
        "name": src_scene_json["name"],
        "desc": src_scene_json["desc"],
        "classes": prepare_classes_or_tags(src_scene_json["classes"], args.endpoint_url),
        "tags": prepare_classes_or_tags(src_scene_json["tags"], args.endpoint_url),
    }
    post_docs("annoscene", [dst_scene_json], args.endpoint_url)
    a = 100


def prepare_classes_or_tags(classes_or_tags: List[Dict], endpoint_url: str) -> List[Dict]:
    full_info = []
    for cls_or_tag in classes_or_tags:
        obj = AnnoClass.from_name(cls_or_tag["name"], endpoint_url) # fetch info through REST API
        
        if "attributes" in cls_or_tag:
            obj.attributes = prepare_attributes(cls_or_tag["attributes"], endpoint_url)
        else:
            obj.attributes = []

        full_info.append(asdict(obj))

    return full_info


def prepare_attributes(attributes: List[Dict], endpoint_url: str) -> List[Dict]:
    full_info = []
    for attr in attributes:
        obj = AnnoAttr.from_name(attr["name"], endpoint_url, embedded=True) # fetch info through REST API
        if "items" in attr:
            obj.items = [i for i in obj.items if i.name in attr["items"]]
        full_info.append(asdict(obj))
    return full_info


def read_scene_json(path: Path):
    with open(path, "r") as f:
        return json.load(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-path", type=Path, required=True)
    parser.add_argument("--endpoint-url", default="http://localhost:5100")
    main(parser.parse_args())
