function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

// 点击推出按钮时执行的函数
function logout() {
    $.ajax({
        url: "/user/logout/",
        type: "delete",
        // headers: {
        //     "X-CSRFToken": getCookie("csrf_token")
        // },
        dataType: "json",
        success: function (resp) {
            if (200 == resp.code) {
                location.href = "/user/login/";
            }
        }
    });
}

$(document).ready(function(){
    $.get("/user/my_info/", function(resp){
        // 用户未登录
        if ("4101" == resp.errno) {
            location.href = "/user/login/";
        }
        // 查询到了用户的信息
        else if (200 == resp.code) {
            $("#user-name").html(resp.data.name);
            $("#user-mobile").html(resp.data.mobile);
            if (resp.data.avatar) {
                $("#user-avatar").attr("src", resp.data.avatar);
            }
        }
    }, "json");
});