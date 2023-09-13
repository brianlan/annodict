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
                "type": "objectid",
                "data_relation": {
                    "resource": "annoclass",
                    "field": "_id",
                    "embeddable": True,
                },
            },
        },
        # TODO: the number of attrs of a class in a scene could vary from the 
        #       number of attrs of the same class in another scene or the original dict
        
        # "selected_attritems": {
        #     "type": "dict",
        #     "schema": {
        #         "class_id": "objectid",
        #         "selected_attr": {
        #             "type": "list",
        #             "schema": {
                        
        #             }
        #         }
        #     }
        # }
    },
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
