let all_annotag_table = new Vue({
    el: '#all_annotag_table',
    data: {
        full_dict: {},
        show: {},
    },
    mounted: function () {
        this.fetch_full_dict();
    },
    methods: {
        fetch_full_dict: function() {
            let self = this;

            axios.get('/annotag?embedded={"attributes":1}&max_results=200')
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

                    // Push the annotag to the corresponding category array
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
        toggle_attr: function (annotag_name, attr_name) {
            this.$set(this.show, annotag_name + "-" + attr_name, !this.show[annotag_name + "-" + attr_name])
        },
        toggle_state: function (annotag_name, attr_name) {
            return this.show[annotag_name + "-" + attr_name];
        }
    }
});