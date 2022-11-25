function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function update_tooltip(selector,replace,replace_with){
    $(selector).attr('data-bs-original-title',$(selector).data("bs-original-title").replace(replace,replace_with));
}

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
    $("input[role='switch']").wrap("<div class=form-switch></div>")

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            }
        }
    });
});

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
