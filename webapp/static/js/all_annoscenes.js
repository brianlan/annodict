let all_annoscene_table = new Vue({
    el: '#all_annoscene_table',
    data: {
        scenes: {},
    },
    mounted: function () {
        let self = this;
        axios.get('/annoscene?max_results=200')
            .then(function (response) {
                self.scenes = response.data._items.map(function (x) {
                    return {
                        id: x._id,
                        name: x.name,
                        num_classes: x.classes.length,
                        created_ts: x._created,
                    };
                });

            })
            .catch(function (error) {
                alert(JSON.stringify(error));
            });
    },
    // methods: {
    //     toggle_attr: function (annoclass_name, attr_name) {
    //         this.$set(this.show, annoclass_name + "-" + attr_name, !this.show[annoclass_name + "-" + attr_name])
    //     },
    //     toggle_state: function (annoclass_name, attr_name) {
    //         return this.show[annoclass_name + "-" + attr_name];
    //     }
    // }
});
