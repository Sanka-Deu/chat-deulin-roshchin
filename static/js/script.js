$(document).ready(function(){
    function renderMessages(messages) {
    var $msgArea = $('#messages-area');
    $msgArea.empty();
    if (!messages || messages.length === 0) {
        $msgArea.html('<div class="empty-chat">Нет сообщений. Напишите что-нибудь!</div>');
        return;
    }
    for (var i = 0; i < messages.length; i++) {
        var msg = messages[i];
        var isOwner = (msg.ownerId == ownerId);
        var msgDiv = $('<div class="message ' + (isOwner ? 'message-owner' : 'message-deliver') + '">')
            .text(msg.text);
        if (msg.date) {
            var info = $('<div class="message-info">').text(msg.date);
            msgDiv.append(info);
        }
        $msgArea.append(msgDiv);
    }
    // прокрутка вниз
    $msgArea.scrollTop($msgArea[0].scrollHeight);
}

function loadMessages(deliverId) {
    if (!deliverId) return;
    currentDeliverId = deliverId;
    $.get('/api/messages', { user1: ownerId, user2: deliverId })
        .done(function(messages) {
            renderMessages(messages);
        })
        .fail(function() {
            alert('Ошибка загрузки сообщений');
        });
}
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
    }).done(function(data){
        if (data.result){
            window.location.href = "/chat";
        } else {
            alert(data.message || "Ошибка регистрации");
        }
    }).fail(function(){
        alert("Ошибка соединения");
    });
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
})
function renderMessages(messages) {
    var $msgArea = $('#messages-area');
    $msgArea.empty();
    if (!messages || messages.length === 0) {
        $msgArea.html('<div class="empty-chat">Нет сообщений. Напишите что-нибудь!</div>');
        return;
    }
    for (var i = 0; i < messages.length; i++) {
        var msg = messages[i];
        var isOwner = (msg.ownerId == ownerId);
        var msgDiv = $('<div class="message ' + (isOwner ? 'message-owner' : 'message-deliver') + '">')
            .text(msg.text);
        if (msg.date) {
            var dateStr = msg.date;
            // если дата в формате строки, можно отформатировать
            var info = $('<div class="message-info">').text(dateStr);
            msgDiv.append(info);
        }
        $msgArea.append(msgDiv);
    }
    // прокрутка вниз
    $msgArea.scrollTop($msgArea[0].scrollHeight);
}

function loadMessages(deliverId) {
    if (!deliverId) return;
    currentDeliverId = deliverId;
    $.get('/api/messages', { user1: ownerId, user2: deliverId })
        .done(function(messages) {
            renderMessages(messages);
        })
        .fail(function() {
            alert('Ошибка загрузки сообщений');
        });
    loadMessages(5)
}