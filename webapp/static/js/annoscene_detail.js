let annoscene_detail_table = new Vue({
    el: '#annoscene_detail_table',
    data: {
        scene: {
            "name": "not populated",
            "desc": "not populated",
        },
        class_array: [],
        show: {},
    },
    mounted: function () {
        let self = this;
        let url_parts = window.location.href.replace(/\/+$/, '').split('/');
        let scene_id = url_parts[url_parts.length - 1];

        axios.get('/annoscene/'+scene_id+'?max_results=200')
            .then(async function (response) {
                self.scene = response.data;
                self.scene.classes.map(async function (annoclass_id) {
                    let annoclass = await axios.get('/annoclass/'+annoclass_id);
                    
                    // fetch annoattr of annoclass.attributes (annoclass.attributes is an array of annoattr ids)
                    let annoattr_ids = '"' + annoclass.data.attributes.join('","') + '"';
                    let annoattr_result = await axios.get(`/annoattr?embedded={"items":1}&where={"_id": {"$in": [${annoattr_ids}]}}`);
                    annoclass.data.attributes = annoattr_result.data._items;

                    self.class_array.push(annoclass.data);

                    // by default, set the attributes's show state to false
                    annoclass.data.attributes.map(function (attr) {
                        self.$set(self.show, annoclass.data.name + "-" + attr.name, false);
                    });
                    
                });
            })
            .catch(function (error) {
                alert(JSON.stringify(error));
            });
    },
    computed: {
        sorted_class_array: function () {
            return this.class_array.sort((a, b) => {
                if(a.category < b.category) {
                    return -1;
                }
                if(a.category > b.category) {
                    return 1;
                }
                return 0;
            });
        }
    },
    methods: {
        toggle_attr: function (annoclass_name, attr_name) {
            this.$set(this.show, annoclass_name + "-" + attr_name, !this.show[annoclass_name + "-" + attr_name])
        },
        toggle_state: function (annoclass_name, attr_name) {
            return this.show[annoclass_name + "-" + attr_name];
        }
    }
});
