//模态框居中的控制
function centerModals(){
    $('.modal').each(function(i){   //遍历每一个模态框
        var $clone = $(this).clone().css('display', 'block').appendTo('body');    
        var top = Math.round(($clone.height() - $clone.find('.modal-content').height()) / 2);
        top = top > 0 ? top : 0;
        $clone.remove();
        $(this).find('.modal-content').css("margin-top", top-30);  //修正原先已经有的30个像素
    });
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

$(document).ready(function(){
    $('.modal').on('show.bs.modal', centerModals);      //当模态框出现的时候
    $(window).on('resize', centerModals);


    $.get('/order/renter_lorders/', function (data) {
        var lorder_str = '';
        console.log(data.order[0].create_date);
        for(var i = 0; i < data.order.length; i++){
            lorder_str += '<li order-id=';
            lorder_str += data.order[i].order_id;
            lorder_str += '><div class="order-title"><h3>订单编号：';
            lorder_str += data.order[i].order_id;
            lorder_str += '</h3>';
            if(data.order[i].status == '待接单') {
                lorder_str += '<div class="fr order-operate"><button type="button" ' +
                    'class="btn btn-success order-accept" data-toggle="modal" ' +
                    'data-target="#accept-modal">接单</button><button type="button" ' +
                    'class="btn btn-danger order-reject" data-toggle="modal" ' +
                    'data-target="#reject-modal">拒单</button></div>';
            }
            lorder_str += '</div><div class="order-content"><img src=';
            lorder_str += data.order[i].image;
            lorder_str += '><div class="order-text"><h3>';
            lorder_str += data.order[i].house_title;
            lorder_str += '</h3><ul><li>创建时间：';
            lorder_str += data.order[i].create_date;
            lorder_str += '</li><li>入住日期：';
            lorder_str += data.order[i].begin_date;
            lorder_str += '</li><li>离开日期：';
            lorder_str += data.order[i].end_date;
            lorder_str += '</li><li>合计金额：￥';
            lorder_str += data.order[i].amount;
            lorder_str += '(共';
            lorder_str += data.order[i].days;
            lorder_str += '晚)</li><li>订单状态：<span>';
            lorder_str += data.order[i].status;
            lorder_str += '</span></li><li>客户评价：';
            lorder_str += data.order[i].comment;
            lorder_str += '</li></ul></div></div></li>';
        }
        $('.orders-list').append(lorder_str);
        $(".order-accept").on("click", function(){
        var orderId = $(this).parents("li").attr("order-id");
            $(".modal-accept").attr("order-id", orderId);
        });
        $(".order-reject").on("click", function(){
            var orderId = $(this).parents("li").attr("order-id");
            $(".modal-reject").attr("order-id", orderId);
        });

    });
    $('.modal-accept').on('click', function () {
        var orderId = $('.modal-accept').attr("order-id");
        var status = '已支付';
        $.ajax({
            url: '/order/orders/',
            type: 'PATCH',
            dataType: 'json',
            data: {'order_id': orderId, 'status': status},
            success: function (data) {
                location.href = '/order/lorders/'
            },
            error: function (data) {
            }
        })
    });
    $('.modal-reject').on('click', function () {
        var orderId = $('.modal-reject').attr("order-id");
        var status = '已拒单';
        var reject_reason = $('#reject-reason').val();
        $.ajax({
            url: '/order/orders/',
            type: 'PATCH',
            dataType: 'json',
            data: {'order_id': orderId, 'status': status, 'reject_reason': reject_reason},
            success: function (data) {
            },
            error: function (data) {
            }
        })
    });

});