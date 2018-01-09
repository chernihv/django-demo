$(document).ready(function (event) {
    const application = new Vue({
        el: '#vue_app',
        data: {
            message: 1
        },
        methods: {
            add_counter: function (event) {
                this.message++;
            }
        }
    });
});

class Application {
    constructor(vue_selector) {
        this.vue_selector = vue_selector;
    }
}
