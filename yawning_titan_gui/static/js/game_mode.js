$(document).ready(function(){
    console.log("TEST");
    $("#filter-game-modes").keyup(function(){
        $(".game-mode").removeClass("hidden");
        $(".game-mode").find(".subhead:not(:contains(" + $(this).val() + "))").closest(".game-mode").addClass("hidden");
    });

    $(".game-mode.selectable").click(function(){   
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

    // update select dependencies 
    $(document).on("change","select",function(){
        $(".grouped").addClass("hidden");
        el =  $("."+$("option:selected",this).text().replaceAll(" ","_"));
        el.removeClass("hidden");
    });

    // update checkbox dependencies
    $(document).on("change",".form-check-input",function(){
        if($(this).is(":checked")){
            $(this).addClass("checked");
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).removeClass("hidden");
        }else{
            $(this).removeClass("checked");
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).addClass("hidden");
        }
    });

    // update input dependencies
    $(document).on("keyup",".grouped.parent",function(){
        if($(this).val().length > 0){
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).removeClass("hidden")
        }else{
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).addClass("hidden")
        }
    });

    $("#game-config-submit").click(function(){
        $.ajax()
    });

});
