
$(document).ready(function(){
    $.get('/house/myhouses/', function (data) {
        if(data.user.id_card){
            $(".auth-warn").hide();

            var myhouses_str = '';
            for(var i=0; i<data.houses.length; i++){
                myhouses_str += '<li><a href="/house/detail/?house_id='+ data.houses[i].id + '"><div class="house-title"><h3>房屋ID: ';
                myhouses_str += data.houses[i].id;
                myhouses_str += ' —— 房屋标题: ';
                myhouses_str += data.houses[i].title;
                myhouses_str += '</h3></div><div class="house-content"><img src='+ data.houses[i].image +'>';
                myhouses_str += '<div class="house-text"><ul><li>位于：';
                myhouses_str += data.houses[i].address;
                myhouses_str += '</li><li>价格：￥'+ data.houses[i].price;
                myhouses_str += '/晚</li><li>发布时间：' + data.houses[i].create_time;
                myhouses_str += '</li></ul></div></div></a></li>'
            }
            $('#houses-list').append(myhouses_str).show();
        }else{
            $(".auth-warn").show();
            $('#houses-list').hide();
        }
    });
});