function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}


$(document).ready(function () {
    $('#form-auth').submit(function () {
        var real_name = $('#real-name').val();
        var id_card = $('#id-card').val();
        $.ajax({
            url: '/user/auth/',
            type: 'PATCH',
            dataType: 'json',
            data: {'real-name': real_name, 'id-card': id_card},
            success: function (msg) {
                $('.btn-success').hide();
            },
            error: function (msg) {

            }
        });
    return false;
    });
});


$.get('/user/auths/', function (msg) {
    if(msg.code=='200'){
        if(msg.msg.id_name){
            $('#real-name').val(msg.msg.id_name).prop('disabled', true);
            $('#id-card').val(msg.msg.id_card).prop('disabled', true);
            $('.btn-success').hide()
        }
    }
});