$(document).ready(function(){
    // create toggle switches from checkboxes
    $("input[role='switch']").wrap("<div class=form-switch></div>");

    // add range setter input field
    $("input[type='range']").wrap("<div class=form-range></div>");
    $(".form-range").append("<input type='number' class='range-setter'>");

    // constrain range setter input field
    $(".range-setter").each(function(){
        let slider_el = $(this).closest(".form-range").children("input[type='range']").first();
        $(this).prop("min",slider_el.prop("min"));
        $(this).prop("max",slider_el.prop("max"));
        $(this).prop("step",slider_el.prop("step"));
        $(this).val(slider_el.val());
    })

    // implement cross updates between range-setter and range sliders
    $(document).on("keyup",".range-setter",function(){
        $(this).siblings("input[type='range']").first().val($(this).val());
    });
    $(document).on("mousemove","input[type='range']",function(){
        $(this).siblings(".range-setter").first().val($(this).val());
    });
 
    // check select dependencies on page load
    $("select").each(function(){
        $("."+$("option:selected",this).text().replaceAll(" ","_")).removeClass("hidden")
    });

    $("input[type='checkbox'].grouped.parent").each(function(){
        if($(this).is(":checked")){
            $(this).addClass("checked");
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).removeClass("hidden");
        }
    });

    $("input[type='text'].grouped.parent").each(function(){
        if($(this).val().length > 0){
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).removeClass("hidden")
        }
    });

    // update select dependencies
    $(document).on("change","select",function(){
        $(".grouped").addClass("hidden");
        el =  $("."+$("option:selected",this).text().replaceAll(" ","_"));
        el.removeClass("hidden");
    });

    // update checkbox dependencies
    $(document).on("change",".form-check-input",function(){
        if($(this).is(":checked")){
            $(this).addClass("checked");
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).removeClass("hidden");
        }else{
            $(this).removeClass("checked");
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).addClass("hidden");
        }
    });

    // update input dependencies
    $(document).on("keyup",".grouped.parent",function(){
        if($(this).val().length > 0){
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).removeClass("hidden")
        }else{
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).addClass("hidden")
        }
    });

    // wrapper for async post request for config section form processing
    function submit_form(form_element){
        config = new FormData($(form_element)[0]);
        config.append('form_name',$(form_element).data("form-name"));
        return $.ajax({
            type: "POST",
            url: window.location.href,
            data: config,
            processData: false,
            contentType: false,
            cache: false,
            dataType: "json"
        });
    }

    $("#config-form-icons>.icon").click(function(){
        $("#config-form-icons>.icon").removeClass("selected")
        $(this).addClass("selected");
        $(".form-container").addClass("hidden");
        console.log("TT",$(this).data("form"));
        $($(this).data("form")).parent().removeClass("hidden");
    });

    // button actions
    $("#game-config-submit").click(function(){
        $(".config-form").each(function(){
            submit_form(this);
        });
    });
});
