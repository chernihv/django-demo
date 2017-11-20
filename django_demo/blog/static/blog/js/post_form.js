var FORM_IMAGE = '#post_image';
var FORM_IMAGE_INPUT = '#post_image_input';

function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $(FORM_IMAGE).attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$(FORM_IMAGE_INPUT).change(function () {
    readURL(this);
});
