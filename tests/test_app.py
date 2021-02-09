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
    assert response.status_code == 200

def test_list_revisions():
  with Client(app) as client:
    response = client.http.get('/list_revisions/f988acb30303493f1ee750e7a93f6d33')
    assert response.status_code == 200

def test_list_s3_buckets():
  with Client(app) as client:
    response = client.http.get('/list_s3_buckets')
    assert response.status_code == 200

def test_runjob_download():
  with Client(app) as client:
    response = client.http.get('/runjob_download?dataset_id=f988acb30303493f1ee750e7a93f6d33&revision_id=3b985004c81cce01f2cecd515bff9483&bucket_name=trifactas3files')
    assert response.status_code == 200