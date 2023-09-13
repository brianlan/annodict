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
                        _id: x._id,
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
    methods: {
        delete_scene: function (scene_idx) {
            let self = this;
            let scene_id = self.scenes[scene_idx]._id;
            let scene_name = self.scenes[scene_idx].name;

            // popup a message box to let user confirm whether to delete
            if (!confirm("Are you sure to delete scene " + scene_name + "?")) {
                return;
            }

            axios.delete('/annoscene/'+scene_id)
                .then(function (response) {
                    console.log("Scene " + scene_id + " has been deleted.")
                })
                .catch(function (error) {
                    alert(JSON.stringify(error));
                });
            
            self.scenes.splice(scene_idx, 1);
        },
    }
});
