const VUE_ELEMENT = '#application';

$(document).ready(() => {
    new Vue({
        el: VUE_ELEMENT,
        data: {},
        methods: {
            get_test_json: function () {

            }
        },
        created: function () {

        },
    });
});

class Helper {
    static get_cookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}
