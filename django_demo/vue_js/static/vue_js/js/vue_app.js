$(document).ready(function (event) {
    const vue_app = new Vue({
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
