import argparse
from typing import List
from pathlib import Path

from loguru import logger
import pandas as pd

from annodict.restful import post_docs


parser = argparse.ArgumentParser()
parser.add_argument("-d", "--dict", type=Path, required=True)
parser.add_argument(
    "-s", "--api-server", required=True, default="http://localhost:5100"
)


def main(args):
    annoattrs = pd.read_excel(args.dict, engine="openpyxl", sheet_name="attr")
    annoclasses = pd.read_excel(args.dict, engine="openpyxl", sheet_name="class")
    annoclass_annoattr = pd.read_excel(
        args.dict, engine="openpyxl", sheet_name="class_attr"
    )
    annoclasses = pd.merge(
        annoclasses, annoclass_annoattr, on="class_value", how="left"
    )

    # insert attrs
    name2attr = insert_attrs(annoattrs, args.api_server)

    # insert classes
    insert_classes(annoclasses, name2attr, args.api_server)


def insert_attrs(annoattrs: pd.DataFrame, api_server: str):
    name2attr = {}
    for name, items in annoattrs.groupby("attr_name"):
        assert items.attr_name_zh.nunique() == 1
        assert items.attr_type.nunique() == 1
        attr_name_zh, attr_type = items[["attr_name_zh", "attr_type"]].values[0]

        attritem_ids = insert_attritems(name, attr_type, items, api_server)
        _attr = {
            "name": name,
            "name_zh": attr_name_zh,
            "attr_type": attr_type,
            "items": attritem_ids,
        }
        attr_objid = post_docs("annoattr", [_attr], api_server)[0]
        _attr.update({"_id": attr_objid})

        name2attr.update({name: _attr})
        logger.info(f"Inserted attribute: {name} ({attr_objid})" "")

    return name2attr


def insert_attritems(attr_name: str, attr_type: str, items: pd.DataFrame, api_server: str) -> dict:
    """Insert attriems into DB through POST method

    Parameters
    ----------
    attr_name : str
        attribute's name
    attr_type : str
        attributes's type
    items : pd.DataFrame
        list of items that associated to the attribute
        schema: {
            "name": {"type": "string", "required": True},
            "name_zh": {"type": "string", "required": True},
            "example_img_paths": {
                "type": "list",
                "schema": {
                    "type": "string"
                }
            }
        }
    api_server : str
        the REST API server

    Returns
    -------
    dict
        a mapping dict that maps each attritem's name to AnnoItem object
    """
    if attr_type == "enum":
        attritems = [
            {"name": i[0], "name_zh": i[1], "example_img_paths": [] if pd.isnull(i[2]) else i[2].split(",")}
            for i in items[["attr_value", "attr_desc", "example_img_paths"]].values.tolist()
        ]

    elif attr_type == "bool":
        assert len(items) == 1
        attritems = [
            {"name": f"{attr_name}.true", "name_zh": "是"},
            {"name": f"{attr_name}.false", "name_zh": "否"},
        ]
    else:
        raise ValueError("Unknown attribute type: {}".format(attr_type))
    
    attritem_ids = post_docs("annoattritem", attritems, api_server)
    return attritem_ids


def insert_classes(annoclasses: pd.DataFrame, name2attr: dict, api_server: str):
    """for each annoclass in annoclasses, if it has no attr, insert it directly;
    otherwise, find the related attrs in name2attr and assign them to the field `attributes`,
    then insert it as a class.
    """
    for name, annoclass in annoclasses.groupby("class_value"):
        assert annoclass.class_desc.nunique() == 1
        name_zh, category, time_varying, example_img_paths_str = annoclass[
            ["class_desc", "category", "time_varying", "example_img_paths"]
        ].values[0]

        attr_objids = []
        example_img_paths = []
        if not annoclass.attr.isnull().all():
            # iterate all the attr values and find the corresponding _id in name2attr using comprehension exp
            # then set the result to attr_objids
            attr_objids = [
                name2attr[attr_name]["_id"]
                for attr_name in annoclass.attr.values
                if attr_name in name2attr
            ]
        
        if not annoclass.example_img_paths.isnull().all():
            example_img_paths = example_img_paths_str.split(",")

        class_objid = post_docs(
            "annoclass",
            [
                {
                    "name": name,
                    "name_zh": name_zh,
                    "category": category,
                    "attributes": attr_objids,
                    "time_varying": time_varying,
                    "example_img_paths": example_img_paths,
                }
            ],
            api_server,
        )[0]
        logger.info(f"Inserted class: {name} ({class_objid})")


if __name__ == "__main__":
    main(parser.parse_args())
