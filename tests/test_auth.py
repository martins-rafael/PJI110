import pytest
from flask import g, session


def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers['Location'] == '/'

    with client:
        client.get('/')
        assert session['member_id'] == 1
        assert g.member.name == 'admin'


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('test@email.com', 'test', b'Email incorreto.'),
    ('admin@email.com', 'test', b'Senha incorreta.'),
))
def test_login_validate_input(auth, email, password, message):
    response = auth.login(email, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'member_id' not in session
