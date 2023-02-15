$(document).ready(function(){
    $(".template .mb-3:not(:first-child)").hide();
    $(`.template .mb-3:has(.${$("select").val()})`).show();
    $("select[type-selector]").on("change",function(){
        console.log($(this).val());
        $(".template  .mb-3:not(:first-child)").hide();
        $(`.template  .mb-3:has(.${$(this).val()})`).show();
    });
    $(".template  .form-control").on("change",function(){
        let update = true;
        $(".template ."+$("select[type-selector]").val()).each(function(){
            if($(this).val() == null){
                update = false
            }
        });
        if (update){
            load_template($("#network-creator-form"));
        }
    });
    $("#save").click(function(){
        save_template()
    });

    $(".random-elements .form-check-input").on("change",function(){
        if($(this).is(":checked")){
            $(`.random-elements .mb-3:has(.form-control[${$(this).data("toggle")}])`).show();
        }else{
            $(`.random-elements .mb-3:has(.form-control[${$(this).data("toggle")}])`).hide();
        }
    });
    $(".random-elements .form-check-input").trigger("change"); // Trigger an initial change call on page ready to hide/show elements.
});

function load_template(form_element){

    config = new FormData($(form_element)[0]);
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: config,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json",
        success: function(response){
            proxy.NETWORK = response.network_json;
            $("#open-editor").attr("href",EDITOR_URL + response.network_id);
        },
        error: function(response){
        }
    });
}

function save_template(){
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: {save:true},
        success: function(response){

        },
        error: function(response){
        }
    });
}
