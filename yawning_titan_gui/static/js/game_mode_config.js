$(document).ready(function(){
    // set the initial value of show-hidden-dependents persisting through refreshes.
    $("#show-hidden-dependents").prop("checked",sessionStorage.getItem("show-hidden-dependents") || false);
    toggle_show_hidden_dependents();

    // check select dependencies on page load
    $("select").each(function(){
        $("."+$("option:selected",this).text().replaceAll(" ","_")).removeClass("hidden")
    });

    $("input[type='checkbox'].grouped.parent").each(function(i,el){
        let child_el = `.${$(el).get(0).classList[1]}:not(.parent)`;
        if($(el).is(":checked")){
            $(el).addClass("checked");
            $(child_el).removeClass("hidden");
        }else{
            $(child_el).attr("disabled","disabled");
            $(child_el).closest(".mb-3").removeClass("active");
        }
    });

    $("input[type='text'].grouped.parent").each(function(){
        let child_el = `.${$(el).get(0).classList[1]}:not(.parent)`;
        if($(el).val().length > 0){
            $(el).addClass("checked");
            $(child_el).removeClass("hidden");
        }else{
            $(child_el).attr("disabled","disabled");
            $(child_el).closest(".mb-3").removeClass("active");
        }
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
    $(".config-form").change(function(){
        submit_form(this)
    });

    // buttons
    $("#show-hidden-dependents").click(function(){
        sessionStorage.setItem("show-hidden-dependents",$(this).is(":checked"));
        toggle_show_hidden_dependents();
    });

    $("#config-form-icons>.icon").click(function(){
        $("#config-form-icons>.icon").removeClass("selected")
        $(this).addClass("selected");
        $(".form-container").addClass("hidden");
        $($(this).data("form")).parent().removeClass("hidden");
    });
});


// wrapper for async post request for config section form processing
function submit_form(form_element){
    config = new FormData($(form_element)[0]);
    config.append('section_name',$(form_element).data("form-name"));
    config.append('game_mode_filename',game_mode_filename);
    $.ajax({
        type: "POST",
        url: window.location.origin + "/update_config/",
        data: config,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json",
        success: function(response){
            $("#error-message").text("").addClass("hidden");
            console.log("RE",response);
        },
        error: function(response){
            console.log("ERR",response);
            if("errors" in response.responseJSON){
                $("#error-message").text(response.responseJSON.errors).removeClass("hidden")
            }
        }
    });
}

// update dependent elements state
function handle_dependent_elements(selector, operation){
    if(operation == "activate"){
        $(selector).removeClass("hidden");
        $(selector).removeAttr("disabled");
        $(selector).closest(".mb-3").addClass("active");
    }else if(operation == "deactivate"){
        if($("show-hidden-dependents").is(":checked")){
            $(selector).addClass("hidden")
        }
        $(selector).attr("disabled","disabled");
        $(selector).closest(".mb-3").removeClass("active");
    }
}

// toggle the visibility of dependent child elements
function toggle_show_hidden_dependents(){
    if($("#show-hidden-dependents").is(":checked")){
        $(".config-form input.grouped:not(.parent)").removeClass("hidden");
        $("#show-hidden-dependents").closest(".el-container").find("label").text("Hide inactive options");
    }else{
        $(".config-form input.grouped:not(.parent)").addClass("hidden");
        $("#show-hidden-dependents").closest(".el-container").find("label").text("Show inactive options");
    }
}
