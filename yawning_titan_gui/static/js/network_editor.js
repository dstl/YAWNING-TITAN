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

$(window).on("load", function () {
    $("#network-randomisation-form .form-check-input, #network-randomisation-form .form-control").on("change", function () {
        update_network($("#network-randomisation-form"));
    });

});


function update_network(form_element) {
    config = new FormData($(form_element)[0]);
    config.append("_network_id", NETWORK_ID);
    proxy.NETWORK_SETTINGS = config;
}

function toggleToolbar(iconEl) {
    // hide all sidebars
    $("#network-randomisation").hide()
    $("#node-list").hide()

    // if icon clicked is network-randomisation
    if (iconEl.hasClass("network-randomisation") && iconEl.hasClass("active")) {
        $("#network-randomisation").show()
    } else {
        $("#network-randomisation").hide()
    }

    // if icon clicked is node-list
    if (iconEl.hasClass("node-list") && iconEl.hasClass("active")) {
        $("#node-list").show()
    } else {
        $("#node-list").hide()
    }
}