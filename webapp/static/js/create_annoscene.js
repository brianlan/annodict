let new_annoscene = new Vue({
    el: '#new_annoscene',
    data: {
        scene_name: undefined,
        scene_desc: undefined,
        selected_classes: [],
        categories: {},
        show: {},
        cur_category: undefined,
        cur_idx_in_category: undefined,
    },
    mounted: function () {
        let self = this;

        axios.get('/annoclass/?embedded={"attributes":1}&max_results=200')
            .then(function (response) {
                self.categories = response.data._items.reduce((acc, x) => {
                    // If the category does not exist in the accumulator object, create an empty array for it
                    if (!acc[x.category]) {
                      acc[x.category] = [];
                    }

                    // Push the annoclass to the corresponding category array
                    acc[x.category].push(x);
                    
                    x.attributes.map(function (attr) {
                        self.$set(self.show, x.name + "-" + attr.name, false);
                    });    

                    return acc;
                }, {});

                
            })
            .catch(function (error) {
                alert(JSON.stringify(error));
            });
    },
    computed: {
        selected_class_ids: function () {
            return this.selected_classes.map(x => x._id);
        }
    },
    methods: {
        add_class: function (annoclass) {
            let self = this;
            self.selected_classes.push(self.categories[self.cur_category][self.cur_idx_in_category]);
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

            headers = {'Content-Type': 'application/json'};
            let new_scene = {
                "name": self.scene_name, 
                "desc": self.scene_desc, 
                "classes": self.selected_class_ids
            };
            axios.post("/annoscene", new_scene, {headers: headers})  // call eve rest api
                .then(function (response) {
                    alert("成功创建标注场景");
                }).catch(function (error) {
                    alert(JSON.stringify(error));
            });
        },
        toggle_attr: function (annoclass_name, attr_name) {
            this.$set(this.show, annoclass_name + "-" + attr_name, !this.show[annoclass_name + "-" + attr_name])
        },
        toggle_state: function (annoclass_name, attr_name) {
            return this.show[annoclass_name + "-" + attr_name];
        }
    }
});
