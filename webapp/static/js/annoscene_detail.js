let annoscene_detail_table = new Vue({
    el: '#annoscene_detail_table',
    data: {
        scene: {
            "name": "not populated",
            "desc": "not populated",
            "classes": [],
            "tags": [],
        },
        show: {},
    },
    mounted: function () {
        let self = this;
        let url_parts = window.location.href.replace(/\/+$/, '').split('/');
        let scene_id = url_parts[url_parts.length - 1];

        axios.get('/annoscene/'+scene_id+'?max_results=200')
            .then(async function (response) {
                self.scene = response.data;

                // Set the toggle state of classes to false
                self.scene.classes.map(async function (annoclass) {

                    // by default, set the attributes's show state to false
                    annoclass.attributes.map(function (attr) {
                        self.$set(self.show, annoclass.name + "-" + attr.name, false);
                    });
                    
                });

                // Set the toggle state of tags to false
                self.scene.tags.map(async function (annotag) {

                    // by default, set the attributes's show state to false
                    annotag.attributes.map(function (attr) {
                        self.$set(self.show, annotag.name + "-" + attr.name, false);
                    });
                    
                });
            })
            .catch(function (error) {
                alert(JSON.stringify(error));
            });
    },
    computed: {
        sorted_class_or_tag_array: function () {
            let classes_or_tags = this.scene.classes.concat(this.scene.tags);
            return classes_or_tags.sort((a, b) => {
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
        toggle_attr: function (class_or_tag_name, attr_name) {
            this.$set(this.show, class_or_tag_name + "-" + attr_name, !this.show[class_or_tag_name + "-" + attr_name])
        },
        toggle_state: function (class_or_tag_name, attr_name) {
            return this.show[class_or_tag_name + "-" + attr_name];
        }
    }
});
