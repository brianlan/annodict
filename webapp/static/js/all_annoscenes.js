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
                        num_classes_or_tags: x.classes.length + x.tags.length,
                        created_ts: x._created,
                    };
                });

            })
            .catch(function (error) {
                alert(JSON.stringify(error));
            });
    },
    methods: {
        export_scene: function (scene_idx, export_type) {
            let self = this;
            let scene_id = self.scenes[scene_idx]._id;

            axios({
                url: `/export_scene/${scene_id}/${export_type}`,
                method: 'GET',
                responseType: 'blob', // Important
            })
            .then((response) => {
                // Create a new Blob object using the response data of the file
                const blob = new Blob([response.data], { type: response.headers['content-type'] });
                
                // Create a URL for the blob object
                const downloadUrl = window.URL.createObjectURL(blob);
                
                // Create a temporary <a> element and trigger a download
                const link = document.createElement('a');
                link.href = downloadUrl;
                link.setAttribute('download', `${scene_id}.${export_type}`); // Use the file name you want
                document.body.appendChild(link);
                link.click();
                
                // Clean up and revoke the object URL
                link.remove();
                window.URL.revokeObjectURL(downloadUrl);
    
                console.log(`Exported scene ${scene_id} as ${export_type}.`);
            })
            .catch((error) => {
                alert(JSON.stringify(error));
            });

            // axios.get(`/export_scene/${scene_id}/${export_type}`)
            //     .then(function (response) {
            //         console.log(`Exported scene ${scene_id} as ${export_type}.`)
            //     })
            //     .catch(function (error) {
            //         alert(JSON.stringify(error));
            //     });
        },
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
