$(document).ready(function(){
    let isFirefox = typeof InstallTrigger !== 'undefined';
    if(isFirefox){
        $("#jupyter-iframe").attr("src",NOTEBOOK_URL)
    }else{
        setTimeout(function(){
            let win = window.open(NOTEBOOK_URL, '_blank');
            $("#jupyter-link").show();
            $("#jupyter-iframe").hide();
        },3000);
    }
})
