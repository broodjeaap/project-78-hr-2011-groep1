# -*- coding: latin-1 -*-
from gaesessions import SessionMiddleware
def webapp_add_wsgi_middleware(app):
    app = SessionMiddleware(app, cookie_key="öý@i]^çœfJ›#!dÑ¦4úb›jW>]D<ÁP‹ÄÉÒ2m¼²Xw‘j]ÄÇŠv&—M.ž1µòPSµµM")
    return app