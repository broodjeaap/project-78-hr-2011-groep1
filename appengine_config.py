# -*- coding: latin-1 -*-
from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key="��@i]^�fJ�#!dѦ4�b�jW>�]D<�P����2m��Xw�j]�Ǌv&�M.�1��PS���M")
    return app