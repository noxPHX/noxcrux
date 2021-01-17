$("#generate").on('click', function (e) {

    e.preventDefault();

    $.ajax({
        method: 'GET',
        url: $(this).data('url')
    })
        .done(function (data) {
            $('input[name=horcrux]').val(data.generated_horcrux);
        })
})
