function logout() {
    $.get("/user/logouts/", function(data){
        if (data.data=='200') {
            location.href = "/user/login/";
        }
    })
}

$(document).ready(function(){
});



$.get('/user/user/', function (data) {
   if(data.code=='200'){
       if(!data.user_info.avatar){
           $('#user-avatar').attr('src', '/static/images/default.png');
       }else{
           $('#user-avatar').attr('src', '/static/upload/' + data.user_info.avatar);
       }
       $('#user-name').html(data.user_info.name);
       $('#user-mobile').html(data.user_info.phone);
   }
})

