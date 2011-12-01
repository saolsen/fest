# -*- coding: utf-8 -*-
"""
    Fest
    ~~~~~~~~

    Fest is a small web service wrapper for the festival server daemon

    :copyright: (c) 2011 by Stephen Olsen
    :license: BSD, see LICENSE for more details.
"""
from flask import Flask, request, session, url_for, redirect, \
    render_template, abort, g, flash
import subprocess
from boto.s3.connection import S3Connection
from boto.s3.key import Key

# configuration

# create our little application :)
app = Flask(__name__)

def render_text(text, name):
    """
    Takes the text, runs in through festival, saves it as _id.wav
    returns the filename
    """
    # I'm thinking that there's a better way to do this without saving the wav file
    # locally first
    subprocess.call('echo "' + text + '" | festival_client --ttw | cat > ' + name + '.wav',
                    shell=True)
    return name + ".wav"

@app.route('/', methods=['GET', 'POST'])
def serve():
    """
    If a get, returns a form that posts the correct criteria to this endpoint.
    If a post of the form {id: 12345, text: "blahblahblah"}
    - It runs the text through festival,
    - saves the rendered audio file to an s3 bucket,
    - returns the url.
    """
    if request.method == 'POST':
        # Remember to set
        # AWS_ACCESS_KEY_ID and
        # AWS_SECRET_ACCESS_KEY
        s3 = S3Connection()
        bucket = s3.create_bucket('us.steveolsen.fest')

        text = request.form['text']
        name = request.form['name']

        filename = render_text(text, name)

        k = Key(bucket)
        k.key = name
        k.set_contents_from_filename(filename)
        url = k.generate_url(6000)

        return redirect(url)

    else:
        # Embedd a form with the text and id fields here
        return render_template('simpleForm.html')

if __name__ == '__main__':
    # Make sure that festival is running
    app.run(host="0.0.0.0")
