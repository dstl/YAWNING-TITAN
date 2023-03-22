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
        update_network(this,"UPDATE_NETWORK_DETAILS");
    });
    $("#doc-meta-form").on("change",function(){
        update_network(this,"UPDATE_NETWORK_METADATA");
    });
});


function update_network(form_element,operation){
    config = new FormData($(form_element)[0]);
    config.append("_network_id",NETWORK_ID);
    config.append('_operation',operation);

    /**
     * The network editor listens to NETWORK_SETTINGS
     * for any changes in the network metadata and the
     * randomisation settings
     *
     * Any updates to the form here will be reflected on the
     * POST body that the angular network editor sends to
     * .../network_editor/
     *
     * Don't do double requests - we can cause race conditions
     */
    proxy.NETWORK_SETTINGS = config;
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
