function remove_unnecessary_keys(obj, keysToRemove) {
    let newObj = Array.isArray(obj) ? [] : {};

    for (let key in obj) {
        if (keysToRemove.includes(key)) {
            continue;
        } else if (typeof obj[key] === "object" && obj[key] !== null) {
            newObj[key] = remove_unnecessary_keys(obj[key], keysToRemove);
        } else {
            newObj[key] = obj[key];
        }
    }

    return newObj;
}

function remove_unchecked_attritems(annoclass, attritem_check_state) {
    // function that remove the unchecked attritems from annoclass
    // `annoclass` is an object, attritem_check_state is an object
    //             annoclass contains a field attributes which is a list of object
    //             each attr in attributes has a field called items which is a list of object
    // `attritem_check_state` (key-value pair, where key is _id, value is boolean)
    // check whether item._id is true in attritem_check_state (key-value pair, where key is _id, value is boolean)
    // remove the unchecked item from attr of annoclass
    // return the annoclass
    let new_annoclass = JSON.parse(JSON.stringify(annoclass));  // deep copy
    new_annoclass.attributes = new_annoclass.attributes.map(function (attr) {
        attr.items = attr.items.filter(function (item) {
            return attritem_check_state[item._id];
        });
        return attr;
    });

    // remove attr if attr.items is empty
    new_annoclass.attributes = new_annoclass.attributes.filter(function (attr) {
        return attr.items.length > 0;
    });
    
    return new_annoclass;
}

let new_annoscene = new Vue({
    el: '#new_annoscene',
    data: {
        scene_name: undefined,
        scene_desc: undefined,
        selected_classes_or_tags: [],
        attritem_check_state: {},
        class_dict: {},
        tag_dict: {},
        full_dict: {},
        show: {},
        cur_category: undefined,
        cur_idx_in_category: undefined,
    },
    mounted: function () {
        this.fetch_full_dict();
    },
    computed: {
        selected_class_ids: function () {
            return this.selected_classes_or_tags.map(x => x._id);
        }
    },
    methods: {
        fetch_full_dict: async function() {
            let self = this;

            const responses = await Promise.all([
                // Fetch annoclass
                axios.get('/annoclass?embedded={"attributes":1}&max_results=200')
                .then(async function (response) {
                    self.class_dict = await response.data._items.reduce(async (accPromise, x) => {
                        x['source'] = 'annoclass';
                        let acc = await accPromise;

                        // fetch annoattritems
                        await Promise.all(x.attributes.map(async function(attr) {
                            let item_ids = '"' + attr.items.join('","') + '"';
                            let result = await axios.get(`/annoattritem?where={"_id": {"$in": [${item_ids}]}}`);
                            attr.items = result.data._items;
                        }));

                        // If the category does not exist in the accumulator object, create an empty array for it
                        if (!acc[x.category]) {
                            acc[x.category] = [];
                        }

                        // Push the annoclass to the corresponding category array
                        acc[x.category].push(x);

                        // Return the updated accumulator object
                        return acc;

                    }, Promise.resolve({}));

                    response.data._items.map(function (x) {
                        for (let i in x.attributes) {
                            self.$set(self.show, x.name + "-" + x.attributes[i].name, false);

                            for (let j in x.attributes[i].items) {
                                self.$set(self.attritem_check_state, x.attributes[i].items[j]._id, true);  // default set all the attritem_check_state to be true
                            }
                        }
                    });
                })
                .catch(function (error) {
                    alert(JSON.stringify(error));
                }),

                // Fetch annotag
                axios.get('/annotag?embedded={"attributes":1}&max_results=200')
                .then(async function (response) {
                    self.tag_dict = await response.data._items.reduce(async (accPromise, x) => {
                        x['source'] = 'annotag';
                        let acc = await accPromise;

                        // fetch annoattritems
                        await Promise.all(x.attributes.map(async function(attr) {
                            let item_ids = '"' + attr.items.join('","') + '"';
                            let result = await axios.get(`/annoattritem?where={"_id": {"$in": [${item_ids}]}}`);
                            attr.items = result.data._items;
                        }));

                        // If the category does not exist in the accumulator object, create an empty array for it
                        if (!acc[x.category]) {
                            acc[x.category] = [];
                        }

                        // Push the annoclass to the corresponding category array
                        acc[x.category].push(x);

                        // Return the updated accumulator object
                        return acc;

                    }, Promise.resolve({}));

                    response.data._items.map(function (x) {
                        for (let i in x.attributes) {
                            self.$set(self.show, x.name + "-" + x.attributes[i].name, false);

                            for (let j in x.attributes[i].items) {
                                self.$set(self.attritem_check_state, x.attributes[i].items[j]._id, true);  // default set all the attritem_check_state to be true
                            }
                        }
                    });
                })
                .catch(function (error) {
                    alert(JSON.stringify(error));
                })

            ]);

            // merge class_dict and tag_dict
            self.full_dict = {...self.class_dict, ...self.tag_dict};

        },
        add_class: function () {
            let self = this;
            self.selected_classes_or_tags.push(self.full_dict[self.cur_category][self.cur_idx_in_category]);
        },
        remove_class: function (annoclass_id) {
            let self = this;
            let index = self.selected_classes_or_tags.findIndex(item => item._id === annoclass_id);
                if (index !== -1) {
                self.selected_classes_or_tags.splice(index, 1);
            }
        },
        create_scene: function () {
            let self = this;

            // check if scene_name is empty, if so, alert and return
            if (self.scene_name === undefined || self.scene_name === "") {
                alert("场景名称不能为空");
                return;
            }

            // check if the same scene_name has been exist in the DB, if so, alert and return
            // here is how we do it:
            // 1. query the RESTAPI /annoscene?where={"name": "self.scene_name"}
            // 2. see if the returned data is empty, if not, alert and return
            axios.get(`/annoscene?where={"name": "${self.scene_name}"}`)
                .then(function (response) {
                    if (response.data._items.length === 0) {
                        headers = {'Content-Type': 'application/json'};
                        let new_scene = {
                            "name": self.scene_name,
                            "desc": self.scene_desc,
                            "classes": self.selected_classes_or_tags.filter(e => e.source === 'annoclass').map(function(cls){
                                return remove_unnecessary_keys(
                                    remove_unchecked_attritems(cls, self.attritem_check_state), ['_created', '_updated', '_links', 'source']
                                );
                            }),
                            "tags": self.selected_classes_or_tags.filter(e => e.source === 'annotag').map(function(cls){
                                return remove_unnecessary_keys(
                                    remove_unchecked_attritems(cls, self.attritem_check_state), ['_created', '_updated', '_links', 'source']
                                );
                            })
                        };

                        axios.post("/annoscene", new_scene, {headers: headers})  // call eve rest api
                            .then(function (response) {
                                alert("成功创建标注场景");
                                
                                // jump to all_annoscenes page
                                window.location.href = "/all_annoscenes";

                            }).catch(function (error) {
                                alert(JSON.stringify(error));
                        });
                    } else {
                        alert(`场景名称${self.scene_name}已经存在，请换一个名字重试.`);
                    }
                })
        },
        show_attr: function (annoclass_name, attr_name) {
            this.$set(this.show, annoclass_name + "-" + attr_name, !this.show[annoclass_name + "-" + attr_name])
        },
        attr_shown_state: function (annoclass_name, attr_name) {
            return this.show[annoclass_name + "-" + attr_name];
        }
    }
});
