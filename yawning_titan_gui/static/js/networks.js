$(document).ready(function(){
    // set multi range sliders on load
    $(".multi-range-input.left").each(function(i,el){
        update_multi_range_left(el);
    });
    $(".multi-range-input.right").each(function(i,el){
        update_multi_range_right(el);
    });

    // update multi range sliders on input
    $(".multi-range-input.left, .multi-range .range-setter.left").on('input',function(){
        let multi_range_el = $(this).closest(".multi-range"),
            left_slider = $(".multi-range-input.left",multi_range_el),
            right_slider = $(".multi-range-input.right",multi_range_el);

        left_slider.val($(this).val()); // set the range slider value to itself if `this` is slider el otherwise set to the value of the input
        update_multi_range_left(left_slider.get(0));
        filter_networks(multi_range_el.data("attribute-name"),left_slider.val(),right_slider.val());
    });

    $(".multi-range-input.right, .multi-range .range-setter.right").on('input',function(e){
        let multi_range_el = $(this).closest(".multi-range"),
            left_slider = $(".multi-range-input.left",multi_range_el),
            right_slider = $(".multi-range-input.right",multi_range_el);
        right_slider.val($(this).val()); // set the range slider value to itself if `this` is slider el otherwise set to the value of the input
        update_multi_range_right(right_slider.get(0));
        filter_networks(multi_range_el.data("attribute-name"),left_slider.val(),right_slider.val());
    });
});

function update_multi_range_right(el){
    $(el).val(
        Math.max(
            $(el).val(),$(el).siblings(".multi-range-input").val()
        )
    );
    let value=(100/(parseInt(el.max)-parseInt(el.min)))*parseInt(el.value)-(100/(parseInt(el.max)-parseInt(el.min)))*parseInt(el.min),
        multi_range_el = $(el).closest(".multi-range"),
        children = $(".slider-container",multi_range_el).children();

    $(children.get(1)).css("width",(100-value)+"%");
    $(children.get(2)).css("right",(100-value)+'%');
    $(children.get(4)).css("left",value+'%');
    $(".range-setter.right",multi_range_el).val($(el).val());
}

function update_multi_range_left(el){
    $(el).val(
        Math.min(
            $(el).val(),$(el).siblings(".multi-range-input").val()
        )
    );
    let value=(100/(parseInt(el.max)-parseInt(el.min)))*parseInt(el.value)-(100/(parseInt(el.max)-parseInt(el.min)))*parseInt(el.min),
        multi_range_el = $(el).closest(".multi-range"),
        children = $(".slider-container",multi_range_el).children();

    $(children.get(0)).css("width",value+"%");
    $(children.get(2)).css("left",value+'%');
    $(children.get(3)).css("left",value+'%');
    $(".range-setter.right",multi_range_el).val($(el).val());
}

// wrapper for async post request for filtering networks by attribute
function filter_networks(attribute,min,max){
    $.ajax({
        type: "POST",
        url: window.location.href,
        data: {"attribute":attribute,"min":min,"max":max},
        success: function(response){
            item_filter.set(
                $(".list-item").filter(function(){
                    return ! response.ids.includes($(this).data("item-id"))
                }),
                "advanced"
            );
            item_filter.update_elements();
        },
        error: function(response){
            console.log(response.error)
        }
    });
}
