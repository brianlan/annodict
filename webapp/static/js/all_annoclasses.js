let all_annoclass_table = new Vue({
    el: '#all_annoclass_table',
    data: {
        categories: {},
        show: {
            'attr.animal.animal.type': false,
        },
        flags: {
            'ok': false,
            'attr.animal.animal.type': false,
        },
    },
    mounted: function () {
        let self = this;
        axios.get('/annoclass?embedded={"attributes":1}&max_results=200')
            .then(function (response) {
                self.categories = response.data._items.reduce((acc, x) => {
                    // If the category does not exist in the accumulator object, create an empty array for it
                    if (!acc[x.category]) {
                      acc[x.category] = [];
                    }

                    // Push the annoclass to the corresponding category array
                    acc[x.category].push(x);
                    // Return the updated accumulator object
                    return acc;
                }, {});

                response.data._items.map(function (x) {
                    for (let i in x.attributes) {
                        self.$set(self.show, x.attributes[i].name, false);
                    }
                });
            })
            .catch(function (error) {
                alert(JSON.stringify(error));
            });
    },
    methods: {
        toggle_attr: function (attr_name) {
            this.$set(this.show, attr_name, !this.show[attr_name])
        }
    }
    // methods: {
    //     delete_job: function (idx) {
    //         let self = this;
    //         axios.delete('/job/' + self.jobs[idx].id)
    //             .then(function (response){
    //                 console.log("deleted job " + self.jobs[idx].id);
    //                 self.jobs.splice(idx, 1);
    //             })
    //             .catch(function (error) {
    //                 alert(JSON.stringify(error));
    //             });
    //     }
    // }
});
