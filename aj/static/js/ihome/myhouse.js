
$(document).ready(function(){
    $.get('/house/myhouses/', function (data) {
        if(!data.msg.id_name) {
            $(".auth-warn").show();
            $('#houses-list').hide()
        }else{
            $(".auth-warn").hide();
            $('#houses-list').show()
        }
    });
});