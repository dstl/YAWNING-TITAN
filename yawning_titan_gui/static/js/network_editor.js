$(document).ready(function(){

    $("#random-elements .form-check-input").on("change",function(){
        if($(this).is(":checked")){
            $(`#random-elements .mb-3:has(.form-control[${$(this).data("toggle")}])`).show();
        }else{
            $(`#random-elements .mb-3:has(.form-control[${$(this).data("toggle")}])`).hide();
        }
    });
    $("#random-elements .form-check-input").trigger("change"); // Trigger an initial change call on page ready to hide/show elements.

    //Open\close random elements menu
    $(".toolbar-button").click(function(){
        $(this).addClass("active");
        if($(this).hasClass("random-elements")){
            $("#random-elements").show()
        }else{
            $("#random-elements").hide()
        }
    })
});

$(window).on("load",function(){
    $("#random-elements-form").on("change",function(){
        update_network(this,"update");
    });
    $("#doc-meta-form").on("change",function(){
        update_network(this,"update doc meta");
    });
});


function update_network(form_element,operation){
    config = new FormData($(form_element)[0]);
    config.append("_network_id",NETWORK_ID);
    config.append('_operation',operation);
    console.log("UPDATE",NETWORK_ID,operation);
    $.ajax({
        type: "POST",
        url: UPDATE_URL,
        data: config,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json",
        success: function(response){
            console.log("UPDATED");
            if (response.network_json){
                proxy.NETWORK = response.network_json;
            }
        }
    });
}
