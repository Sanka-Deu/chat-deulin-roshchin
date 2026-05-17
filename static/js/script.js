$(document).ready(function(){
    $("#registerForm").on("submit",function(e){
        e.preventDefault();
        $.ajax({
            url: "/user_registration",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                name: $("#firstName").val(),
                surname: $("#lastName").val(),
                login: $("#login").val(),
                password: $("#password").val(),
            })
        })
    })
})