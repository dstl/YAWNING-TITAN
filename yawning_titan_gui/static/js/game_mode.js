$(document).ready(function(){
    console.log("TEST");
    $("#filter-game-modes").keyup(function(){
        console.log($(".game-mode").find(".subhead:contains(" + $(this).val() + ")"),".subhead:contains(" + $(this).val() + ")");
        $(".game-mode").removeClass("hidden");
        $(".game-mode").find(".subhead:not(:contains(" + $(this).val() + "))").closest(".game-mode").addClass("hidden");
    });

    $(".game-mode.selectable").click(function(){   
        console.log($("#game-mode-set").data("bs-original-title").replace("incomplete","complete"));
        if($(this).hasClass("selected")){
            $(this).removeClass("selected");
            $("#game-mode-set").removeClass("complete");
            update_tooltip("#game-mode-set","complete","incomplete");
        }else{
            $(".game-mode").removeClass("selected");
            $(this).addClass("selected");
            $("#game-mode-set").addClass("complete");
            update_tooltip("#game-mode-set","incomplete","complete");
        }               
    });

    $(".icon.delete").click(function(e){
        e.stopPropagation();
        toggle_dialogue("#delete-dialogue");
        $("#delete-dialogue h3").text("Delete " + $(this).closest(".game-mode").find(".subhead").first().text());
    });
});
