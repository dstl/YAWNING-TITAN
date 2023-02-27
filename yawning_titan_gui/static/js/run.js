$(document).ready(function(){
    let selected = {
        "game_mode":null,
        "network":null
    }
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
    })
});

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
            console.log(response.stdout);
            $("#run-view").html(response.stdout);
        },
        error: function(response){
            console.log(response.message)
        }
    });
}

function stderr(data){
    $.ajax({
        type: "GET",
        url: STDERR_URL,
        data: data,
        //cache: false,
        dataType: "json",
        success: function(response){
            console.log("STDERR",response.stderr);
        }
    });
}
