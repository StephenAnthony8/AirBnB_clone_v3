#!/usr/bin/python3
# module documentation
from flask import Blueprint

# url prefix must be '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

if (True):
    from api.v1.views.index import *  # wildcard import of everything in index
