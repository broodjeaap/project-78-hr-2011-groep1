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
        
class AfspraakPlanningPost(webapp.RequestHandler):
    def post(self):
        
        vakken = entities.Vak.all()
        self.response.out.write("<table border='1'>")
        for vak in vakken:
            self.response.out.write("<tr>")
            self.response.out.write("<td>"+vak.vakCode+"</td>")
            x = self.request.get(vak.vakCode+"_afspraak")
            self.response.out.write("<td>"+x+"</td>")
            self.response.out.write("<td>"+vak.vakCode+"_afspraak</td>")
            self.response.out.write("</tr>")
    
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/afspraakplanningpost', AfspraakPlanningPost)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
