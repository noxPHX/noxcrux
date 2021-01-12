$(".toggle-visibility").on('click', function (e) {

    e.preventDefault();

    let field = $(this).parent().parent().children('input');

    if (field.prop("type") === "text") {
        field.prop("type", 'password');
        $(this).children('i').removeClass('fa-eye').addClass('fa-eye-slash');
    } else if (field.prop("type") === "password") {
        field.prop("type", 'text');
        $(this).children('i').removeClass('fa-eye-slash').addClass('fa-eye');
    }
});
