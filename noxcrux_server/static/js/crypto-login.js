$("form").on('submit', async function (e) {

    e.preventDefault();

    let masterPassword = fromUtf8($('input[name="password"]').val());
    let username = fromUtf8($('input[name="username"]').val());

    let masterKey = await pbkdf2(masterPassword, username, 100000, 256);

    dbSetup().then(function (store) {
		store.put({id: 1, masterKey: masterKey});
	});

    let masterHash = await pbkdf2(fromUtf8(masterKey.b64), masterPassword, 30000, 256);

    $('input[name="password"]').val(masterHash.b64);

    $(this).off('submit');
    $(this).submit();
});
