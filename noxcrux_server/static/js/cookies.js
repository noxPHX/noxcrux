$("#cookies_accepted").on('click', function () {

    let date = new Date();
    date.setTime(date.getTime() + (365 * 24 * 60 * 60 * 1000));
    let expires = "; expires=" + date.toUTCString();
    document.cookie = encodeURIComponent("cookies_accepted") + "=" + encodeURIComponent(true) + expires + "; path=/";
    $(this).parent(".alert").alert('close');
});
