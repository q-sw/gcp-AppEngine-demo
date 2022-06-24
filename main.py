from flask import Flask, render_template
from google.cloud import storage
from google import auth
import os
import json
import datetime as dt

app = Flask(__name__)

expiration = dt.timedelta(hours=1)


@app.route('/')
def home():
    CONFIG_FILE_PATH = os.path.dirname(__file__)
    CONFIG_FILE = os.path.join(CONFIG_FILE_PATH, 'config.json')
    with open(CONFIG_FILE, 'r') as config_file:
        config = json.load(config_file)

    SLIDES = config.get("slides")

    result = []
    for s in SLIDES:
        cred = get_auth()
        bucket_name = os.getenv("thumbnail_bucket")
        blob_name = s.get("thumbnail_name")

        thumbnail_img = get_blob_object(cred, bucket_name, blob_name)
        signed_url = sign_url(expiration, cred, thumbnail_img)

        s['signed_url'] = signed_url
        result.append(s)

    return render_template('index.html', slides=result)


@app.route('/<url>')
def slides(url):
    cred = get_auth()
    blobs = list_bucket_file(cred, os.getenv(f"prez_{url}_bucket"))

    slides = {}
    i = 1
    for blob in blobs:
        signed_url = sign_url(expiration, cred, blob)
        slides[i] = signed_url
        i += 1

    return render_template('slides.html', images=slides)


def get_auth():
    credentials, project = auth.default()
    credentials.refresh(auth.transport.requests.Request())

    return credentials


def sign_url(expiration_time, credentials, blob_object):
    signed_url = blob_object.generate_signed_url(expiration=expiration_time,
                                                 service_account_email=credentials.service_account_email,
                                                 access_token=credentials.token)
    return signed_url


def get_blob_object(credentials, bucket_name, object_path):
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_path)

    return blob


def list_bucket_file(credentials, bucket_name):
    storage_client = storage.Client(credentials=credentials)
    blobs = storage_client.list_blobs(bucket_name)

    return blobs

# Uncomment when you want try localy
# if __name__ == "__main__":
#    app.run(host='127.0.0.1', port=8080, debug=True)
