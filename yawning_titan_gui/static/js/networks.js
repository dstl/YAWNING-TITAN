$(document).ready(function(){
    $(".multi-range-input.left").on('input',function(){
        $(this).val(
            Math.min(
                $(this).val(),$(this).siblings(".multi-range-input").val()
            )
        );
        let value=(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.value)-(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.min);
        let children = this.parentNode.childNodes[1].childNodes;
        children[1].style.width=value+'%';
        children[5].style.left=value+'%';
        children[7].style.left=value+'%';
        $(this).closest(".multi-range").find(".value-left").val($(this).val());
    });
    $(".multi-range-input.right").on('input',function(){
        $(this).val(
            Math.max(
                $(this).val(),$(this).siblings(".multi-range-input").val()
            )
        );
        let value=(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.value)-(100/(parseInt(this.max)-parseInt(this.min)))*parseInt(this.min);
        let children = this.parentNode.childNodes[1].childNodes;
        children[3].style.width=(100-value)+'%';
        children[5].style.right=(100-value)+'%';
        children[9].style.left=value+'%';
        $(this).closest(".multi-range").find(".value-right").val($(this).val());
    });
})
