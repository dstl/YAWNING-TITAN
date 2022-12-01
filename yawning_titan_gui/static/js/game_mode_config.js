$(document).ready(function(){
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
