$(document).ready(function(){
    $("#template-form .mb-3:not(:first-child)").hide();
    $(`#template-form .mb-3:has(.${$("select").val()})`).show();
    $("select[type-selector]").on("change",function(){
        $(".template  .mb-3:not(:first-child)").hide();
        $(`.template  .mb-3:has(.${$(this).val()})`).show();
    });
    $("#template-form  .form-control").on("change",function(){
        if (check_form_filled(".template ."+$("select[type-selector]").val())){
            load_template($("#template-form"))
        }
    });
    $(".network-details  .form-control").on("change",function(){
        update_network($("#network-details-form"))
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
