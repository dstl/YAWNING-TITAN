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

    $("#config-form-icons>.icon").click(function(){
        $("#config-form-icons>.icon").removeClass("selected")
        $(this).addClass("selected");
        $(".form-container").addClass("hidden");
        console.log("TT",$(this).data("form"));
        $($(this).data("form")).parent().removeClass("hidden");
    });

    // $(".next-form").click(function(){
    //     let el = this,
    //         next_form_el = $(this).data("next-form-el");

    //     submit_form($(this).siblings(".config-form")).done(function(response){
    //         $("#error-message").addClass("hidden");
    //         $(el).closest(".form-container").addClass("hidden"); //hide current form container
    //         $(next_form_el).parent().removeClass("hidden");  //show next form container
    //         $("#config-form-icons>.icon").removeClass("selected"); //deselect current icon
    //         $(`#${$(next_form_el).data("form-name")}-icon`).addClass("selected"); //select next icon
    //     }).fail(function(response){
    //         console.log("ERR",JSON.parse(response.responseText));
    //         $("#error-message").removeClass("hidden").text("Error: " + JSON.parse(response.responseText)["message"]);
    //     })
    // });

    //Button actions
    $("#game-config-submit").click(function(){
        $(".config-form").each(function(){
            submit_form(this);
        });
    });

    $("#create-game-mode").click(function(){
        toggle_dialogue("#create-dialogue");
    });

    $("#create-dialogue .submit").click(function(){
        let game_mode_name = $(this).closest(".dialogue-center").find("input").first().val();
        if (game_mode_name.length > 0){
            $.ajax({
                type: "POST",
                url: "/manage_config/",
                data: {"game_mode_name":game_mode_name,"operation":"create"},
            }).done(function(){
                location.reload();
            });
        }
    });

    $("#delete-dialogue .submit").click(function(){
        $.ajax({
            type: "POST",
            url: "/manage_config/",
            data: {"game_mode_name":selected_game_mode,"operation":"delete"},
        }).done(function(){
            location.reload();
        });
    });

    $(".icon.delete").click(function(e){
        e.stopPropagation();
        toggle_dialogue("#delete-dialogue");
        $("#delete-dialogue h3").text("Delete " + $(this).closest(".game-mode").find(".subhead").first().text());
        selected_game_mode = $(this).closest(".game-mode").data("game-mode-name");
    });


});
