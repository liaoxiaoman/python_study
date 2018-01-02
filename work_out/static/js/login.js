$(document).ready(function(){
    $("#a_signup").click(function(){
        $('#login').hide();
        $('#signup').show();
    });
    $("#back_login").click(function(){
        $('#signup').hide();
        $('#login').show();
    });
    $("#signup_submit").click(function(){
        var name = $("#signup_name").val();
        var password = $("#signup_password").val();
        var re_password = $("#signup_re_password").val();
        if(password != re_password){
            $("#error_info").html("两次输入的密码不一致");
            $("#error_info").show();
        };
        $.post('/signup',{'name': name, 'password': password}, function(data){
            var obj = $.parseJSON(data);
            if(obj.success==false){
                $("#error_info").html(obj.data.reason);
                $("#error_info").show();
            }
            else{
                $.post('/',{'name': name, 'password': password});
            };
        });
    });

    // 登陆
    $("#login_submit").click(function(){
        var name = $("#name").val();
        var password = $("#password").val();
        $.post('/',{'name': name, 'password': password}, function(data){
            var obj = $.parseJSON(data);
            if(obj.success==false){
                $("#error_info").html(obj.data.reason);
                $("#error_info").show();
            }
            else{
                window.location.replace("/index?uid="+obj.data.uid+"&token="+obj.data.token);
            };
        });
    });
});