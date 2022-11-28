$(document).ready(function(){
    //page variables
    let selected_game_mode;

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
    // check select dependencies on page load
    $("select").each(function(){
        $("."+$("option:selected",this).text().replaceAll(" ","_")).removeClass("hidden")
    });

    $(".form-check-input").each(function(){
        if($(this).is(":checked")){
            $(this).addClass("checked");
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).removeClass("hidden");
        }
    });

    $(".grouped.parent").each(function(){
        if($(this).val().length > 0){
            $(`.${$(this).get(0).classList[1]}:not(.parent)`).removeClass("hidden")
        }
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

    // wrapper for async post request for config section form processing
    function submit_form(form_element){
        config = new FormData($(form_element)[0]);
        config.append('form_name',$(form_element).data("form-name"));
        return $.ajax({
            type: "POST",
            url: window.location.href,
            data: config,
            processData: false,
            contentType: false,
            cache: false,
            dataType: "json"
        });
    }

    // ajax post request and attached reload callback
    function submit_game_mode(game_mode_name,operation,additional_params={}){
        if (game_mode_name.length > 0){
            $.ajax({
                type: "POST",
                url: "/manage_config/",
                data: Object.assign({},{"game_mode_name":game_mode_name,"operation":operation},additional_params),
            }).done(function(){
                location.reload();
            });
        }
    }

    $("#config-form-icons>.icon").click(function(){
        $("#config-form-icons>.icon").removeClass("selected")
        $(this).addClass("selected");
        $(".form-container").addClass("hidden");
        console.log("TT",$(this).data("form"));
        $($(this).data("form")).parent().removeClass("hidden");
    });

    // button actions
    $("#game-config-submit").click(function(){
        $(".config-form").each(function(){
            submit_form(this);
        });
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
