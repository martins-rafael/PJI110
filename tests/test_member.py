import pytest

from app.models import Member


@pytest.mark.parametrize('path', (
    '/create',
    '/1/edit',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize('path', (
    '/2',
    '/2/edit',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.get(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/create').status_code == 200
    client.post('/create', data={'name': 'testing', 'email': 'testing@email.com',
                                 'password': 'testing', 'password_repeat': 'testing'})

    with app.app_context():
        assert Member.query.count() == 2


def test_update(client, auth, app):
    auth.login()
    assert client.get('/1/edit').status_code == 200
    client.post('/1/edit', data={'name': 'updated',
                'email': 'updated@email.com'})

    with app.app_context():
        member = Member.query.filter_by(id=1).first()
        assert member.name == 'updated'


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers["Location"] == "/members"

    with app.app_context():
        member = Member.query.filter_by(id=1).first()
        assert member is None
