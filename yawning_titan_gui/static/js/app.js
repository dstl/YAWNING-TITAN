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
    
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            }
        }
    });
});