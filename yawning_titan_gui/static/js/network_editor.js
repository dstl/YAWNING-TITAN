$(document).ready(function () {

    $("#network-randomisation .form-check-input").on("change", function () {
        if ($(this).is(":checked")) {
            $(`#network-randomisation .mb-3:has(.form-control[${$(this).data("toggle")}])`).show();
        } else {
            $(`#network-randomisation .mb-3:has(.form-control[${$(this).data("toggle")}])`).hide();
        }
    });
    $("#network-randomisation .form-check-input").trigger("change"); // Trigger an initial change call on page ready to hide/show elements.

    //Open\close random elements menu
    $(".toolbar-button").click(function () {
        toggleToolbar($(this));
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
    $.ajax({
        type: "POST",
        url: UPDATE_URL,
        data: config,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json",
        success: function(response){
            if (response.network_json){
                proxy.NETWORK = response.network_json;
            }
        }
    });
}

function toggleToolbar(iconEl) {
    // hide all sidebars
    $("#network-randomisation").hide();
    $("#node-list").hide();

    // if icon clicked is network-randomisation
    $($(iconEl).data("toolbar")).show();
}
