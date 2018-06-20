function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$('#form-avatar').submit(function () {
    // evt.preventDefault()
    $('.error-msg').hide()
    $(this).ajaxSubmit({
        url: '/user/profile/',
        type: 'post',
        dataType: 'json',
        success: function (msg) {
            if(msg.code=='200'){
                $('#user-avatar').attr('src', msg.img_url)
            }
        },
        error: function (msg) {
            alert('图片保存失败')
        }
    })
    return false;
});

$('#form-name').submit(function () {
    // evt.preventDefault()
    var username = $('#user-name').val();
    $('.error-msg').hide()
    $(this).ajaxSubmit({
        url: '/user/profile/',
        type: 'patch',
        dataType: 'json',
        data:{'user-name': username},
        success: function (msg) {
            $('.error-msg').show()
            $('.error-msg span').html(msg.msg)
        },
        error: function (msg) {
            alert('修改失败')
            $('#error-msg').show()
        }
    })
    return false;
});

function del_msg(){
    $('.error-msg span').html('');
    $('.error-msg').hide()
}