function hrefBack() {
    history.go(-1);
}

function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

$(document).ready(function(){
    // var mySwiper = new Swiper ('.swiper-container', {
    //     loop: true,
    //     autoplay: 2000,
    //     autoplayDisableOnInteraction: false,
    //     pagination: '.swiper-pagination',
    //     paginationType: 'fraction'
    // });
    // $(".book-house").show();
});

$(document).ready(function () {
    var info = location.search;
    var house_id = info.split('=')[1];
    $.ajax({
        url: '/house/details/'+ house_id +'/',
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            var image_str = '';
            console.log(data.house.images.length);
            for(var i=0;i < data.house.images.length;i++){
                image_str += '<li class="swiper-slide"><img src=';
                image_str += data.house.images[i];
                image_str += '></li>';
            }
            $('.swiper-wrapper').append(image_str);
            $('.house-price span').html(data.house.price);
            $('.house-title').html(data.house.title);
            $('.landlord-pic img').attr('src', '/static/upload/' + data.user.avatar);
            $('.landlord-name span').html(data.user.name);
            $('.text-center li').html(data.house.address);
            $('#house_rent_count').html('出租' + data.house.room_count + '间');
            $('#house_rent_acreage').html('房屋面积 :' + data.house.acreage + '平米');
            $('#house_rent_type').html('房屋户型 :' + data.house.unit);
            $('#livable_number').html('宜居人数 :' + data.house.capacity);
            $('#beds').html(data.house.beds);
            $('#atleast_days').html(data.house.min_days);
            $('#most_days').html(data.house.max_days);

            var facilitys_list = data.house.facilities;
            console.log(facilitys_list);
            var facilitys_str = '';
            for(var j=0; j<facilitys_list.length; j++){
                facilitys_str += '<li><span class="';
                facilitys_str += facilitys_list[j].css;
                facilitys_str += '"></span>';
                facilitys_str += facilitys_list[j].name;
                facilitys_str += '</li>';
            }
            $('.house-facility-list').append(facilitys_str);
            $('.book-house').attr('href', '/order/booking/?house_id=' + data.house.id);

            var mySwiper = new Swiper ('.swiper-container', {
                loop: true,
                autoplay: 2000,
                autoplayDisableOnInteraction: false,
                pagination: '.swiper-pagination',
                paginationType: 'fraction'
            });
            $(".book-house").show();
        },
        error: function (data) {
            alert('失败')
        }


    });

});