import pytest
from web import create_app
import requests

@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    app.config.from_object('web.config.TestingConfig')
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()
    yield client  # this is where the testing happens!
    ctx.pop()

def test_landing_page(client):
    resp = client.get('/')
    assert b"Login" in resp.data
    assert resp.status_code == 200

def test_login_page(client):
    resp = client.get('/login')
    assert b"Login" in resp.data
    assert resp.status_code == 200

def test_signup_page(client):
    resp = client.get('/sign_up')
    assert b"Sign up" in resp.data
    assert resp.status_code == 200

def test_non_existing_page(client):
    resp = client.get('/non_existing_page')
    assert resp.status_code == 404
    assert b"Either you requested invalid page or you don't have permission to access this page." in resp.data

def test_redirect_preferences(client):
    resp = client.get('/preference',follow_redirects=True)
    assert resp.status_code == 200
    assert b'You need to login for accessing this page!' in resp.data

def test_redirect_matches(client):
    resp = client.get('/matches', follow_redirects=True)
    assert resp.status_code == 200
    assert b'You need to login for accessing this page!' in resp.data

# def test_redirect_followup(client):
#     resp = client.get('/followup', follow_redirects=True)
#     assert resp.status_code == 200
#     assert b'You need to login for accessing this page!' in resp.data
