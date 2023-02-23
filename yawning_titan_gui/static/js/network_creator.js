$(document).ready(function(){
    $(".template .mb-3:not(:first-child)").hide();
    $(`.template .mb-3:has(.${$("select").val()})`).show();
    $("select[type-selector]").on("change",function(){
        console.log($(this).val());
        $(".template  .mb-3:not(:first-child)").hide();
        $(`.template  .mb-3:has(.${$(this).val()})`).show();
    });
    $(".template  .form-control").on("change",function(){
        if (check_form_filled(".template ."+$("select[type-selector]").val())){
            load_template($("#template-form"))
        }
    });
    $(".random-elements  .form-control").on("change",function(){
        update_network($("#random-elements-form"))
    });
    $("#save").click(function(){
        save_template()
    });
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
        }
    });
}

function save_template(){
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: {save:true}
    });
}
