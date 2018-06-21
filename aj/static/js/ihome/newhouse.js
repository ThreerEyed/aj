function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.popup_con').fadeIn('fast');
    $('.popup_con').fadeOut('fast');
    $.get('/house/newhouses/', function (data) {
        var areas = data.all_area;
        var facilitys = data.all_facility;
        var areas_str = '';
        var facilitys_str = '';
        for(var i=0; i<areas.length; i++){
            areas_str += '<option value='+ areas[i].id +'>'+ areas[i].name + '</option>'
        }
        for(var j=0; j < facilitys.length; j++){
            facilitys_str += '<li><div class="checkbox"><label><input type="checkbox" name="facility" value=';
            facilitys_str += facilitys[j].id;
            facilitys_str += '>';
            facilitys_str += facilitys[j].name;
            facilitys_str += '</label></div></li>'
        }
        $('#area-id').html(areas_str);
        $('.house-facility-list').html(facilitys_str)
    })
});

$('#form-house-info').submit(function () {
    $('.error-msg text-center').hide();
    //验证内容是否填写
    $.post('/house/newhouses/',$(this).serialize(),function (data) {
        if(data.code== '200'){
            $('#form-house-info').hide();
            $('#form-house-image').show();
            $('#house-id').val(data.msg);
        }else{
            $('.error-msg text-center').show()
        }
    });
    return false;
});


$('#form-house-image').submit(function () {
    $(this).ajaxSubmit({
        url: '/house/house_img/',
        type: 'post',
        dataType: 'json',
        success: function (data) {
            var img_url = '<img src='+ data.image_url + '>';
            $('.house-image-cons').append(img_url)
        },
        error:function (data) {
            alert('添加失败')
        }
    })
    return false
});