#!/bin/env python

from gevent import monkey; monkey.patch_all()
import gevent.event
import bottle
import subprocess
import StringIO
import os

pending = []
next_id = 0
event = gevent.event.Event()
root = '.'

@bottle.get('/file/<path:path>')
def file(path):
    # Handle a request from the client to download a whole file from the
    # server.  Open the file with a4, and then send the file down to the
    # client.
    return bottle.static_file(path, root='/')

@bottle.get('/open/<id:int>')
def open(id):
    # Wait for the next file to open.
    while len(pending) == 0 or pending[0]['id'] < id:
        event.wait(600)
    return pending.pop(0)

@bottle.post('/open')
def open():
    # Open a new file with the given name.
    global next_id
    path = bottle.request.json['path']
    data = {'id': next_id, 'path': path}
    if not os.path.exists(os.path.join(root, path)):
        bottle.response.status = 404
        return {'status': 'no such file'}

    pending.append(data)
    next_id += 1
    event.set()
    event.clear()
    return data

@bottle.post('/patch')
def patch():
    # Post a diff of the given file and apply it.
    patch = bottle.request.json['patch']
    path = bottle.request.json['path']
    print patch
    p = subprocess.Popen(('patch', '-t', path), stdin=subprocess.PIPE)
    p.communicate(input=patch)
    if p.returncode != 0:
        bottle.response.status = 500
        return {'status': 'patch failure'}
    return {'status': 'success'}
    
def main():
    bottle.run(host='', port=int(os.environ['RVIMPORT']), server='gevent')
      
if __name__ == '__main__':
    main()
