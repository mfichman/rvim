#!/bin/env python

import httplib
import urllib
import json

class Cli:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.conn = httplib.HTTPConnection(host, port)

    def open(self, path):
        # Post a patch to the server.
        data = json.dumps({'path': path})
        headers = {'Content-Type': 'application/json'}
        self.conn.request('POST', '/open', data, headers)
        return json.load(self.conn.getresponse())

def main():
    pass

if __name__ == '__main__':
    c = Cli('localhost', 40000)
    c.open('foo/test.txt')
