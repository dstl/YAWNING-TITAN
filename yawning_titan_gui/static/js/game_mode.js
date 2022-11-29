$(document).ready(function(){
    //page variables
    let selected_game_mode;

    $("#filter-game-modes").keyup(function(){
        $(".game-mode").removeClass("hidden");
        $(".game-mode").find(".subhead:not(:contains(" + $(this).val() + "))").closest(".game-mode").addClass("hidden");
    });

    // dialogue launchers
    $("#create-game-mode").click(function(){
        toggle_dialogue("#create-dialogue");
    });

    $(".icon.delete").click(function(e){
        e.stopPropagation();
        toggle_dialogue("#delete-dialogue");
        selected_game_mode = $(this).closest(".game-mode").data("game-mode-name");
        $("#delete-dialogue .header").text("Delete " + selected_game_mode);

    });

    $(".icon.create-from").click(function(e){
        e.stopPropagation();
        toggle_dialogue("#create-from-dialogue");
        selected_game_mode = $(this).closest(".game-mode").data("game-mode-name");
        console.log("TXT",$("#create-from-dialogue .header").text());
        $("#create-from-dialogue .header").text($("#create-from-dialogue .header").text() + " " + selected_game_mode);
    });

    // dialogue submit functions

    $("#create-dialogue .submit").click(function(){
        let game_mode_name = $(this).closest(".dialogue-center").find("input").first().val();
        submit_game_mode(game_mode_name, "create");
    });

    $("#create-from-dialogue .submit").click(function(){
        let game_mode_name = $(this).closest(".dialogue-center").find("input").first().val();
        submit_game_mode(game_mode_name, "create from",{"source_game_mode":selected_game_mode});
    });

    $("#delete-dialogue .submit").click(function(){
        submit_game_mode(selected_game_mode, "delete");
    });
});
