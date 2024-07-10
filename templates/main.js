$(document).ready(function(){
    $('.search_box').keydown(function(e){
        debounce = setTimeout(function(){
            getAutoComplete();
        }, 300);
    })
})

function getAutoComplete(){
    console.log("Auto Complete");
}
