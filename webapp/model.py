annoclass = {
    "item_title": "annoclass",
    "resource_methods": ["GET", "POST", "DELETE"],
    "item_methods": ["GET", "PATCH", "PUT", "DELETE"],
    "schema": {
        "name": {"type": "string", "required": True},
        "category": {"type": "string", "required": True},
        "name_zh": {"type": "string", "required": True},
        "movable": {"type": "boolean", "required": True},
        "attributes": {
            "type": "list",
            "schema": {
                "type": "objectid",
                "data_relation": {
                    "resource": "annoattr",
                    "field": "_id",
                    "embeddable": True,
                },
            },
        },
        "example_img_paths": {
            "type": "list",
            "schema": {
                "type": "string"
            }
        }
    },
}

annoattr = {
    "item_title": "annoattr",
    "resource_methods": ["GET", "POST", "DELETE"],
    "item_methods": ["GET", "PATCH", "PUT", "DELETE"],
    "schema": {
        "name": {"type": "string", "required": True},
        "name_zh": {"type": "string", "required": True},
        "items": {
            "type": "list",
            "schema": {
                "type": "dict",
                "schema": {
                    "name": {"type": "string", "required": True},
                    "name_zh": {"type": "string", "required": True},
                    "example_img_paths": {
                        "type": "list",
                        "schema": {
                            "type": "string"
                        }
                    }
                }
            }
        },
        "attr_type": {"type": "string", "required": True},
    },
}
