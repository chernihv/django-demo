var FORM_IMAGE = '#post_image';
var FORM_IMAGE_INPUT = '#post_image_input';
var POST_CONTENT_BLOCKS = '#post_blocks';

var QUESTION_ITER = 0;
var IMAGE_ITER = 0;
var HAVE_FIRST_CODE_BLOCK = false;

var FRONT_NAME_QUESTIONS = 'question_block';
var FRONT_NAME_CODE_BLOCKS = 'code_block';
var FRONT_NAME_IMAGE_BLOCKS = 'image_block';
var FRONT_NAME_TEXT_BLOCKS = 'text_block';

function readURL(input, image_elem) {

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
}

function get_hr() {
    return $("<hr>")
}

$(FORM_IMAGE_INPUT).change(function () {
    readURL(this);
});

function add_image_block() {
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
    wrapper.append(input);

    $(POST_CONTENT_BLOCKS).append(get_hr());
    $(POST_CONTENT_BLOCKS).append(first_elem);
    $(POST_CONTENT_BLOCKS).append(wrapper);
    input.click();
}

function add_code_block() {
    var code_block = $("<textarea required placeholder='Code block'></textarea>");
    var original = $(POST_CONTENT_BLOCKS + ' textarea').first();
    code_block.addClass(original.attr('class'));
    code_block.attr('name', FRONT_NAME_CODE_BLOCKS);
    code_block.attr('rows', original.attr('rows'));

    $(POST_CONTENT_BLOCKS).append(get_hr());
    if (!HAVE_FIRST_CODE_BLOCK) {
        var alert_block = create_bootstrap_alert('Text in this area wrap in special code tags');
        $(POST_CONTENT_BLOCKS).append(alert_block);
        HAVE_FIRST_CODE_BLOCK = true;
    }
    $(POST_CONTENT_BLOCKS).append(code_block);
}

function add_question_block() {
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

    $(POST_CONTENT_BLOCKS).append(get_hr());
    $(POST_CONTENT_BLOCKS).append(question_block);
    add_choice_block(question_block);
    add_choice_block(question_block);
}

function add_choice_block(parent) {

    var choice_block = $("<input type='text' required class='form-control' placeholder='One of choice'>");
    choice_block.attr('title', 'Choice question ' + parent.attr('iter'));
    choice_block.attr('name', 'choice_text_' + parent.attr('iter'));

    parent.append(choice_block);
}

function add_text_block() {

    var text_block = $("<textarea required></textarea>");
    var original = $(POST_CONTENT_BLOCKS + ' textarea').first();
    text_block.addClass(original.attr('class'));
    text_block.attr('name', FRONT_NAME_TEXT_BLOCKS);
    text_block.attr('rows', original.attr('rows'));
    text_block.attr('placeholder', original.attr('placeholder'));

    $(POST_CONTENT_BLOCKS).append(get_hr());
    $(POST_CONTENT_BLOCKS).append(text_block);
}

$(document).ready(function (event) {
    $(document).on('click', '.question-block a', function (event) {
        var target = $(event.target);
        var parent_id = $(target).attr('value');
        var parent = $('#question_block_' + parent_id);
        add_choice_block(parent);
    });
    $(document).on('change', '[name=' + FRONT_NAME_IMAGE_BLOCKS + ']', function (event) {
        readURL(this, $("#image_block_" + IMAGE_ITER));
        IMAGE_ITER++;
    });
});

function create_bootstrap_alert(text) {
    var info_block = $("<div class='alert alert-info' title='Notice!'></div>");
    var second_info_block = $("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>×</button>");
    var third_info_block = $("<strong>Notice:</strong><span> " + text + "</span>");

    info_block.append(second_info_block);
    info_block.append(third_info_block);
    return info_block;
}
