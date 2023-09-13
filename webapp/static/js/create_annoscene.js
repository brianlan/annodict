let new_annoscene = new Vue({
    el: '#new_annoscene',
    data: {
        scene_name: undefined,
        scene_desc: undefined,
        selected_classes: [],
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
            return this.selected_classes.map(x => x._id);
        }
    },
    methods: {
        fetch_full_dict: function() {
            let self = this;

            axios.get('/annoclass?embedded={"attributes":1}&max_results=200')
            .then(async function (response) {
                self.full_dict = await response.data._items.reduce(async (accPromise, x) => {
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
                    }
                });
            })
            .catch(function (error) {
                alert(JSON.stringify(error));
            });
        },
        add_class: function (annoclass) {
            let self = this;
            self.selected_classes.push(self.full_dict[self.cur_category][self.cur_idx_in_category]);
        },
        remove_class: function (annoclass_id) {
            let self = this;
            let index = self.selected_classes.findIndex(item => item._id === annoclass_id);
                if (index !== -1) {
                self.selected_classes.splice(index, 1);
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
                            "classes": self.selected_class_ids
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
        toggle_attr: function (annoclass_name, attr_name) {
            this.$set(this.show, annoclass_name + "-" + attr_name, !this.show[annoclass_name + "-" + attr_name])
        },
        toggle_state: function (annoclass_name, attr_name) {
            return this.show[annoclass_name + "-" + attr_name];
        }
    }
});
