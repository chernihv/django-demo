let app;
let app_settings;

$(document).ready(function (event) {
    app_settings = new AppSettings();
    app = new Application();
});

class Application {

    constructor() {
        this.create_base_objects();
        this.ready_log();
    };

    create_base_objects() {
        this.event_handlers = new EventHandlers();
        this.helper = new Helpers();
        this.post_constructor = new PostConstructor();
    };

    ready_log() {
        console.log('Constructor ready');
        console.log('Post ID: ' + app_settings.POST_ID);
    };
}

class AppSettings {
    constructor() {
        this.FRONT_NAME_QUESTIONS = 'question_block';
        this.FRONT_NAME_CODE_BLOCKS = 'code_block';
        this.FRONT_NAME_IMAGE_BLOCKS = 'image_block';
        this.FRONT_NAME_TEXT_BLOCKS = 'text_block';

        //Remote values;
        this.POST_ID = POST_ID;
        this.ACTION_URL = ACTION_URL;
        this.CSRF_TOKEN = CSRF_TOKEN;

        this.FORM_IMAGE = '#post_image';
        this.FORM_IMAGE_INPUT = '#post_image_input';
        this.POST_CONTENT_BLOCKS = '#post_blocks';
        this.POST_TITLE_INPUT = '#title';
        this.POST_TEXT_INPUT = '#post_text';
    }
}

class EventHandlers {
    constructor() {
        this.change_image_input();
        this.question_block_button();
        this.image_block_button();
        this.code_block_button();
        this.test_block_button();
        this.remove_created_block();
        this.send_form();
    }

    change_image_input() {
        $(app_settings.FORM_IMAGE_INPUT).change(function () {
            app.helper.readURL(this);
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
        $(document).on('click', '#add_image_block_button', function () {
            app.post_constructor.add_image_block();
        });
        $(document).on('change', '[name=' + app_settings.FRONT_NAME_IMAGE_BLOCKS + ']', function (event) {
            app.helper.readURL(this, $("#image_block_" + app.post_constructor.IMAGE_ITER));
            app.post_constructor.IMAGE_ITER++;
        });
    }

    code_block_button() {
        $(document).on('click', '#add_code_block_button', function () {
            app.post_constructor.add_code_block();
        });
    }

    test_block_button() {
        $(document).on('click', '#add_text_block_button', function () {
            app.post_constructor.add_text_block();
        });
    }

    send_form() {
        $(document).on('click', '#send_form_button', function (event) {
            $.ajax({
                type: 'POST',
                url: app_settings.ACTION_URL,
                data: app.helper.get_form_data(),
                processData: false,
                contentType: false,
                success: function (response_data) {
                    window.location = response_data['redirect'];
                }
            });
        });
    }

    remove_created_block() {
        $(document).on('click', '.remove-block', function (event) {
            return confirm('Remove block?');
        });
    }

}

class Helpers {
    readURL(input, image_elem) {
        if (input.files && input.files[0]) {
            let reader = new FileReader();
            reader.onload = function (e) {
                if (image_elem !== undefined) {
                    $(image_elem).attr('src', e.target.result);
                } else {
                    $(app_settings.FORM_IMAGE).attr('src', e.target.result);
                }
            };
            reader.readAsDataURL(input.files[0]);
        }
    };

    get_form_data() {
        let form_data = new FormData();
        form_data.append('file', $(app_settings.FORM_IMAGE_INPUT)[0].files[0]);
        form_data.append('csrfmiddlewaretoken', app_settings.CSRF_TOKEN);
        form_data.append('title', $(app_settings.POST_TITLE_INPUT).val());
        form_data.append('post_text', $(app_settings.POST_TEXT_INPUT).val());
        let image_blocks = $('[name=' + app_settings.FRONT_NAME_IMAGE_BLOCKS + ']');
        for (let i = 0; i < image_blocks.length; i++) {
            form_data.append(app_settings.FRONT_NAME_IMAGE_BLOCKS, image_blocks[i].files[0]);
        }
        let code_blocks = $('[name=' + app_settings.FRONT_NAME_CODE_BLOCKS + ']');
        for (let i = 0; i < code_blocks.length; i++) {
            form_data.append(app_settings.FRONT_NAME_CODE_BLOCKS, $(code_blocks[i]).val());
        }
        let text_bloks = $('[name=' + app_settings.FRONT_NAME_TEXT_BLOCKS + ']');
        for (let i = 0; i < text_bloks.length; i++) {
            form_data.append(app_settings.FRONT_NAME_TEXT_BLOCKS, $(text_bloks[i]).val());
        }
        return form_data;
    };
}

class PostConstructor {

    constructor() {
        this.QUESTION_ITER = 0;
        this.IMAGE_ITER = 0;
        this.BLOCK_ITER = 0;
        this.HAVE_FIRST_CODE_BLOCK = false;
    }

    add_image_block() {
        let first_elem = $('<div class="col-md-12 blog-post"></div>');
        let second_elem = $('<div class="post-image"></div>');
        let third_elem = $('<img>');

        third_elem.attr('id', 'image_block_' + this.IMAGE_ITER);

        first_elem.append(second_elem);
        second_elem.append(third_elem);

        let wrapper = $("<a hidden></a>");
        let input = $("<input type='file'>");
        input.attr('name', app_settings.FRONT_NAME_IMAGE_BLOCKS);
        input.attr('id', 'image_block_' + this.IMAGE_ITER);
        this.add_in_queue(input);
        wrapper.append(input);

        $(app_settings.POST_CONTENT_BLOCKS).append(this.get_hr());
        $(app_settings.POST_CONTENT_BLOCKS).append(first_elem);
        $(app_settings.POST_CONTENT_BLOCKS).append(wrapper);
        input.click();
    };

    add_code_block() {
        let code_block = $("<textarea required placeholder='Code block'></textarea>");
        let original = $(app_settings.POST_CONTENT_BLOCKS + ' textarea').first();
        code_block.addClass(original.attr('class'));
        code_block.attr('name', app_settings.FRONT_NAME_CODE_BLOCKS);
        code_block.attr('rows', original.attr('rows'));
        this.add_in_queue(code_block);


        $(app_settings.POST_CONTENT_BLOCKS).append(this.get_hr());
        $(app_settings.POST_CONTENT_BLOCKS).append(code_block);
        if (!this.HAVE_FIRST_CODE_BLOCK) {
            let alert_block = this.create_bootstrap_alert('Text in this area wrap in special code tags');
            $(app_settings.POST_CONTENT_BLOCKS).append(alert_block);
            this.HAVE_FIRST_CODE_BLOCK = true;
        }
    };

    add_question_block() {
        let question_block = $("<div class='question-block'></div>");
        question_block.attr('id', 'question_block_' + this.QUESTION_ITER);
        let question_text = $("<input type='text' required class='form-control' title='Question' placeholder='Enter you question'>");

        let add_choice_button = $("<a style='cursor: pointer; user-select: none' '>add choice...</a>");
        add_choice_button.attr('value', this.QUESTION_ITER);
        add_choice_button.attr('id', 'add_choice_button_' + this.QUESTION_ITER);

        question_text.attr('name', app_settings.FRONT_NAME_QUESTIONS);
        question_block.attr('iter', this.QUESTION_ITER);
        this.QUESTION_ITER++;

        question_block.append(add_choice_button);
        question_block.append(question_text);

        $(app_settings.POST_CONTENT_BLOCKS).append(this.get_hr());
        $(app_settings.POST_CONTENT_BLOCKS).append(question_block);
        this.add_choice_block(question_block);
        this.add_choice_block(question_block);
    };

    add_choice_block(parent) {

        let choice_block = $("<input type='text' required class='form-control' placeholder='One of choice'>");
        choice_block.attr('title', 'Choice question ' + parent.attr('iter'));
        choice_block.attr('name', 'choice_text_' + parent.attr('iter'));

        parent.append(choice_block);
    };

    add_text_block() {

        let text_block = $("<textarea required></textarea>");
        let original = $(app_settings.POST_CONTENT_BLOCKS + ' textarea').first();
        text_block.addClass(original.attr('class'));
        text_block.attr('name', app_settings.FRONT_NAME_TEXT_BLOCKS);
        text_block.attr('rows', original.attr('rows'));
        text_block.attr('placeholder', original.attr('placeholder'));
        this.add_in_queue(text_block);

        $(app_settings.POST_CONTENT_BLOCKS).append(this.get_hr());
        $(app_settings.POST_CONTENT_BLOCKS).append(text_block);
    };

    create_bootstrap_alert(text) {
        let info_block = $("<div class='alert alert-info' title='Notice!' style='margin-top: 10px'></div>");
        let second_info_block = $("<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>×</button>");
        let third_info_block = $("<strong>Notice:</strong><span> " + text + "</span>");

        info_block.append(second_info_block);
        info_block.append(third_info_block);
        return info_block;
    };

    get_hr() {
        return $("<hr>")
    };

    add_in_queue(block) {
        block.attr('order', this.BLOCK_ITER);
        this.BLOCK_ITER++;
    };
}
