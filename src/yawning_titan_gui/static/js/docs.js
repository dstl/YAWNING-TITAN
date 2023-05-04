$(document).ready(function(){
    let $iframe = $("#docs-iframe");
    $iframe.on('load', function(){
        $iframe.contents().find("img").each(function(i,el){
            // replace all references to the images directory relative url
            if($(el).attr("src").includes("_images")){
                let regex = /_images/i;
                $(el).attr("src",$(el).attr("src").replace(regex,"_static"));
            }
        });
    });
});
