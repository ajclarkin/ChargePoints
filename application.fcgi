#!/usr/bin/env python3
from app import app
from flipflop import WSGIServer

if __name__ == '__main__':
    WSGIServer(app).run()
