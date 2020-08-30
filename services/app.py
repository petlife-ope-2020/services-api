import os

from flask import Flask
from flask_restful import Api

from cheroot.wsgi import PathInfoDispatcher
from cheroot.wsgi import Server as WSGIServer

from services.api.routes.manage import Manage
from services.api.routes.search import Search

APP = Flask(__name__)
API = Api(APP)
PORT = int(os.getenv('PORT', '8080'))

DISPATCHER = PathInfoDispatcher({'/': APP})
SERVER = WSGIServer(('0.0.0.0', PORT), DISPATCHER)

API.add_resource(Manage, '/manage')
API.add_resource(Search, '/search')

if __name__ == '__main__':
    SERVER.safe_start()
