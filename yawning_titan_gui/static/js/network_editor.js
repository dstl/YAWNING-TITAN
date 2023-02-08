$(document).ready(function(){
    $(".download-button").click(function(){
        console.log("CLICK");
        console.log("TESTING",proxy.NETWORK);
        $.ajax({
            type: "POST",
            url: window.location.href,
            dataType : "json",
            data: proxy.NETWORK,
            success: function(response){
                if (response.load == "reload"){
                    location.reload()
                }else{
                    location.href = response.load
                }
            }
        });
    });
});