let app;

const CODE_BLOCKS = 'block_code';
const IMAGE_BLOCKS = 'block_image';
const TEXT_BLOCKS = 'block_text';

let FORM_IMAGE = '#post_image';
let FORM_IMAGE_INPUT = '#post_image_input';
let POST_CONTENT_BLOCKS = '#post_blocks';
let POST_TITLE_INPUT = '#title';
let POST_TEXT_INPUT = '#post_text';

let ADD_CODE_BLOCK_BUTTON = '#add_code_block_button';
let ADD_TEXT_BLOCK_BUTTON = '#add_text_block_button';
let ADD_IMAGE_BLOCK_BUTTON = '#add_image_block_button';

let REMOVE_BLOCK_BUTTON = '.remove-block';
let SAVE_BLOCK_BUTTON = '.save-block';

$(document).ready(function (event) {
    app = new Application();
});

class Application {

    constructor() {
        this.create_base_objects();
        Application.ready_log();
    };

    create_base_objects() {
        this.event_handlers = new EventHandlers();
        this.helper = new Helpers();
        this.post_constructor = new PostConstructor();
        this.post_constructor_original_textinput = $(POST_CONTENT_BLOCKS + ' textarea').first();
    };

    static ready_log() {
        console.log('Constructor ready');
        console.log('Post ID: ' + POST_ID);
    };
}

class EventHandlers {
    constructor() {
        this.change_image_input();
        this.question_block_button();
        this.image_block_button();
        this.code_block_button();
        this.text_block_button();
        this.remove_created_block();
        this.send_form();
        this.save_created_block();
    }

    change_image_input() {
        $(FORM_IMAGE_INPUT).change(function () {
            Helpers.readURL(this);
        });
    }

    question_block_button() {
        $(document).on('click', '.question-block a', function (event) {
            let target = $(event.target);
            let parent_id = $(target).attr('value');
            let parent = $('#question_block_' + parent_id);
            app.add_choice_block(parent);
        });
    }

    image_block_button() {
        $(document).on('click', ADD_IMAGE_BLOCK_BUTTON, function () {
            app.post_constructor.add_image_block();
        });
        $(document).on('change', '[name=' + IMAGE_BLOCKS + ']', function (event) {
            Helpers.readURL(this, $("#image_block_" + app.post_constructor.image_iter));
            app.post_constructor.image_iter++;
        });
    }

    code_block_button() {
        $(document).on('click', ADD_CODE_BLOCK_BUTTON, function () {
            Helpers.request_create_new_block(CODE_BLOCKS, PostConstructor.add_code_block);
        });
    }

    text_block_button() {
        $(document).on('click', ADD_TEXT_BLOCK_BUTTON, function () {
            Helpers.request_create_new_block(TEXT_BLOCKS, PostConstructor.add_text_block);
        });
    }

    send_form() {
        $(document).on('click', '#send_form_button', function (event) {
            $.post(PUBLISH_POST, {'post_id': POST_ID, csrfmiddlewaretoken: CSRF_TOKEN}, function (data) {
                window.location = data['redirect']
            });
        });
    }

    remove_created_block() {
        $(document).on('click', REMOVE_BLOCK_BUTTON, function (event) {
            let block_id = $(event.target).attr('block_id');
            if (confirm('Remove block?')) {
                Helpers.request_delete_block(block_id, PostConstructor.delete_block);
            }
        });
    }

    save_created_block() {
        function send_changes(event) {
            let block_id = $(event.target).attr('block_id');
            let value = $('textarea[block_id=' + block_id + ']').val();
            $.post(SAVE_BLOCK_ACTION, {
                block_id: block_id,
                value: value,
                csrfmiddlewaretoken: CSRF_TOKEN
            }, function (data) {

            });
        }

        $(document).on('click', SAVE_BLOCK_BUTTON, send_changes);
        $(document).on('change', 'textarea[block_id]', send_changes);
    }
}

class Helpers {
    static readURL(input, image_elem) {
        if (input.files && input.files[0]) {
            let reader = new FileReader();
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

    static request_create_new_block(block_type, call_back) {
        $.post(CREATE_BLOCK_ACTION, {block_type: block_type, csrfmiddlewaretoken: CSRF_TOKEN}, function (data) {
            PostConstructor.append_wrapper(call_back, data);
        });
    };

    static request_delete_block(block_id, call_back) {
        $.post(DELETE_BLOCK_ACTION, {block_id: block_id, csrfmiddlewaretoken: CSRF_TOKEN}, function (data) {
            call_back(data);
        });
    }
}

class PostConstructor {

    constructor() {
        this.block_iter = 0;
        this.is_have_first_block_code = false;
    };

    static before_append(data) {

    };

    static append_wrapper(func, data) {
        PostConstructor.before_append(data);
        func(data);
        PostConstructor.after_append(data);
    };

    static after_append(data) {
        app.post_constructor.block_iter++;
        console.log('Block created, id:' + PostConstructor.get_block_id(data));
    };

    add_image_block() {
        let first_elem = $('<div class="col-md-12 blog-post"></div>');
        let second_elem = $('<div class="post-image"></div>');
        let third_elem = $('<img>');

        third_elem.attr('id', 'image_block_' + this.image_iter);

        first_elem.append(second_elem);
        second_elem.append(third_elem);

        let wrapper = $("<a hidden></a>");
        let input = $("<input type='file'>");
        input.attr('name', IMAGE_BLOCKS);
        input.attr('id', 'image_block_' + this.image_iter);
        wrapper.append(input);

        $(POST_CONTENT_BLOCKS).append(this.create_hr());
        $(POST_CONTENT_BLOCKS).append(first_elem);
        $(POST_CONTENT_BLOCKS).append(wrapper);
        input.click();
    };

    static add_text_block(data) {

        let block_id = PostConstructor.get_block_id(data);
        let text_block = $("<textarea required></textarea>");
        let original = app.post_constructor_original_textinput;

        let labels = PostConstructor.create_labels(block_id, data['block_type']);

        PostConstructor.add_block_id(text_block, block_id);
        text_block.addClass(original.attr('class'));
        text_block.addClass('margin-top-10');
        text_block.attr('name', TEXT_BLOCKS);
        text_block.attr('rows', original.attr('rows'));
        text_block.attr('placeholder', original.attr('placeholder'));

        let wrapper = $("<div></div>");
        PostConstructor.add_block_id(wrapper, block_id);

        wrapper.append(PostConstructor.create_hr());
        wrapper.append(labels);
        wrapper.append(text_block);

        $(POST_CONTENT_BLOCKS).append(wrapper);
    };

    static add_code_block(data) {
        let block_id = PostConstructor.get_block_id(data);
        let code_block = $("<textarea required placeholder='Code block'></textarea>");
        let original = $(POST_CONTENT_BLOCKS + ' textarea').first();
        code_block.addClass(original.attr('class'));
        PostConstructor.add_block_id(code_block, block_id);
        code_block.attr('name', CODE_BLOCKS);
        code_block.attr('rows', original.attr('rows'));

        let wrapper = $("<div></div>");
        PostConstructor.add_block_id(wrapper, block_id);
        wrapper.append(PostConstructor.create_hr());
        wrapper.append(PostConstructor.create_labels(block_id, data['block_type']));
        wrapper.append(code_block);

        $(POST_CONTENT_BLOCKS).append(wrapper);
        if (!app.post_constructor.is_have_first_block_code) {
            let alert_block = PostConstructor.create_bootstrap_alert('Text in this area wrap in special code tags');
            $(POST_CONTENT_BLOCKS).append(alert_block);
            app.post_constructor.is_have_first_block_code = true;
        }
    };

    static add_block_id(object, block_id) {
        $(object).attr('block_id', block_id);
    };

    static get_block_id(data) {
        return data['block_id'];
    };

    static create_labels(block_id, block_type, append_save_button = true) {
        let first_label = $('<span class="label label-info margin-bottom-10">Type: ' + block_type + '</span>');
        let second_label = $('<span class="label label-pill label-danger margin-bottom-10 remove-block">remove</span>');
        PostConstructor.add_block_id(second_label, block_id);

        let wrapper = $("<div></div>");
        wrapper.append(first_label);
        wrapper.append(second_label);

        if (append_save_button) {
            let third_label = $('<span class="label label-success margin-bottom-10 save-block">save changes</span>');
            PostConstructor.add_block_id(third_label, block_id);
            wrapper.append(third_label);
        }

        return wrapper;
    };

    static create_bootstrap_alert(text) {
        let info_block = $("<div class='alert alert-info' title='Notice!' style='margin-top: 10px'></div>");
        let second_info_block = $("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>×</button>");
        let third_info_block = $("<strong>Notice:</strong><span> " + text + "</span>");

        info_block.append(second_info_block);
        info_block.append(third_info_block);
        return info_block;
    };

    static create_hr() {
        return $("<hr>");
    };

    static delete_block(data) {
        $("div[block_id=" + PostConstructor.get_block_id(data) + "]").remove();
    }
}
