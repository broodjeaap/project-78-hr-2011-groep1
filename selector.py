import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from gaesessions import get_current_session
from google.appengine.ext import db
from google.appengine.api import mail
from google.appengine.api import memcache
import datetime
import webpages
import entities


import wsgiref.handlers
import sys
from reportlab.pdfgen import canvas

MAX = 2147483647

class Main(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        self.response.out.write("<script type='text/javascript' src='/js/selector.js'></SCRIPT>");
        self.response.out.write("<div class='leerlingSelectorDiv'>");
        self.response.out.write("<input type='text' id='leerlingIDText' onkeyup='textboxchange(this.value);' />");
        self.response.out.write("<div class='leerlingenOutputDiv' id='leerlingenOutputDiv'>");
        
        self.response.out.write("</div>")
        self.response.out.write("</div>")
        self.response.out.write(webpages.footer())

class LeerlingGet(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        q = self.request.get('q')
        selectorList = []
        leerlingen = getLeerlingen();
        selectorList.append(leerlingen[0])
        selectorList.append(leerlingen[1])
        selectorList.append(leerlingen[2])
        selectorList.append(leerlingen[3])
        result = []
        for leerling in leerlingen:
            if(leerling.leerlingID.find(q) != -1):
                result.append(leerling)
        self.response.out.write("<table border='1'>")
        for leerling in result:
            image = "redcross.png"
            if(leerling in selectorList):
                image = "greencheck.png"
            self.response.out.write("<tr onclick='addleerling("+leerling.leerlingID+")'>      <td><img src='/images/"+image+"' width='20' height='20' /></td>          <td>"+leerling.leerlingID+"</td><td>"+leerling.voornaam+" "+leerling.tussenvoegsel+" "+leerling.achternaam+"</td></tr>")
        self.response.out.write("</table>")
        

class LeerlingAdd(webapp.RequestHandler):
    def post(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        
        self.response.out.write(webpages.footer())
    
class DocentPost(webapp.RequestHandler):
    def get(self):
        session = get_current_session()
        self.response.out.write(webpages.header(session))
        
        self.response.out.write(webpages.footer())

def getLeerlingen():
    leerlingen = memcache.get("leerlingen1")
    if not leerlingen:
        leerlingen = db.GqlQuery("SELECT * FROM Leerling")
        leerlingen = leerlingen.fetch(MAX)
        memcache.set("leerlingen1",leerlingen[:(len(leerlingen) / 2)])
        memcache.set("leerlingen2",leerlingen[((len(leerlingen) /2)+1):])
    leerlingen += memcache.get("leerlingen2")
    return leerlingen
    

def main():
    application = webapp.WSGIApplication([('/selector', Main),
                                          ('/selector/leerlingget', LeerlingGet),
                                          ('/selector/leerlingadd', LeerlingAdd),
                                          ('/selector/docentpost', DocentPost)],
                                            debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
