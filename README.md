Fest
====
Fest is a web service wrapper for the festival text processing system

Running
------
* First you have to get festival installed and set up the way you like
(voices etc).
* Make sure you have your AWS credentials set in environment variables.
* Start Festival in server mode. $ festival --server
* Start up fest, you can do this two ways. You can run it with the
  webserver built into the flask library by invoking it on the command
  line $ python fest.py
* Otherwise you can run it with some other web server. How you do this
  will vary. (I currently run it with gunicorn)

Useing
------
If you hit the webserver you'll get a simple (terrible looking) form
that contains a name and text field. This is just for testing
purposes. The form posts to the same endpoint which is how anything
consuming this web service would use it.
To use the service send a POST to the root endpoint of the server
containing {'name': 'the_name_of_the_file', 'text': 'Some Text you
want to convert to audio'} The text will be translated to audio,
stored in an s3 bucket and then a direct url to the file will be
returned.
