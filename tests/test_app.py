from chalice.test import Client
from app import app

def test_index():
  with Client(app) as client:
      response = client.http.get('/')
      assert response.status_code == 200
      assert response.headers['Content-Type'] == 'text/html'

def test_list_datasets():
  with Client(app) as client:
    response = client.http.get('/list_datasets')
    assert type(response.json_body) == list