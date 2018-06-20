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
    alert($(this).serialize())
    $.post('/house/newhouses/',$(this).serialize(),function (data) {
        if(data.code== '200'){
            $('#form-house-info').hide();
            $('#form-house-image').show();
            $('#house-id').val(data.house_id);
        }else{
            $('.error-msg text-center').show().find('span').html(ret_map[data.code]);
        }
    });
    return false;
});