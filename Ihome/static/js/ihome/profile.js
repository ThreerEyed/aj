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

$(document).ready(function () {
    // 在页面加载是向后端查询用户的信息
    $.get("/user/show_user_info/", function(resp){
        // 用户未登录
        if ("1015" == resp.code) {
            location.href = "/user/login/";
        }
        // 查询到了用户的信息
        else if (200 == resp.code) {
            $("#user-name").val(resp.data.name);
            if (resp.data.avatar) {
                $("#user-avatar").attr("src", resp.data.avatar);
            }
        }
    }, "json");

    // 管理上传用户头像表单的行为
    $("#form-avatar").submit(function (e) {
        // 禁止浏览器对于表单的默认行为
        e.preventDefault();
        $(this).ajaxSubmit({
            url: "/user/avatar/",
            type: "post",
            // headers: {
            //     "X-CSRFToken": getCookie("csrf_token"),
            // },
            dataType: "json",
            success: function (resp) {
                if (resp.code == 200) {
                    // 表示上传成功， 将头像图片的src属性设置为图片的url
                    $("#user-avatar").attr("src", resp.data);
                } else if (resp.errno == "4101") {
                    // 表示用户未登录，跳转到登录页面
                    location.href = "/user/login/";
                } else {
                    alert(resp.errmsg);
                }
            }
        });
        return false;
    });
    $("#form-name").submit(function(e){
        e.preventDefault();
        // 获取参数
        var name = $("#user-name").val();

        if (!name) {
            alert("请填写用户名！");
            return;
        }
        $.ajax({
            url:"/user/profile/",
            type:"PUT",
            data: JSON.stringify({name: name}),
            contentType: "application/json",
            dataType: "json",
            // headers:{
            //     "X-CSRFTOKEN":getCookie("csrf_token")
            // },
            success: function (data) {
                if (200 == data.code) {
                    $(".error-msg").hide();
                    showSuccessMsg();
                } else if (1011 == data.code) {
                    $(".error-msg").show();
                } else if ("4101" == data.errno) {
                    location.href = "/user/login/";
                } else if (0 == data.code){
                    $('.error-msg').show();
                }
            }
        });
        return false;
    })
})

