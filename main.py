from flask import Flask, render_template, url_for
from google.cloud import storage
import random
import urllib3

urllib3.disable_warnings()

app = Flask(__name__)
milu = None

MILU_BUCKET = 'milu-world'


@app.route('/')
def get_milu():
    global milu
    if not milu:
        return 'There no milu yet, please update by this <a href="%s">link</a>' % url_for('update_milu')
    # Get random milu
    random_milu = random.choice(milu)
    return render_template('milu.html', milu_url=random_milu)


@app.route('/update')
def update_milu():
    global milu
    milu = []
    client = storage.Client()
    bucket = client.get_bucket(MILU_BUCKET)
    for blob in bucket.list_blobs(prefix='images/'):
        if blob.content_type.startswith('image'):
            milu.append(blob.public_url)

    return 'Update milu successfully! Start <a href="%s">get milu</a>' % url_for('get_milu')


if __name__ == '__main__':
    app.run()
