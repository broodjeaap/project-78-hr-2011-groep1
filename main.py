from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import datetime


import htmlHelper
import entities

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write("<html><body><SCRIPT LANGUAGE='JavaScript' SRC='/js/Afspraak.js'></SCRIPT>")

        self.response.out.write(htmlHelper.afspraakTable('ABC'))
        self.response.out.write(htmlHelper.afspraakTable('DEF'))
        self.response.out.write('</body></html>')
        

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
