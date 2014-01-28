#!/bin/env python

import httplib
import difflib
import urllib
import json
import sys
import subprocess
import watchdog.observers
import watchdog.events
import shutil

class Client(watchdog.events.FileSystemEventHandler):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = httplib.HTTPConnection(host, port)
        self.conn2 = httplib.HTTPConnection(host, port)

    def file(self, path):
        # Get a file by pathname
        self.conn.request('GET', '/file/%s' % path)
        return self.conn.getresponse().read()

    def patch(self, path, patch):
        # Post a patch to the server.
        data = json.dumps({'path': path, 'patch': patch})
        headers = {'Content-Type': 'application/json'}
        self.conn.request('POST', '/patch', data, headers)
        return json.load(self.conn.getresponse())

    def next(self, id):
        # Wait for the next file to open
        self.conn2.request('GET', '/open/%d' % id)
        return json.load(self.conn2.getresponse())

    def run(self):
        # Wait for commands from the remote server.
        id = 0
        while True:
            data = self.next(id)
            print data['path']
            subprocess.Popen(('gvim', data['path']), shell=True)


