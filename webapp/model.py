annoscene = {
    "item_title": "annoscene",
    "resource_methods": ["GET", "POST", "DELETE"],
    "item_methods": ["GET", "PATCH", "PUT", "DELETE"],
    "schema": {
        "name": {"type": "string", "required": True},
        "desc": {"type": "string"},
        "classes": {
            "type": "list",
            "required": True,
            "schema": {
                "type": "dict",
                "schema": {
                    "_id": {"type": "string", "required": True},
                    "name": {"type": "string", "required": True},
                    "category": {"type": "string", "required": True},
                    "name_zh": {"type": "string", "required": True},
                    "time_varying": {"type": "boolean", "required": True},
                    "example_img_paths": {"type": "list", "schema": {"type": "string"}},
                    "attributes": {
                        "type": "list",
                        "schema": {
                            "type": "dict",
                            "schema": {
                                "_id": {"type": "string", "required": True},
                                "name": {"type": "string", "required": True},
                                "name_zh": {"type": "string", "required": True},
                                "attr_type": {"type": "string", "required": True},
                                "items": {
                                    "type": "list",
                                    "required": True,
                                    "schema": {
                                        "type": "dict",
                                        "schema": {
                                            "_id": {"type": "string", "required": True},
                                            "name": {"type": "string", "required": True},
                                            "name_zh": {"type": "string", "required": True},
                                            "example_img_paths": {
                                                "type": "list",
                                                "schema": {"type": "string"},
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    }
                }
            }
        }
    }
}

annoclass = {
    "item_title": "annoclass",
    "resource_methods": ["GET", "POST", "DELETE"],
    "item_methods": ["GET", "PATCH", "PUT", "DELETE"],
    "schema": {
        "name": {"type": "string", "required": True},
        "category": {"type": "string", "required": True},
        "name_zh": {"type": "string", "required": True},
        "time_varying": {"type": "boolean", "required": True},
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
                "type": "objectid",
                "data_relation": {
                    "resource": "annoattritem",
                    "field": "_id",
                    "embeddable": True,
                },
            }
        },
        "attr_type": {"type": "string", "required": True},
    },
}

annoattritem = {
    "item_title": "annoattritem",
    "resource_methods": ["GET", "POST", "DELETE"],
    "item_methods": ["GET", "PATCH", "PUT", "DELETE"],
    "schema": {
        "name": {"type": "string", "required": True},
        "name_zh": {"type": "string", "required": True},
        "example_img_paths": {
            "type": "list",
            "schema": {
                "type": "string"
            }
        }
    },
}
