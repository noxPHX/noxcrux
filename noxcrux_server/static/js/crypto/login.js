$(document).ready(function () {
    // Empty password field to avoid confusion with the hashed one
    $('input[name="password"]').val("");
});

$("form").on('submit', async function (e) {

    e.preventDefault();

    let masterPassword = UTF8toBytes($('input[name="password"]').val());
    let username = UTF8toBytes($('input[name="username"]').val());

    let masterKey = await pbkdf2(masterPassword, username, 100000);

    dbSetup().then(function (store) {
		store.put({id: 1, masterKey: masterKey});
	});

    let masterHash = await pbkdf2(masterKey.array.buffer, masterPassword, 30000);

    $('input[name="password"]').val(masterHash.b64);

    $(this).off('submit');
    $(this).submit();
});
