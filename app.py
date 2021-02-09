from chalice import Chalice, Response

app = Chalice(app_name='trifacta-dataexchange')


@app.route('/')
def index():
    with open('chalicelib/index.html') as f:
        html = f.read()
    return Response(body=html, headers={'Content-Type': 'text/html'}, status_code=200)

@app.route('/list_datasets')
def list_datasets(region_name='us-east-1'):
    import boto3
    dx = boto3.client('dataexchange', region_name=region_name)
    return {'results': [{'id': i['Id'], 'text': i['Name']} for i in dx.list_data_sets(Origin='ENTITLED')['DataSets']]}

@app.route('/list_revisions/{dataset_id}')
def list_revisions(dataset_id, region_name='us-east-1'):
    import boto3
    dx = boto3.client('dataexchange', region_name=region_name)
    return {'results': [{'id': i['Id'], 'text': i['CreatedAt'].isoformat()} for i in dx.list_data_set_revisions(DataSetId=dataset_id)['Revisions']]}

@app.route('/list_s3_buckets')
def list_s3_buckets(region_name='us-east-1'):
    import boto3
    s3 = boto3.client('s3', region_name=region_name)
    buckets = s3.list_buckets()['Buckets'] 
    return {'results': [{'id': b['Name'], 'text': b['Name']} for b in buckets]}

def dx_runjob_download(dataset_id, revision_id, bucket_name, region_name='us-east-1'):
    import boto3
    dx = boto3.client('dataexchange', region_name)
    assets = [{'AssetId':i['Id'], 'Bucket': bucket_name, 'Key': i['Name']} for i in dx.list_revision_assets(DataSetId=dataset_id, RevisionId=revision_id)['Assets']]
    createjob_response = dx.create_job(
        Details={
            'ExportAssetsToS3': {
                'AssetDestinations': assets,
                'DataSetId': dataset_id,
                'RevisionId': revision_id
            }
        },
        Type='EXPORT_ASSETS_TO_S3'
    )
    startjob_response = dx.start_job(JobId=createjob_response['Id'])
    dx_job_id = createjob_response['Id']
    return {'job_id': dx_job_id, 'assets': assets}

@app.route('/runjob_download')
def runjob_download(region_name='us-east-1'):
    params = app.current_request.query_params
    print(app.current_request.to_dict())
    result = dx_runjob_download(params['dataset_id'], params['revision_id'], params['bucket_name'], region_name)
    print(result)
    return result

@app.route('/favicon.ico')
def favicon():
    return Response(body='', headers={'Location': 'https://trifactas3files.s3.us-east-1.amazonaws.com/trifacta_logo.ico'}, status_code=301)

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
