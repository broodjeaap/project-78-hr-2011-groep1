from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext import db
import datetime
import webpages


import htmlHelper
import entities

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write(webpages.LoginForm())

class Authenticate(webapp.RequestHandler):
    def post(self):
        wachtwoord=self.request.get("wachtwoord")
        id=self.request.get("id")
        categorys = ['docent', 'leerling']
        NoValidCredentials= True
        
        for category in categorys:
            result = db.GqlQuery("SELECT __key__ FROM "+category.capitalize()+" WHERE "+category+'ID'+" = '"+id+"' AND wachtwoord='"+wachtwoord+"'")
            if result.count() >=1:
                self.response.out.write(getattr(webpages, category.capitalize()+'Page')(db.get(result[0])))
                NoValidCredentials = False
        
        if NoValidCredentials:
            self.response.out.write(webpages.LoginForm('Geen geldige combinatie!'))

class OuderAvondPlannen(webapp.RequestHandler):
    def get(self):
        self.response.out.write(webpages.header())
        self.response.out.write(htmlHelper.planningPage())
        self.response.out.write(webpages.footer())

class OuderAvondPlannenPost(webapp.RequestHandler):
    def post(self):
        self.response.out.write(webpages.header())
        docenten = self.request.get("checkedDocenten").split(",")
        datums = self.request.get("datums").split(",")
        splitDatums = []
        for datum in datums:
            splitDatums.append(datum.split("-"))
            
        for docent in docenten:
            for datum in splitDatums:
                afspraak = entities.Afspraak(leerlingID="0",docentID=docent,dag=datetime.date(int(datum[0]), int(datum[1]), int(datum[2])), tijd=-1,tafelnummer=0,beschrijving='#')
                afspraak.put();
            self.response.out.write(docent+" heeft ouderavond(en) op: <br />")
            for datum in datums:
                self.response.out.write(datum+" <br />")
            self.response.out.write("<br />")
        self.response.out.write(webpages.footer())
            
class AfspraakPlanningPost(webapp.RequestHandler):
    def post(self):
        key = self.request.get("afzegkey")
        if(len(key) != 0):
            afspraak = entities.Afspraak.get(key)
            afspraak.delete()
            self.redirect('/')
            return
        klas = self.request.get("klas")
        leerlingID = "4321"
        vakken = db.GqlQuery("SELECT * FROM VakPerKlas WHERE klas = '"+klas+"'")
        
        #self.response.out.write("<table border='1'><tr><th>leerlingID</th><th>docentID</th><th>dag</th><th>tijd</th><th>beschrijving</th></tr>")
        for vak in vakken:
            afspraakString = self.request.get(vak.docentID+"_afspraak")
            if(len(afspraakString) != 0):
                beschrijving = self.request.get(vak.docentID+"_beschrijving")
                afspraakData = afspraakString.split("_")
                
                datumStrings = afspraakData[0].split("-")
                
                afspraak = entities.Afspraak(leerlingID = leerlingID,docentID = vak.docentID,dag= datetime.date(int(datumStrings[0]),int(datumStrings[1]), int(datumStrings[2])),tijd= int(afspraakData[1]),tafelnummer=0,beschrijving = beschrijving)
                afspraak.put()
                self.redirect('/')
    
def main():
    application = webapp.WSGIApplication([('/', MainHandler),
                                          ('/authenticate', Authenticate),
                                          ('/afspraakplanningpost', AfspraakPlanningPost),
                                          ('/plannen', OuderAvondPlannen),
                                          ('/plannenpost', OuderAvondPlannenPost)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
