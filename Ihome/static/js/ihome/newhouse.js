function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    // $('.popup_con').fadeIn('fast');
    // $('.popup_con').fadeOut('fast');
    $.get("/house/house_area_facilities/", function (resp) {
        if (200 == resp.code) {
            // // 表示查询到了数据,修改前端页面
            // for (var i=0; i<resp.data.length; i++) {
            //     // 向页面中追加标签
            //     var areaId = resp.data[i].aid;
            //     var areaName = resp.data[i].aname;
            //     $("#area-id").append('<option value="'+ areaId +'">'+ areaName +'</option>');
            // }

            // 使用前端模板 artTemplate
            rendered_html = template("areas-tmpl", {areas: resp.data.areas});
            $("#area-id").html(rendered_html);
            $('#house_facility_list').html(template('house_facility_temp',{facilities: resp.data.facilities}));
        } else {
            alert(resp.errmsg);
        }
    }, "json");

    // 处理房屋基本信息的表单数据
    $("#form-house-info").submit(function (e) {
        e.preventDefault();
        // 检验表单数据是否完整
        // 将表单的数据形成json，向后端发送请求
        var formData = {};
        $(this).serializeArray().map(function (x) { formData[x.name] = x.value });

        // 对于房屋设施的checkbox需要特殊处理
        var facility = [];
        // $("input:checkbox:checked[name=facility]").each(function(i, x){ facility[i]=x.value });
        $(":checked[name=facility]").each(function(i, x){ facility[i]=x.value });

        formData.facility = facility;

        // 使用ajax向后端发送请求
        $.ajax({
            url: "/house/release_house/",
            type: "post",
            data: JSON.stringify(formData),
            contentType: "application/json",
            dataType: "json",
            // headers: {
            //     "X-CSRFToken": getCookie("csrf_token")
            // },
            success: function(resp){
                if ("4101" == resp.errno) {
                    location.href = "/user/login/";
                } else if (200 == resp.code) {
                    // 后端保存数据成功
                    // 隐藏基本信息的表单
                    $("#form-house-info").hide();
                    // 显示上传图片的表单
                    $("#form-house-image").show();
                    // 设置图片表单对应的房屋编号那个隐藏字段
                    $("#house-id").val(resp.data.house_id);
                } else {
                    alert(resp.errmsg);
                }
            }
        });
        return false;
    });

    // 处理图片表单的数据
    $("#form-house-image").submit(function (e) {
        e.preventDefault();
        var house_id = $("#house-id").val();
        // 使用jquery.form插件，对表单进行异步提交，通过这样的方式，可以添加自定义的回调函数
        $(this).ajaxSubmit({
            url: "/house/house_images/",
            type: "post",
            data: {'house_id': house_id},
            // headers: {
            //     "X-CSRFToken": getCookie("csrf_token")
            // },
            dataType: "json",
            success: function (resp) {
                if ("4101" == resp.code) {
                    location.href = "/user/login/";
                } else if (200 == resp.code) {
                    // 在前端中添加一个img标签，展示上传的图片
                    $(".house-image-cons").append('<img src="'+ resp.url+'">');
                } else {
                    alert(resp.errmsg);
                }
            }
        })
    })


});