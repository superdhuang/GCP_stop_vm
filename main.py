import json
import httplib2
import logging
from googleapiclient import discovery
from google.appengine.api import memcache
from oauth2client.contrib.appengine import AppAssertionCredentials

from flask import Flask

app = Flask(__name__)

INSTANCE_ZONE = 'asia-east1-a'
PROJECT = 'coral-mode-159015'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/vm/start/<instance_name>')
def start_vm(instance_name):
    credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/compute')
    http = credentials.authorize(httplib2.Http(memcache))
    compute = discovery.build('compute', 'v1', http=http)
    result = compute.instances().start(instance=instance_name, zone=INSTANCE_ZONE, project=PROJECT).execute()
    logging.debug(result)
    return json.dumps(result, indent=4)


@app.route('/vm/stop/<instance_name>')
def stop_vm(instance_name):
    credentials = AppAssertionCredentials(scope='https://www.googleapis.com/auth/compute')
    http = credentials.authorize(httplib2.Http(memcache))
    compute = discovery.build('compute', 'v1', http=http)
    result = compute.instances().stop(instance=instance_name, zone=INSTANCE_ZONE, project=PROJECT).execute()
    logging.debug(result)
    return json.dumps(result, indent=4)


if __name__ == '__main__':
    app.run()
