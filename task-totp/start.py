#!/usr/bin/env python3
from main import app, init
from gevent import socket
from gevent.pywsgi import WSGIServer
from gevent import monkey

monkey.patch_all()

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

listener.bind(("0.0.0.0", 8000))
listener.listen(100)


if __name__ == "__main__":
    init()
    WSGIServer(listener, app).serve_forever()
