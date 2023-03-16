$(document).ready(function () {

    $("#network-details .form-check-input").on("change", function () {
        if ($(this).is(":checked")) {
            $(`#network-details .mb-3:has(.form-control[${$(this).data("toggle")}])`).show();
        } else {
            $(`#network-details .mb-3:has(.form-control[${$(this).data("toggle")}])`).hide();
        }
    });
    $("#network-details .form-check-input").trigger("change"); // Trigger an initial change call on page ready to hide/show elements.

    //Open\close random elements menu
    $(".network-sidenav-navigation-btn").click(function () {
        toggleToolbar($(this));
    });

    // open the first tab item on load
    $(".network-sidenav-navigation-btn:first").trigger("click");
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

function toggleToolbar(iconEl) {
    // remove active from all icons
    $(".network-sidenav-navigation-btn").removeClass("active");

    // add active class to icon
    $(iconEl).addClass("active")

    // hide all sidebars
    $("#network-details").hide();
    $("#node-list").hide();

    // open the relevant item
    $($(iconEl).data("item")).css('display', 'flex');
}
