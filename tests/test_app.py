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
    assert type(response.json_body) == dict

def test_list_revisions():
  with Client(app) as client:
    response = client.http.get('/list_revisions/46d55215cf9fc28d71d47ffa563cb948')
    assert type(response.json_body) == dict

def test_list_s3_buckets():
  with Client(app) as client:
    response = client.http.get('/list_s3_buckets')
    assert type(response.json_body) == dict