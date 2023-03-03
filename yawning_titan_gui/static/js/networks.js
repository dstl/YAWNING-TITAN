$(document).ready(function(){
    // update multi range sliders on input
    $(".multi-range-input.left, .multi-range .range-setter.left").on('input',function(){
        let multi_range_el = $(this).closest(".multi-range"),
            left_slider = $(".multi-range-input.left",multi_range_el),
            right_slider = $(".multi-range-input.right",multi_range_el);
        filter_networks(multi_range_el.data("attribute-name"),left_slider.val(),right_slider.val());
    });

    $(".multi-range-input.right, .multi-range .range-setter.right").on('input',function(){
        let multi_range_el = $(this).closest(".multi-range"),
            left_slider = $(".multi-range-input.left",multi_range_el),
            right_slider = $(".multi-range-input.right",multi_range_el);
        filter_networks(multi_range_el.data("attribute-name"),left_slider.val(),right_slider.val());
    });
});

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
