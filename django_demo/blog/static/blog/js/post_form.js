var FORM_IMAGE = '#post_image';
var FORM_IMAGE_INPUT = '#post_image_input';
var POST_CONTENT_BLOCKS = '#post_blocks';
var POST_TITLE_INPUT = '#title';
var POST_TEXT_INPUT = '#post_text';

var QUESTION_ITER = 0;
var IMAGE_ITER = 0;
var BLOCK_ITER = 0;
var HAVE_FIRST_CODE_BLOCK = false;

const FRONT_NAME_QUESTIONS = 'question_block';
const FRONT_NAME_CODE_BLOCKS = 'code_block';
const FRONT_NAME_IMAGE_BLOCKS = 'image_block';
const FRONT_NAME_TEXT_BLOCKS = 'text_block';


var application;
var helper;
var constructor;

$(document).ready(function (event) {
    application = new Application();
    application.start();
});

function Application() {

    this.start = function () {
        this.create_base_objects();
        this.attach_event_handlers();
        this.ready_log();
    };

    this.create_base_objects = function () {
        helper = new Helpers();
        constructor = new Constructors();
    };

    this.attach_event_handlers = function () {
        $(FORM_IMAGE_INPUT).change(function () {
            helper.readURL(this);
        });
        $(document).on('click', '.question-block a', function (event) {
            var target = $(event.target);
            var parent_id = $(target).attr('value');
            var parent = $('#question_block_' + parent_id);
            this.add_choice_block(parent);
        });
        $(document).on('click', '#add_image_block_button', function () {
            constructor.add_image_block();
        });
        $(document).on('click', '#add_code_block_button', function () {
            constructor.add_code_block();
        });
        $(document).on('click', '#add_text_block_button', function () {
            constructor.add_text_block();
        });
        $(document).on('change', '[name=' + FRONT_NAME_IMAGE_BLOCKS + ']', function (event) {
            helper.readURL(this, $("#image_block_" + IMAGE_ITER));
            IMAGE_ITER++;
        });
        $(document).on('click', '#send_form_button', function (event) {
            $.ajax({
                type: 'POST',
                url: ACTION_URL,
                data: helper.get_form_data(),
                processData: false,
                contentType: false,
                success: function (response_data) {
                    window.location = response_data['redirect'];
                }
            });
        });
    };

    this.ready_log = function () {
        console.log('App ready');
        console.log('Post ID: ' + POST_ID);
    };
}

function Helpers() {
    this.readURL = function (input, image_elem) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                if (image_elem !== undefined) {
                    $(image_elem).attr('src', e.target.result);
                } else {
                    $(FORM_IMAGE).attr('src', e.target.result);
                }
            };
            reader.readAsDataURL(input.files[0]);
        }
    };

    this.get_form_data = function () {
        var form_data = new FormData();
        form_data.append('file', $(FORM_IMAGE_INPUT)[0].files[0]);
        form_data.append('csrfmiddlewaretoken', CSRF_TOKEN);
        form_data.append('title', $(POST_TITLE_INPUT).val());
        form_data.append('post_text', $(POST_TEXT_INPUT).val());
        var image_blocks = $('[name=' + FRONT_NAME_IMAGE_BLOCKS + ']');
        for (i = 0; i < image_blocks.length; i++) {
            form_data.append(FRONT_NAME_IMAGE_BLOCKS, image_blocks[i].files[0]);
        }
        var code_blocks = $('[name=' + FRONT_NAME_CODE_BLOCKS + ']');
        for (i = 0; i < code_blocks.length; i++) {
            form_data.append(FRONT_NAME_CODE_BLOCKS, $(code_blocks[i]).val());
        }
        var text_bloks = $('[name=' + FRONT_NAME_TEXT_BLOCKS + ']');
        for (i = 0; i < text_bloks.length; i++) {
            form_data.append(FRONT_NAME_TEXT_BLOCKS, $(text_bloks[i]).val());
        }
        return form_data;
    };
}

function Constructors() {
    this.add_image_block = function () {
        var first_elem = $('<div class="col-md-12 blog-post"></div>');
        var second_elem = $('<div class="post-image"></div>');
        var third_elem = $('<img>');

        third_elem.attr('id', 'image_block_' + IMAGE_ITER);

        first_elem.append(second_elem);
        second_elem.append(third_elem);

        var wrapper = $("<a hidden></a>");
        var input = $("<input type='file'>");
        input.attr('name', FRONT_NAME_IMAGE_BLOCKS);
        input.attr('id', 'image_block_' + IMAGE_ITER);
        this.add_in_queue(input);
        wrapper.append(input);

        $(POST_CONTENT_BLOCKS).append(this.get_hr());
        $(POST_CONTENT_BLOCKS).append(first_elem);
        $(POST_CONTENT_BLOCKS).append(wrapper);
        input.click();
    };

    this.add_code_block = function () {
        var code_block = $("<textarea required placeholder='Code block'></textarea>");
        var original = $(POST_CONTENT_BLOCKS + ' textarea').first();
        code_block.addClass(original.attr('class'));
        code_block.attr('name', FRONT_NAME_CODE_BLOCKS);
        code_block.attr('rows', original.attr('rows'));
        this.add_in_queue(code_block);


        $(POST_CONTENT_BLOCKS).append(this.get_hr());
        $(POST_CONTENT_BLOCKS).append(code_block);
        if (!HAVE_FIRST_CODE_BLOCK) {
            var alert_block = this.create_bootstrap_alert('Text in this area wrap in special code tags');
            $(POST_CONTENT_BLOCKS).append(alert_block);
            HAVE_FIRST_CODE_BLOCK = true;
        }
    };

    this.add_question_block = function () {
        var question_block = $("<div class='question-block'></div>");
        question_block.attr('id', 'question_block_' + QUESTION_ITER);
        var question_text = $("<input type='text' required class='form-control' title='Question' placeholder='Enter you question'>");

        var add_choice_button = $("<a style='cursor: pointer; user-select: none' '>add choice...</a>");
        add_choice_button.attr('value', QUESTION_ITER);
        add_choice_button.attr('id', 'add_choice_button_' + QUESTION_ITER);

        question_text.attr('name', FRONT_NAME_QUESTIONS);
        question_block.attr('iter', QUESTION_ITER);
        QUESTION_ITER++;

        question_block.append(add_choice_button);
        question_block.append(question_text);

        $(POST_CONTENT_BLOCKS).append(this.get_hr());
        $(POST_CONTENT_BLOCKS).append(question_block);
        this.add_choice_block(question_block);
        this.add_choice_block(question_block);
    };

    this.add_choice_block = function (parent) {

        var choice_block = $("<input type='text' required class='form-control' placeholder='One of choice'>");
        choice_block.attr('title', 'Choice question ' + parent.attr('iter'));
        choice_block.attr('name', 'choice_text_' + parent.attr('iter'));

        parent.append(choice_block);
    };

    this.add_text_block = function () {

        var text_block = $("<textarea required></textarea>");
        var original = $(POST_CONTENT_BLOCKS + ' textarea').first();
        text_block.addClass(original.attr('class'));
        text_block.attr('name', FRONT_NAME_TEXT_BLOCKS);
        text_block.attr('rows', original.attr('rows'));
        text_block.attr('placeholder', original.attr('placeholder'));
        this.add_in_queue(text_block);

        $(POST_CONTENT_BLOCKS).append(this.get_hr());
        $(POST_CONTENT_BLOCKS).append(text_block);
    };

    this.create_bootstrap_alert = function (text) {
        var info_block = $("<div class='alert alert-info' title='Notice!' style='margin-top: 10px'></div>");
        var second_info_block = $("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>×</button>");
        var third_info_block = $("<strong>Notice:</strong><span> " + text + "</span>");

        info_block.append(second_info_block);
        info_block.append(third_info_block);
        return info_block;
    };

    this.get_hr = function () {
        return $("<hr>")
    };

    this.add_in_queue = function (block) {
        block.attr('order', BLOCK_ITER);
        BLOCK_ITER++;
    };

}
