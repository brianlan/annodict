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
            .then(function (response) {
                self.scene = response.data;
                self.scene.classes.map(function (annoclass_id) {
                    axios.get('/annoclass/'+annoclass_id+'?embedded={"attributes":1}')
                        .then(function (response) {
                            self.class_array.push(response.data);

                            response.data.attributes.map(function (attr) {
                                self.$set(self.show, response.data.name + "-" + attr.name, false);
                            });
                        })
                        .catch(function (error) {
                            alert(JSON.stringify(error));
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
