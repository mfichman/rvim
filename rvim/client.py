#!/bin/env python

import httplib
import urllib
import json
import sys
import subprocess

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
        return json.load(self.conn.getresponse())

    def run(self):
        # Wait for the next file
        id = 0
        while True:
            next = self.next(id)
            print 'next', next
            path = next['path']
            id = next['id']+1
            
            data = self.file(path)  
            print 'file', path

            base = open('data/%d.base' % id, 'w')
            base.write(data)
            base.close()
            
            work = open('data/%d.work' % id, 'w')
            work.write(data)
            work.close()
        
            desc = open('data/%d.json' % id, 'w')
            desc.write(json.dumps(next))
            desc.close()

            subprocess.Popen(('gvim', 'data/%d.work' % id), shell=True)

def main():
    c = Client('obs20.mp.optumsoft.com', 40000)
    c.run()

if __name__ == '__main__':
    main()


