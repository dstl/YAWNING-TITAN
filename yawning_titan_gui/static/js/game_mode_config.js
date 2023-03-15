$(window).on("unload", function(e) {
    localStorage.setItem('scrollpos', $(".form-container").scrollTop());
});

$(document).ready(function(){
    let scrollpos = localStorage.getItem('scrollpos');
    if (scrollpos)  $(".form-container").scrollTop(scrollpos);

    // set the initial value of show-hidden-dependents persisting through refreshes.
    $("#show-hidden-dependents").prop("checked",sessionStorage.getItem("show-hidden-dependents") || false);

    // check select dependencies on page load
    $("select").each(function(){
        $("."+$("option:selected",this).text().replaceAll(" ","_")).removeClass("hidden")
    });

    // update select dependencies
    $(document).on("change",".config-form select",function(){
        if($("show-hidden-dependents").is(":checked")){
            $(".grouped").addClass("hidden")
        }
        el =  $("."+$("option:selected",this).text().replaceAll(" ","_"));
        el.removeClass("hidden");
    });

    // update checkbox dependencies
    $(document).on("change",".config-form  .form-check-input",function(){
        let child_els = `.${$(this).get(0).classList[1]}:not(.parent)`;
        if($(this).is(":checked")){
            handle_dependent_elements(child_els,"activate")
        }else{
            handle_dependent_elements(child_els,"deactivate")
        }
    });

    // update input dependencies
    $(document).on("keyup",".config-form  .grouped.parent",function(){
        let child_els = `.${$(this).get(0).classList[1]}:not(.parent)`;
        if($(this).val().length > 0){
            handle_dependent_elements(child_els,"activate")
        }else{
            handle_dependent_elements(child_els,"deactivate")
        }
    });

    // form updates
    $("#save-game-mode").click(function(){
        save_game_mode();
    });

    $(".config-form").change(function(){
        submit_form(this,SECTION_NAME);
    });

    $("#doc-meta-form").change(function(){
        submit_form(this,"doc-meta");
    });

    $("#config-form-icons>.icon").click(function(){
        $("#config-form-icons>.icon").removeClass("selected")
        $(this).addClass("selected");
        $(".form-container").addClass("hidden");
        $($(this).data("form")).parent().removeClass("hidden");
    });
});

function save_game_mode(){
    config = new FormData();
    config.append('_game_mode_id',GAME_MODE_ID);
    config.append('_operation',"save");
    $.ajax({
        type: "POST",
        url: window.location.origin + "/update_game_mode/",
        data: config,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json"
    });

}

// wrapper for async post request for config section form processing
function submit_form(form_element,section_name){
    config = new FormData($(form_element)[0]);
    config.append('_form_id',$(form_element).data("id"));
    config.append('_section_name',section_name);
    config.append('_game_mode_id',GAME_MODE_ID);
    config.append('_operation',"update");
    $.ajax({
        type: "POST",
        url: window.location.origin + "/update_game_mode/",
        data: config,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json",
        success: function(response){
            $(form_element).find(".error-list").empty();
            if(response.valid){
                $(`.icon-container[data-section="${SECTION_NAME}"]`).addClass("complete");
            }
        },
        error: function(response){
            let errors = response.responseJSON.errors;
            add_form_errors(JSON.parse(errors));
        }
    });
}

function add_form_errors(errors){
    $(".error-list").remove(); // remove existing errors
    $(".erroneous").removeClass("erroneous"); // remove all erroneous settings
    $(`.icon-container[data-section="${SECTION_NAME}"]`).removeClass("complete"); // show section as incomplete
    for (const [form_id, error] of Object.entries(errors)){
        let group_error_list = $("<ul class='error-list'></ul>");

        for (const msg of error["group"]){
            group_error_list.append("<li>"+msg+"</li>")
        }
        $(`#config-form-${form_id}`).addClass("erroneous");
        $(".title-container",`#config-form-${form_id}`).append(group_error_list);
        for (const [item_id, item_errors] of Object.entries(error["items"])){
            let item_error_list = $("<ul class='error-list'></ul>");
            for (const msg of item_errors){
                item_error_list.append("<li>"+msg+"</li>")
            }
            let info_obj = $(`label[for='id_${item_id}']`,"#config-form-"+form_id).closest(".info");
            info_obj.children(".error-list").remove();
            info_obj.append(item_error_list);
        }
    }
}
