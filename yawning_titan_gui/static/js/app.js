function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function update_tooltip(selector,replace,replace_with){
    $(selector).attr('data-bs-original-title',$(selector).data("bs-original-title").replace(replace,replace_with));
}

function toggle_dialogue(dialogue_selector){
    if($("#mask").hasClass("hidden")){
        $("#mask").removeClass("hidden");
        $(dialogue_selector).removeClass("hidden");
        $("#window").addClass("blur");
    }else{
        $("#mask").addClass("hidden");
        $("#mask>*").addClass("hidden");
        $("#window").removeClass("blur");
    }
}

$(window).on('load', function(){
    $("body").removeClass("preload");
});

$(document).ready(function(){
    $('[data-toggle="tooltip"]').tooltip();

    $('#sandwich-icon').click(function(){
		$(this).toggleClass('open');
        $($(this).data("sidebar")).toggleClass('open');
	});

    $(".dialogue-center .cancel").click(function(){
        toggle_dialogue($(this).closest(".dialogue-center"))
    });

    // create toggle switches from checkboxes
    $("input[role='switch']").wrap("<div class=form-switch></div>");

    // add range setter input field
    $("input[type='range']").wrap("<div class=form-range></div>");
    $(".form-range").append("<input type='number' class='form-control range-setter'>");

    // constrain range setter input field
    $(".range-setter").each(function(){
        let slider_el = $(this).closest(".form-range").children("input[type='range']").first();
        $(this).prop("min",slider_el.prop("min"));
        $(this).prop("max",slider_el.prop("max"));
        $(this).val(slider_el.val());
    })

    $(document).on("keyup",".range-setter",function(){
        $(this).closest(".form-range").children("input[type='range']").first().val($(this).val());
    })

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            }
        }
    });
});
