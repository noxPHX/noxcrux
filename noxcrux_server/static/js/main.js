$(document).ready(function () {
    $(function () {
        $('[data-toggle="popover"]').popover()
        $(".error-popover").popover('show');
    });

    $("#id_logout").on('click', function () {

        let indexedDB = window.indexedDB || window.mozIndexedDB || window.webkitIndexedDB || window.msIndexedDB || window.shimIndexedDB;
        indexedDB.deleteDatabase('KeysContainer');
    });
});
