#!/bin/env python

import httplib
import urllib
import json

class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = httplib.HTTPConnection(host, port)

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
        self.conn.request('GET', '/open/%d' % id)
        return self.conn.getresponse().read()

def main():
    pass

if __name__ == '__main__':
    main()


