function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function check_form_filled(selector) {
    let update = true;
    $(selector).each(function () {
        if ($(this).val() == null) {
            update = false
        }
    });
    return update
}

function update_tooltip(selector, replace, replace_with) {
    $(selector).attr('data-bs-original-title', $(selector).data("bs-original-title").replace(replace, replace_with));
}

function toggle_dialogue(dialogue_selector) {
    if ($("#mask").hasClass("hidden")) {
        $("#mask").removeClass("hidden");
        $(dialogue_selector).removeClass("hidden");
        $("#window").addClass("blur");
    } else {
        $("#mask").addClass("hidden");
        $("#mask>*").addClass("hidden");
        $("#window").removeClass("blur");
    }
}

$(window).on('load', function () {
    $("body").removeClass("preload");
});

$(document).ready(function(){

    $('[data-toggle="tooltip"]').tooltip();

    //toolbar
    $('#sandwich-icon').click(function(){
		$(this).toggleClass('open');
        $($(this).data("toolbar")).toggleClass("open");
	});
    $("#toolbar .toolbar-button").click(function(){
        $(this).siblings(".toolbar-button").removeClass("show");
        $(this).toggleClass("show");
        if(!$(this).closest("*[toolbar]").hasClass("open") | $(this).find(".toolbar-links").length == 0){
            window.location.href = $(this).data("href")
        }
    });


    //close center dialogue
    $(".dialogue-center .cancel").click(function () {
        toggle_dialogue($(this).closest(".dialogue-center"))
    });

    // create toggle switches from checkboxes
    $("input[role='switch']").wrap("<div class=form-switch></div>");

    // add range setter input field
    $("input[type='range'].form-range").wrap("<div class='form-range-container'></div>");
    // $("input[type='range'].form-range").wrap("<div class=form-range></div>");
    $(".form-range-container").append("<input type='number' class='range-setter form-control'>");

    // constrain range setter input field
    $(".range-setter").each(function(){
        let slider_el = $(this).closest(".form-range-container").children("input[type='range']").first();
        $(this).prop("min",slider_el.prop("min"));
        $(this).prop("max",slider_el.prop("max"));
        $(this).prop("step",slider_el.prop("step"));
        $(this).val(slider_el.val());
    })

    // implement cross updates between range-setter and range sliders
    $(document).on("change",".range-setter",function(){
        $(this).siblings("input[type='range']").first().val($(this).val());
        $(this).siblings("input[type='range'].slider-progress").first().css("--value",$(this).val()); // update slider progress value
    });
    $(document).on("mousemove", "input[type='range']", function () {
        $(this).siblings(".range-setter").first().val($(this).val());
    });

    setup_form_range();
    setup_form_multi_range();

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            }
        }
    });
});

class Filter {
    constructor() {
        this.hidden = {};
    }
    update_elements() {
        $(".list-item").removeClass("hidden");
        for (const [group, elements] of Object.entries(this.hidden)) {
            elements.each(function () {
                $(this).addClass("hidden")
            })
        }
    }
    set(elements, group) {
        this.hidden[group] = elements
    }
}
const item_filter = new Filter();


function setup_form_range(){
    $('input[type="range"].slider-progress').each(function(i,el){
        console.log("EL",el);
        $(el).css({
            "--value":el.value,
            '--min': el.min == '' ? '0' : el.min,
            '--max': el.max == '' ? '100' : el.max
        });
        $(el).on("input",function(){
            $(this).css("--value",el.value);
        });
    });
}

function setup_form_multi_range(){
    $(".multi-range-placeholder").each(function(i,el){
        let min = $(el).attr("min"),
            max = $(el).attr("max"),
            step = Math.pow(10, Math.floor(Math.log10((max-min)))) / 20,
            _class = $(el).attr("class"),
            name = $(el).attr("name").replace(/(_min$)/, '');
        $(el).replaceWith(
            `
            <div class="multi-range ${_class}" name="${name}">
                <input class="range-setter left" type="number" value="${min}" min="${min}" max="${max}" step="${step}">
                <div class="slider slider-distance">
                    <div class="slider-container">
                        <div class="inverse-left" style="width:70%;"></div>
                        <div class="inverse-right" style="width:70%;"></div>
                        <div class="range" style="left:30%;right:40%;"></div>
                        <span class="thumb" style="left:30%;"></span>
                        <span class="thumb" style="left:60%;"></span>
                    </div>
                    <input class="multi-range-input left" type="range" tabindex="0" value="${min}" max="${max}" min="${min}" step="${step}" />
                    <input class="multi-range-input right" type="range" tabindex="0" value="${max}" max="${max}" min="${min}" step="${step}"/>
                </div>
                <input class="range-setter right" type="number" value="${max}" min="${min}" max="${max}" step="${step}">
            </div>
            `
        );
    });
    $(".multi-range").removeClass("multi-range-placeholder");

    // set multi range sliders on load
    $(".multi-range-input.left").each(function(i,el){
        update_multi_range_left(el);
    });
    $(".multi-range-input.right").each(function(i,el){
        update_multi_range_right(el);
    });

    // update multi range sliders on input
    $(".multi-range-input.left, .multi-range .range-setter.left").on('input',function(){
        let multi_range_el = $(this).closest(".multi-range"),
            left_slider = $(".multi-range-input.left",multi_range_el);
        left_slider.val($(this).val()); // set the range slider value to itself if `this` is slider el otherwise set to the value of the input
        update_multi_range_left(left_slider.get(0));
    });

    $(".multi-range-input.right, .multi-range .range-setter.right").on('input',function(){
        let multi_range_el = $(this).closest(".multi-range"),
            right_slider = $(".multi-range-input.right",multi_range_el);
        right_slider.val($(this).val()); // set the range slider value to itself if `this` is slider el otherwise set to the value of the input
        update_multi_range_right(right_slider.get(0));
    });
}

function update_multi_range_right(el){
    let multi_range_el = $(el).closest(".multi-range"),
        value = Math.max(
            $(el).val(),$(el).siblings(".multi-range-input").val()
        ),
        children = $(".slider-container",multi_range_el).children();


    if($(multi_range_el).hasClass("integer")){
        value = Math.round(value);
    }
    percent = (100/(parseFloat(el.max)-parseFloat(el.min)))*value-(100/(parseFloat(el.max)-parseFloat(el.min)))*parseFloat(el.min);

    $(el).val(value);

    $(children.get(1)).css("width",(100-percent)+"%");
    $(children.get(2)).css("right",(100-percent)+'%');
    $(children.get(4)).css("left",percent+'%');
    $(".range-setter.right",multi_range_el).val($(el).val());
}

function update_multi_range_left(el){
    let multi_range_el = $(el).closest(".multi-range"),
        value = Math.min(
            $(el).val(),$(el).siblings(".multi-range-input").val()
        ),
        children = $(".slider-container",multi_range_el).children();

    if($(multi_range_el).hasClass("integer")){
        value = Math.round(value);
    }

    let percent = (100/(parseFloat(el.max)-parseFloat(el.min)))*value-(100/(parseFloat(el.max)-parseFloat(el.min)))*parseFloat(el.min);

    $(el).val(value);
    $(children.get(0)).css("width",percent+"%");
    $(children.get(2)).css("left",percent+'%');
    $(children.get(3)).css("left",percent+'%');
    $(".range-setter.left",multi_range_el).val($(el).val());
}
