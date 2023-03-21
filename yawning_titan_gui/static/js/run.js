$(document).ready(function(){
    let selected = {
        "game_mode":null,
        "network":null
    }
    $("#field-menu button").click(function(){
        $(this).siblings("button").removeClass("btn-primary");
        $(this).addClass("btn-primary");
        $(".run-fieldset").hide();
        $($(this).data("form")).show();
    });
    $(".list-item").click(function(){
        $(this).closest(".grid-item").find(".list-item").removeClass("selected");
        $(this).addClass("selected");
        selected[$(this).closest(".grid-item").data("type")] = $(this).data("item-id");
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

    console.log("OUTPUT",OUTPUT_URL);

    //setup on start
    $("#view-buttons button:first-child").addClass("selected");
    $(".run-subsection:first-child").show();
});


let interval;

// wrapper for async post request for managing YT run instance
function run(data){
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: data,
        processData: false,
        contentType: false,
        cache: false,
        dataType: "json",
        success: function(response){
            console.log("FINISHED");
            // clearInterval(interval);
        },
        error: function(response){
            console.log(response.message)
        }
    });
    interval = setInterval(get_output,500);
}

function get_output(){
    $.ajax({
        type: "GET",
        url: OUTPUT_URL,
        cache: false,
        dataType: "json",
        success: function(response){
            console.log("RESPONSE",response);
            let stderr_out = $("#log-view>.inner"),
                stdout_out = $("#metric-view>.inner");

            $(stderr_out).html(response.stderr);
            $(stdout_out).html(response.stdout);

            $(stderr_out).scrollTop($(stderr_out).get(0).scrollHeight);
            $(stdout_out).scrollTop($(stdout_out).get(0).scrollHeight);

            if(!response.active & response.request_count > 100){
                console.log("FINISHED!!!");
                $("#gif-output").show();
                $("#gif-output").attr("src",response.gif);
                clearInterval(interval);
            }
        }
    });
}
