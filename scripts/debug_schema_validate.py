from cerberus import Validator


schema = {
    "name": {"type": "string", "required": True},
    "desc": {"type": "string"},
    "classes": {
        "type": "list",
        "required": True,
        "schema": {
            "type": "dict",
            "schema": {
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
                            "name": {"type": "string", "required": True},
                            "name_zh": {"type": "string", "required": True},
                            "attr_type": {"type": "string", "required": True},
                            "items": {
                                "type": "list",
                                "required": True,
                                "schema": {
                                    "type": "dict",
                                    "schema": {
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

d = {
    "name": "test snapshot",
    "classes": [
        {
            "name": "class.parking.parking_slot",
            "name_zh": "停车位",
            "category": "泊车设施",
            "attributes": [
                {
                    "name": "attr.parking.parking_slot.type",
                    "name_zh": "车位类型",
                    "attr_type": "enum",
                    "items": [
                        {
                            "name": "attr.parking.parking_slot.type.regular",
                            "name_zh": "正常车位",
                            "example_img_paths": []
                        },
                        {
                            "name": "attr.parking.parking_slot.type.charging",
                            "name_zh": "充电车位/新能源车位",
                            "example_img_paths": [
                                "https://s2.loli.net/2023/07/27/SJohyEquMVsPe6H.png"
                            ]
                        },
                    ]
                },
                {
                    "name": "attr.parking.parking_slot.direction",
                    "name_zh": "车位方向",
                    "attr_type": "enum",
                    "items": [
                        {
                            "name": "attr.parking.parking_slot.parking_slot.direction.parallel",
                            "name_zh": "平行车位",
                            "example_img_paths": [
                                "https://s2.loli.net/2023/07/27/M5z4stBAdRkoCUN.png"
                            ]
                        },
                    ]
                },
                {
                    "name": "attr.parking.parking_slot.is_mechanical",
                    "name_zh": "是否为机械车位",
                    "attr_type": "bool",
                    "items": [
                        {
                            "name": "attr.parking.parking_slot.is_mechanical.true",
                            "name_zh": "是"
                        },
                        {
                            "name": "attr.parking.parking_slot.is_mechanical.false",
                            "name_zh": "否"
                        }
                    ]
                }
            ],
            "time_varying": False,
            "example_img_paths": [],
        }
    ],
}

# schema = {
#     "name": {"type": "string"},
#     "rows": {
#         "type": "list",
#         "schema": {
#             "type": "dict",
#             "schema": {
#                 "sku": {"type": "string"}, 
#                 "price": {"type": "integer"}
#             },
#         },
#     }
# }
# d = {"name": "aaabbbccc", "rows": [{"sku": "KT123", "price": 100}]}

v = Validator(schema)
v.validate(d)
