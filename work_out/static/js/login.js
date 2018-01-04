$(document).ready(function(){
    $.cookie('the_work_out_cookie', '');
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
        }
        else{
            $.post('/signup',{'name': name, 'password': password}, function(data){
                var obj = $.parseJSON(data);
                if(obj.success==false){
                    $("#error_info").html(obj.data.reason);
                    $("#error_info").show();
                }
                else{
                    $.cookie('the_work_out_cookie', obj.data.cookie);
                    $.cookie('the_work_out_uid', obj.data.uid);
                    window.location.href = "/index?uid="+obj.data.uid;
                };
            });
        }
    });

    // 登陆
    $("#login_submit").click(function(){
        var name = $("#name").val();
        var password = $("#password").val();
        $.post('/',{'name': name, 'password': password}, function(data){
            var obj = $.parseJSON(data);
            if(obj.success==false){
                $("#login_error_info").html(obj.data.reason);
                $("#login_error_info").show();
            }
            else{
                $.cookie('the_work_out_cookie', obj.data.cookie);
                $.cookie('the_work_out_uid', obj.data.uid);
                window.location.href = "/index?uid="+obj.data.uid;
            };
        });
    });

    // 回车提交
    $("#login_form").keydown(function(e){
        var e = e || event,
        keycode = e.which || e.keyCode;
        if (keycode==13) {
            $("#login_submit").trigger("click");
        }
    });
    $("#signup_form").keydown(function(e){
        var e = e || event,
        keycode = e.which || e.keyCode;
        if (keycode==13) {
            $("#signup_submit").trigger("click");
        }
    });

});