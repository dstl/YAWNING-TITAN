function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$(document).ready(function(){
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