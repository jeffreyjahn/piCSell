$(document).ready(function(){
    $('.carousel').carousel()
    $('.carousel').carousel({
        interval: 400,
        pause: "false"
    });
    $('#register-link').click((e) => { 
        e.preventDefault();
        $('#register-form').show();
        $('#login-form').hide();
        $('a#register-link').addClass("active")
        $('a#login-link').removeClass("active")
    });
    $('#login-link').click((e) => { 
        e.preventDefault();
        $('#login-form').show();
        $('#register-form').hide();
        $('a#login-link').addClass("active")
        $('a#register-link').removeClass("active")
    });
    
    $('#chatroom').scrollTop($('#chatroom')[0].scrollHeight);
})
