//page variables
let selected_item_names = [],
    selected_item_ids = [];

$(document).ready(function(){
    $("#filter-list-items").keyup(function(){
        $(".list-item").removeClass("hidden");
        $(".list-item").find(".subhead:not(:contains(" + $(this).val() + "))").closest(".list-item").addClass("hidden");
    });

    // dialogue launchers
    $("#create").click(function(){
        toggle_dialogue("#create-dialogue");
    });

    $("#delete-all").click(function(){
        $("#delete-dialogue .header").text(`Delete all (${$('.form-check-input:checkbox:checked').length}) items`);
        selected_item_names = $(".list-item:has(.form-check-input:checkbox:checked)").map(function(){return $(this).attr("data-item-name")}).get();
        selected_item_ids = $(".list-item:has(.form-check-input:checkbox:checked)").map(function(){return $(this).attr("data-item-id")}).get();
        toggle_dialogue("#delete-dialogue");
    });

    $(".icon.delete").click(function(e){
        e.stopPropagation();
        toggle_dialogue("#delete-dialogue");
        selected_item_names = [$(this).closest(".list-item").data("item-name")];
        selected_item_ids = [$(this).closest(".list-item").data("item-id")];
        $("#delete-dialogue .header").text("Delete " + selected_item_names[0]);
    });

    $(".icon.create-from").click(function(e){
        e.stopPropagation();
        toggle_dialogue("#create-from-dialogue");
        selected_item_names = [$(this).closest(".list-item").data("item-name")];
        selected_item_ids = [$(this).closest(".list-item").data("item-id")];
        $("#create-from-dialogue .header").text($("#create-from-dialogue .header").text() + " " + selected_item_names[0]);
    });

    // dialogue submit functions
    $("#create-dialogue .submit").click(function(){
        let item_names = [$(this).closest(".dialogue-center").find("input").first().val()];
        manage_items("create",item_names);
    });

    $("#create-from-dialogue .submit").click(function(){
        let item_names = [$(this).closest(".dialogue-center").find("input").first().val()];
        manage_items("create from", item_names, selected_item_ids,{"source_game_mode":selected_item_names[0]});
    });

    $("#delete-dialogue .submit").click(function(){
        manage_items("delete",selected_item_names,selected_item_ids);
    });

    $(".list-item").click(function(){
        let checkbox = $(this).find(".form-check-input");
        if(checkbox.prop( "checked")){
            checkbox.prop( "checked", false )
        }else{
            checkbox.prop( "checked", true )
        }
        toggle_delete_all();
    });
    $(".form-check-input").click(function(e){
        e.stopPropagation();
        toggle_delete_all();
    });
});

function toggle_delete_all(){
    if($('.form-check-input:checkbox:checked').length > 0){
        $("#delete-all").removeClass("hidden")
    }else{
        $("#delete-all").addClass("hidden")
    }
}

// wrapper for async post request for managing config items
function manage_items(operation,item_names=[],item_ids=[],additional_data={}){
    $.ajax({
        type: "POST",
        url: FILE_MANAGER_URL,
        dataType : "json",
        data: Object.assign({},{"operation":operation,"item_type":FILE_TYPE,"item_ids":item_ids,"item_names":item_names},additional_data),
        success: function(response){
            if (response.load == "reload"){
                location.reload()
            }else{
                location.href = response.load
            }
        }
    });
}
