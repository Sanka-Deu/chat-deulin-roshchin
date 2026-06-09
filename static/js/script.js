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
    $("#avtorizationForm").on("submit",function(e){
        e.preventDefault();
        $.ajax({
            url: "/user_avtorization",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                login: $("#login").val(),
                password: $("#password").val(),
            })
        }).done(function(data){
            if (data.result){
                window.location.href = "/chat";
            }else{
                alert("Что-то пошло не так")
            }
        })
    })
    $("#send_mes").on("click",function(){
        var urlParams = new URLSearchParams (window.location.search);
        var owner = urlParams.get("owner");
        var deliver = urlParams.get("id")
        $.ajax({
            url: "/send_mes",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                owner: owner,
                deliver: deliver,
                text: $("#mes_input").val()
            })
        }).done(function(data){
            if (data.result){
                window.location.reload();
            }
        })
    })
})