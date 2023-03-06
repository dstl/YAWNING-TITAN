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

    // search form

    $("*[restrict-selector]").on("change",function(){
        $(`.${$(this).val()}`).removeClass("hidden");
    });

    // delete icons - search elements
    $("#search-form .mb-3:not(:has(*[restrict-selector]))").append(
        `<div class="icon delete">
            <i class="bi bi-trash3"></i>
        </div>`
    );
    $("#search-form .delete").click(function(){
        let container = $(this).closest(".mb-3"),
            input;
        if ($(container).find(".multi-range").length){
            let left_setter =  $(container).find(".range-setter.left"),
                right_setter = $(container).find(".range-setter.right");
            input = $(container).find(".multi-range");
            $(left_setter).val($(left_setter).attr("min"));
            $(right_setter).val($(right_setter).attr("max"));
        }else if($(container).find(".form-check-input").length){
            input = $(container).find(".form-check-input");
            $(input).prop("checked",false);
        }

        $(input).addClass("hidden");
        $("*[restrict-selector] option:selected").prop("selected", false); // update selected filters
        $("#search-form").trigger("change"); // update filters
    });

    $("#search-form").change(function(){
        filter(this)
    });
});

function toggle_delete_all(){
    if($('.list-item .form-check-input:checkbox:checked').length > 0){
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
        return false
    }
}

function search_form_data(form_element){
    let data = {};
    $(form_element).find(".multi-range").each(function(i,el){
        data[$(el).attr("name")+"_min"] = $(el).find(".range-setter.left").first().val();
        data[$(el).attr("name")+"_max"] = $(el).find(".range-setter.right").first().val();
    });
    $(form_element).find(".form-check-input").each(function(i,el){
        data[$(el).attr("name")] = $(el).is(':checked') ? "true" : "false";
    });
    $(form_element).find(".form-control").each(function(i,el){
        data[$(el).attr("name")] = $(el).val();
    });
    return data
}

function hide_show_items(item_ids){
    $(".list-item").addClass("hidden");
    console.log("IDS",item_ids);
    $(".list-item").each(function(i,el){
        if(item_ids.includes($(el).data("item-id"))){
            $(el).removeClass("hidden")
        }
    });
}

// wrapper for async post request for managing config items
function manage_items(operation,item_names=[],item_ids=[],additional_data={}){
    $.ajax({
        type: "POST",
        url: DB_MANAGER_URL,
        dataType : "json",
        data: Object.assign({},{"operation":operation,"item_type":ITEM_TYPE,"item_ids":item_ids,"item_names":item_names},additional_data),
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

// wrapper for async post request for config section form processing
function filter(form_element){
    console.log("POSTING TO",window.location.href);
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: search_form_data(form_element),
        dataType: "json",
        success: function(response){
            hide_show_items(response.item_ids)
        },
        error: function(response){
            console.log("ERR",response.message)
        }
    });
}
