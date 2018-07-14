$(document).ready(function(){
    // 对于发布房源，只有认证后的用户才可以，所以先判断用户的实名认证状态
    $.get("/house/check_auth/", function(resp){
        if ("4101" == resp.errno) {
            // 用户未登录
            location.href = "/user/login/";
        } else if (200 == resp.code) {
            // 未认证的用户，在页面中展示 "去认证"的按钮
            if (!(resp.data.real_name && resp.data.id_card)) {
                $(".auth-warn").show();
                $('#release_house_temp').hide();
                return;
            }
            // 已认证的用户，请求其之前发布的房源信息
            $.get("/house/houses/", function(resp){
            $('#release_house_temp').show();
                if (200 == resp.code) {
                    $("#houses-list").html(template("houses-list-tmpl", {houses:resp.data.houses}));
                } else {
                    // $("#houses-list").html(template("houses-list-tmpl", {houses:[]}));
                }
            });
        }
    });
})