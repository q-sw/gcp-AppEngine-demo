from flask import Flask, render_template
from  google.cloud import storage
from google import auth
import os

import datetime as dt

app = Flask(__name__)

@app.route('/')
def home():
    images = list_bucket_file(os.getenv("thumbnail_bucket"))
    return render_template('index.html', images=images)
@app.route('/cloud')
def cloud():
    images = list_bucket_file(os.getenv("prez_cloud_bucket"))
    return render_template('slides.html', images=images)

def list_bucket_file(bucket_name):

    credentials, project = auth.default()
    credentials.refresh(auth.transport.requests.Request())

    expiration = dt.timedelta(hours=1)

    storage_client = storage.Client(credentials=credentials)
    blobs = storage_client.list_blobs(bucket_name)


    slides = {}
    i = 1
    for blob in blobs:
        signed_url = blob.generate_signed_url(expiration=expiration,
                                              service_account_email=credentials.service_account_email,
                                              access_token=credentials.token
                                             )
        slides[i] = signed_url
        i += 1
    return slides

# Uncomment when you want try localy
# if __name__ == "__main__":
#    app.run(host='127.0.0.1', port=8080, debug=True)