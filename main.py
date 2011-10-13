from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import datetime


import htmlHelper
import entities

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(htmlHelper.header())
        self.response.out.write(htmlHelper.klasAfspraakPage('h3'))
        self.response.out.write(htmlHelper.footer())
        

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
