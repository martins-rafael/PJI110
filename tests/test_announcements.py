import pytest

from app.models import Announcement


@pytest.mark.parametrize('path', (
    '/announcements/create',
    '/announcements/1/edit',
    '/announcements/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize('path', (
    '/announcements/2',
    '/announcements/2/edit',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.get(path).status_code == 404


def test_create(client, auth, app):
    auth.login()
    assert client.get('/announcements/create').status_code == 200
    client.post('/announcements/create',
                data={'title': 'testing', 'description': 'test'})

    with app.app_context():
        assert Announcement.query.count() == 1


def test_update(client, auth, app):
    auth.login()
    client.post('/announcements/create',
                data={'title': 'testing', 'description': 'test'})
    assert client.get('/announcements/1/edit').status_code == 200
    client.post('/announcements/1/edit', data={'title': 'updated',
                'description': 'description updated'})

    with app.app_context():
        announcement = Announcement.query.filter_by(id=1).first()
        assert announcement.title == 'updated'
        assert announcement.description == 'description updated'


def test_delete(client, auth, app):
    auth.login()
    client.post('/announcements/create',
                data={'title': 'testing', 'description': 'test'})
    response = client.post('/announcements/1/delete')
    assert response.headers["Location"] == "/announcements/"

    with app.app_context():
        announcements = Announcement.query.filter_by(id=1).first()
        assert announcements is None
