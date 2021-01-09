function timeOuts() {

    setTimeout(function () {
        $(".alert-success").alert('close')
    }, 2000);

    setTimeout(function () {
        $(".alert-info").alert('close')
    }, 2000);

    setTimeout(function () {
        $(".alert-warning").alert('close')
    }, 5000);
}

timeOuts();
