// used to poll for data
let interval;

// keeps track of whether or not there is a current run
let isRunning = false;

$(document).ready(function () {
    let selected = {
        "game_mode": null,
        "network": null
    };
    enable_run_form(true);
    updateRunValidity();
    $("#field-menu button").click(function () {
        $(this).siblings("button").removeClass("btn-primary");
        $(this).addClass("btn-primary");
        $(".run-fieldset").hide();
        $($(this).data("form")).show();
    });
    $(".list-item").click(function () {
        // the type of grid item that was clicked
        let type = $(this).closest(".list-container").data("type");

        // remove the previously selected item
        $(this).closest(".grid-item").find(".list-item").removeClass("selected");

        // check if item was already selected
        if ($(this).data("item-id") != selected[type] && !$(this).hasClass("incompatible")) {
            // highlight selected item
            $(this).addClass("selected");
            selected[type] = $(this).data("item-id");
        } else {
            selected[type] = null;
        }

        // check for game mode compatibility if the user selects a network
        if (type == "network") {
            if (!selected.network) {
                // clear selected
                selected[type] = null;
                // remove the incompatible class from all game modes
                resetCompatibilities()
                return;
            }

            get_game_modes_compatible_with($(this).data("item-id")).then(res => {
                // iterate over all game mode items
                for (const game_mode of $("#game-modes-container .list-item")) {
                    const el = $(game_mode)

                    // check if the game mode is in the compatible list
                    if (res.game_mode_ids.some(gm => gm == el.data("itemId"))) {
                        resetCompatibilities(el);
                        continue;
                    }

                    // add tooltip to game mode
                    el.tooltip("enable");

                    // deselect
                    selected["game_mode"] = null
                    el.removeClass("selected");

                    // mark as incompatible
                    el.addClass("incompatible");
                }
            })
                .then(() => updateRunValidity());
        }
        updateRunValidity();
    });
    $("#run-form").submit(function (e) {
        e.preventDefault();
        data = new FormData(this);
        data.append("game_mode", selected["game_mode"]);
        data.append("network", selected["network"]);
        run(data);
    });
    $("#stderr").click(function () {
        stderr();
    });
    $("#view-buttons button").click(function () {
        $(".run-subsection").hide();
        $("#view-buttons button").removeClass("selected");
        $(this).addClass("selected");
        $($(this).data("toggle")).show();
    });

    //setup on start
    $("#view-buttons button:first-child").addClass("selected");
    $(".run-subsection:first-child").show();
    $("#gif-spinner-container").hide();

    // add tooltip to each game mode item
    $("#game-modes-container .list-item").each(function (el) {
        $(this).tooltip({
            html: true,
            title: "Game Mode is incompatible with selected network",
            placement: "bottom"
        });
        $(this).tooltip("disable");
    })

    /**
     * Function used to check
     */
    function updateRunValidity() {
        // check if there are values for game_mode and network
        selGameMode = $("#game-modes-container .list-item").hasClass("selected");
        selNetwork = $("#networks-container .list-item").hasClass("selected");
        enable_run_form(!(selGameMode && selNetwork));
    }

    /**
     * Resets the compatibility status of all game modes
     */
    function resetCompatibilities(el) {
        if (!el) {
            el = $("#game-modes-container .list-item")
        }

        el.removeClass("incompatible");
        el.tooltip("disable");
        updateRunValidity();
    }
});

/**
 * Function that triggers a YT run
 * @param {*} data 
 */
function run(data) {
    $("#open-gif").hide();
    isRunning = true;

    // clear logs
    $("#log-view>.inner").empty();
    $("#metric-view>.inner").empty();

    if (data.get("render") == "on") {
        $("#gif-spinner-container").css({ display: "flex" });
    }

    // deactivate the input form
    $("#run-form input").prop("disabled", true);
    $("#run").prop("disabled", true);
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json",
        error: function (response) {
            console.error(response.message);
            enable_run_form();
        }
    })
        .done(() => interval = setInterval(get_output, 500))
}

/**
 * Function used to deal with incompatibilities between networks and game modes
 * @param {*} network_id 
 */
function get_game_modes_compatible_with(network_id) {
    return $.ajax({
        type: "GET",
        url: FILE_MANAGER_URL,
        data: { "network_id": network_id },
        dataType: "json",
        error: function (response) {
            console.error(response.message);
            enable_run_form();
        }
    });
}

function enable_run_form(disable) {
    $("#run-form input").prop("disabled", disable || isRunning);
    $("#run").prop("disabled", disable || isRunning);
}

function get_output() {
    $.ajax({
        type: "GET",
        url: OUTPUT_URL,
        cache: false,
        dataType: "json",
        success: function (response) {
            let stderr_out = $("#log-view>.inner"),
                stdout_out = $("#metric-view>.inner");

            $(stderr_out).html(response.stderr);
            $(stdout_out).html(response.stdout);

            $(stderr_out).scrollTop($(stderr_out).get(0).scrollHeight);
            $(stdout_out).scrollTop($(stdout_out).get(0).scrollHeight);
        },
        error: function () {
            enable_run_form();

            // stop polling
            clearInterval(interval);
            $("#gif-spinner-container").hide();
            isRunning = false;
        }
    })
        .done(res => {
            // show gif only if a gif returned in the payload
            if (res.gif && res.request_count > 20) {
                $("#gif-spinner-container").hide();

                // stop polling
                clearInterval(interval);

                $("#gif-output").css({ display: 'flex' });
                $("#gif-output").css({
                    backgroundImage: `url(..${res.gif}?${Math.random()})`,
                    backgroundSize: 'contain',
                    width: '100%',
                    height: '100%',
                });

                $("#open-gif").attr("href", `..${res.gif}?${Math.random()}`)
                $("#open-gif").show();
                isRunning = false;
            }

            if (!res.active && interval) {
                clearInterval(interval);
                isRunning = false;
            }

            enable_run_form();
        })
}
