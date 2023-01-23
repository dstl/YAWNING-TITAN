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
    //close center dialogue
    $(".dialogue-center .cancel").click(function(){
        toggle_dialogue($(this).closest(".dialogue-center"))
    });

    $("#main").click(function(){$("#sidebar-left, #sandwich-icon").removeClass("open")});

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
            }
        }
    });
});

class Filter{
    constructor(){
        this.hidden = {};
    }
    update_elements(){
        $(".list-item").removeClass("hidden");
        // console.log("TESTING 123",this.hidden);
        for (const [group,elements] of Object.entries(this.hidden)){
            elements.each(function(){
                $(this).addClass("hidden")
            })
        }
    }
    set(elements,group){
        this.hidden[group] = elements
    }
}
const item_filter = new Filter();
