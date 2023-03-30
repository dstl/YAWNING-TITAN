$(document).ready(function(){
    let selected = {
        "game_mode":null,
        "network":null
    };
    $("#field-menu button").click(function(){
        $(this).siblings("button").removeClass("btn-primary");
        $(this).addClass("btn-primary");
        $(".run-fieldset").hide();
        $($(this).data("form")).show();
    });
    $(".list-item").click(function(){
        $(this).closest(".grid-item").find(".list-item").removeClass("selected");
        $(this).addClass("selected");
        let type = $(this).closest(".list-container").data("type");
        selected[type] = $(this).data("item-id");
        console.log("000",type,$(this).data("item-id"));
        if(type == "network"){
            get_game_modes_compatible_with($(this).data("item-id"))
        }
    });
    $("#run-form").submit(function(e){
        e.preventDefault();
        data = new FormData(this);
        data.append("game_mode",selected["game_mode"]);
        data.append("network",selected["network"]);
        run(data);
    });
    $("#stderr").click(function(){
        stderr();
    });
    $("#view-buttons button").click(function(){
        $(".run-subsection").hide();
        $("#view-buttons button").removeClass("selected");
        $(this).addClass("selected");
        $($(this).data("toggle")).show();
    });

    //setup on start
    $("#view-buttons button:first-child").addClass("selected");
    $(".run-subsection:first-child").show();
});


let interval;

// wrapper for async post request for managing YT run instance
function run(data){
    // deactivate the input form
    console.log("RUN");
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
        error: function(response){
            console.log(response.message);
            enable_run_form();
        }
    });
    interval = setInterval(get_output,500);
}

function get_game_modes_compatible_with(network_id){
    console.log("LOOKING");
    $.ajax({
        type: "GET",
        url: FILE_MANAGER_URL,
        data: {"network_id":network_id},
        // processData: false,
        // contentType: false,
        // cache: false,
        dataType: "json",
        success: function(response){
            $("#game-modes-container .list-item").hide();
            for(const id of response.game_mode_ids){
                $(`.list-item[data-item-id=${id}]`).show()
            }
        },
        error: function(response){
            console.log(response.message);
            enable_run_form();
        }
    });
}

function enable_run_form(){
    $("#run-form input").prop("disabled", false);
    $("#run").prop("disabled", false);
}

function get_output(){
    $.ajax({
        type: "GET",
        url: OUTPUT_URL,
        cache: false,
        dataType: "json",
        success: function(response){
            let stderr_out = $("#log-view>.inner"),
                stdout_out = $("#metric-view>.inner");

            $(stderr_out).html(response.stderr);
            $(stdout_out).html(response.stdout);

            $(stderr_out).scrollTop($(stderr_out).get(0).scrollHeight);
            $(stdout_out).scrollTop($(stdout_out).get(0).scrollHeight);

            if(!response.active & response.request_count > 100){
                console.log("FINISHED!!!",response.gif);
                enable_run_form();
                // show gif only if a gif returned in the payload
                if(response.gif){
                    $("#gif-output").show();
                    $("#gif-output").attr("src",response.gif);
                }
                clearInterval(interval);
            }
        }
    });
}
