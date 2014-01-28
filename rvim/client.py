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
import os

class Client(watchdog.events.FileSystemEventHandler):

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = httplib.HTTPConnection(host, port)

    def file(self, path):
        # Get a file by pathname
        try:
            self.conn.request('GET', '/file/%s' % path)
            return self.conn.getresponse().read()
        except httplib.HTTPException, e:
            self.conn.close()
            raise

    def patch(self, path, patch):
        # Post a patch to the server.
        try:
            data = json.dumps({'path': path, 'patch': patch})
            headers = {'Content-Type': 'application/json'}
            self.conn.request('POST', '/patch', data, headers)
            return json.load(self.conn.getresponse())
        except httplib.HTTPException, e:
            self.conn.close()
            raise

    def next(self, id):
        # Wait for the next file to open
        try:
            self.conn.request('GET', '/open/%d' % id)
            return json.load(self.conn.getresponse())
        except httplib.HTTPException, e:
            self.conn.close()
            raise

    def run(self):
        # Wait for commands from the remote server.
        id = 0
        while True:
            data = self.next(id)
            os.environ['RVIM'] = '1'
            os.environ['RVIMHOST'] = self.host
            os.environ['RVIMPORT'] = str(self.port)
            print data['path']
            subprocess.Popen(('gvim', data['path']), shell=True)

def main():
    c = Client('obs20', 40000)
    c.run()

if __name__ == '__main__':
    main()
