def test_home(client, auth):
    auth.login()
    response = client.get('/')
    assert b'<title>Dashboard - Igreja Conectada</title>'
    assert b'Home' in response.data
    assert b'Membros' in response.data
    assert b'Comunicados' in response.data
    assert b'Sair' in response.data
