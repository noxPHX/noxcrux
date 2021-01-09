function timeOuts() {

    setTimeout(function () {
        $(".alert-success:first").alert('close');
    }, 2000);

    setTimeout(function () {
        $(".alert-info:first").alert('close');
    }, 2000);

    setTimeout(function () {
        $(".alert-warning:first").alert('close');
    }, 5000);
}

timeOuts();
