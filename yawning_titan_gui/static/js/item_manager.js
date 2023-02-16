//page variables
let selected_item_names = [],
    selected_item_ids = [];

$(document).ready(function(){
    $("#filter-list-items").keyup(function(){
        let input = this;
        item_filter.set(
            $(".list-item").filter(function(){
                return !$(this).data("item-name").toLowerCase().includes($(input).val())
            }),
            "search"
        );
        item_filter.update_elements();
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
        let input = $(this).closest(".dialogue-center").find("input").first(),
            item_names = [input.val()];
        $(this).closest(".dialogue-center").find("button[type='submit']").click();
        if(input.val()){
            if($(this).hasClass("custom-network")||$(this).hasClass("create")){
                manage_items("create",item_names);
            }else if($(this).hasClass("template-network")){
                manage_items("template",item_names);
            }
        }
    });

    $("#create-dialogue").submit(false);

    $("#create-from-dialogue .submit").click(function(){
        let item_names = [$(this).closest(".dialogue-center").find("input").first().val()];
        if($(this).closest(".dialogue-center").submit(false)){ // check that name field has been entered
            manage_items("create from", item_names, selected_item_ids,{"source_item_id":selected_item_ids[0]});
        }
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

function check_dialogue_filled(dialogue_el){
    if($(dialogue_el).find("input").first().val() != null){
        return true
    }else{
        // add error message
        console.log("NOT FILLED");
        return false
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
        },
        error: function(response){
            console.log(response)
        }
    });
}
